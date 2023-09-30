import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from job_tracker.jobs.models import Application  # Use absolute import

User = get_user_model()


@pytest.mark.django_db
def test_application_model():
    user = User.objects.create(username="testuser")
    application = Application.objects.create(
        user=user,
        name="Test Name",
        email="test@example.com",
        company_name="Test Company",
        position="Test Position",
        rate="Test Rate",
        status=Application.JobStatus.submitted_proposal,
        notes="Test Notes",
    )
    assert application.slug == "test-company"  # Make sure the slug is correctly generated
    assert str(application) == "test-company"  # Ensure the __str__ method works correctly
    assert application.get_absolute_url() == reverse(
        "jobs:detail", kwargs={"slug": application.slug}
    )  # Test get_absolute_url()
