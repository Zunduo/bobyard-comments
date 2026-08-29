from rest_framework import serializers

from .models import GenerationJob


class GenerationJobSerializer(serializers.ModelSerializer):
    result_url = serializers.SerializerMethodField()

    class Meta:
        model = GenerationJob
        fields = [
            "id",
            "prompt",
            "order_index",
            "status",
            "progress",
            "celery_task_id",
            "result_url",
            "error_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_result_url(self, obj: GenerationJob) -> str | None:
        if not obj.result_image:
            return None
        request = self.context.get("request")
        if request is None:
            return obj.result_image.url
        return request.build_absolute_uri(obj.result_image.url)


class CreateGenerationJobSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=500)
