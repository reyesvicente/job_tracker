import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from job_tracker.jobs.models import Application  # Use absolute import

User = get_user_model()


@pytest.mark.django_db
def test_application_views(client):
    user = User.objects.create(username="testuser")
    client.force_login(user)

    # Test ApplicationListView
    response = client.get(reverse("jobs:list"))
    assert response.status_code == 200
    assert (
        "applications" in response.context
    ), f"Expected 'applications' in context, but context was: { response.context}"  # noqa

    applications = response.context["applications"]
    assert len(applications) == 0, f"Expected 0 applications, but got {len(applications)}"

    # Test ApplicationCreateView
    response = client.post(
        reverse("jobs:add"),
        {
            "name": "Test Name",
            "email": "test@example.com",
            "company_name": "Test Company",
            "position": "Test Position",
            "rate": "Test Rate",
            "status": Application.JobStatus.submitted_proposal,
            "notes": "Test Notes",
        },
    )
    assert response.status_code == 302  # Redirect after successful form submission
    assert Application.objects.count() == 1  # One application should be created

    # Test ApplicationDetailView
    application = Application.objects.first()
    response = client.get(reverse("jobs:detail", kwargs={"slug": application.slug}))
    assert response.status_code == 200
    assert "application" in response.context
    assert response.context["application"] == application

    # Test ApplicationUpdateView
    response = client.post(
        reverse("jobs:update", kwargs={"slug": application.slug}),
        {
            "name": "Updated Name",
            "email": "updated@example.com",
            "company_name": "Updated Company",
            "position": "Updated Position",
            "rate": "Updated Rate",
            "status": Application.JobStatus.applied,
            "notes": "Updated Notes",
        },
    )
    assert response.status_code == 302  # Redirect after successful form submission
    application.refresh_from_db()
    assert application.name == "Updated Name"

    # Test ApplicationDeleteView
    response = client.post(reverse("jobs:delete", kwargs={"slug": application.slug}))
    assert response.status_code == 302  # Redirect after successful deletion
    assert Application.objects.count() == 0  # No applications left

    # Make sure the user is redirected to the list view after deletion
    response = client.get(reverse("jobs:detail", kwargs={"slug": application.slug}))
    assert response.status_code == 302
    assert response.url == reverse("jobs:list")
