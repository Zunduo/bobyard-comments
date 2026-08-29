import time
from pathlib import Path

from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from .models import GenerationJob


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_image(self, job_id: int) -> str:
    """
    Simulate a long-running image generation task.

    In production this would call a GPU model / external API, upload to S3, etc.
    """
    job = GenerationJob.objects.get(pk=job_id)
    job.status = GenerationJob.Status.PROCESSING
    job.celery_task_id = self.request.id or ""
    job.save(update_fields=["status", "celery_task_id", "updated_at"])

    total_steps = 4
    duration = settings.IMAGE_GENERATION_SECONDS
    step_sleep = duration / total_steps

    try:
        for step in range(1, total_steps + 1):
            time.sleep(step_sleep)
            job.progress = int(step / total_steps * 100)
            job.save(update_fields=["progress", "updated_at"])

        image_bytes = _render_placeholder_image(job.prompt, job.order_index)
        filename = f"job-{job.id}.png"
        job.result_image.save(filename, ContentFile(image_bytes), save=False)
        job.status = GenerationJob.Status.COMPLETED
        job.progress = 100
        job.save(update_fields=["result_image", "status", "progress", "updated_at"])
        return filename
    except Exception as exc:
        job.status = GenerationJob.Status.FAILED
        job.error_message = str(exc)
        job.save(update_fields=["status", "error_message", "updated_at"])
        raise


def _render_placeholder_image(prompt: str, order_index: int) -> bytes:
  width, height = 640, 360
  image = Image.new("RGB", (width, height), color=(24, 32, 48))
  draw = ImageDraw.Draw(image)

  title = f"Generated image #{order_index}"
  body = prompt[:80] + ("..." if len(prompt) > 80 else "")

  draw.rectangle((20, 20, width - 20, height - 20), outline=(96, 165, 250), width=3)
  draw.text((40, 60), title, fill=(226, 232, 240))
  draw.text((40, 110), body, fill=(148, 163, 184))

  output = Path("/tmp") / "generated.png"
  image.save(output, format="PNG")
  return output.read_bytes()
