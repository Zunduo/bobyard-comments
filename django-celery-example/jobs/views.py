from django.db import transaction
from django.db.models import Max
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GenerationJob
from .serializers import CreateGenerationJobSerializer, GenerationJobSerializer
from .tasks import generate_image


class GenerationJobListCreateView(APIView):
    def get(self, request):
        jobs = GenerationJob.objects.all()
        serializer = GenerationJobSerializer(jobs, many=True, context={"request": request})
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        payload = CreateGenerationJobSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        next_order = (
            GenerationJob.objects.aggregate(max_order=Max("order_index"))["max_order"] or 0
        ) + 1

        job = GenerationJob.objects.create(
            prompt=payload.validated_data["prompt"],
            order_index=next_order,
        )

        async_result = generate_image.delay(job.id)
        job.celery_task_id = async_result.id
        job.save(update_fields=["celery_task_id", "updated_at"])

        serializer = GenerationJobSerializer(job, context={"request": request})
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class GenerationJobDetailView(APIView):
    def get(self, request, job_id: int):
        job = GenerationJob.objects.get(pk=job_id)
        serializer = GenerationJobSerializer(job, context={"request": request})
        return Response(serializer.data)
