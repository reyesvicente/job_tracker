from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import models
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel

User = get_user_model()


class Application(TimeStampedModel):
    class JobStatus(models.TextChoices):
        submitted_proposal = "Submitted Proposal"
        applied = "Applied"
        meeting_done = "Meeting Done"
        for_meeting = "For Meeting"
        no_reply = "No Reply"

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='company_name', default=None)
    email = models.EmailField()
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    rate = models.CharField(max_length=100)
    status = models.CharField(choices=JobStatus.choices, max_length=50)
    notes = models.TextField()

    class Meta:
        verbose_name = 'tracker'
        verbose_name_plural = 'tracker'
        
    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("jobs:detail", kwargs={"slug": self.slug})