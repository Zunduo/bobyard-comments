from django.urls import path

from .views import GenerationJobDetailView, GenerationJobListCreateView

urlpatterns = [
    path("jobs/", GenerationJobListCreateView.as_view(), name="job-list-create"),
    path("jobs/<int:job_id>/", GenerationJobDetailView.as_view(), name="job-detail"),
]
