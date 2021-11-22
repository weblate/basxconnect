from django.db import models
from django.utils.translation import gettext_lazy as _
from languages.fields import LanguageField

from basxconnect.core.models import Email

LanguageField.db_collation = None  # fix issue with LanguageField in django 3.2


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    external_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def languages_choices(field, request, instance):
    from basxconnect.core import settings

    return settings.PREFERRED_LANGUAGES


class SynchronizationResult(models.Model):
    total_synchronized_persons = models.IntegerField(null=True)
    sync_completed_datetime = models.DateTimeField(null=True)


class Subscription(models.Model):
    email = models.OneToOneField(Email, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[
            ("subscribed", "subscribed"),
            ("unsubscribed", "unsubscribed"),
            ("non-subscribed", "non-subscribed"),
            ("cleaned", "cleaned"),
        ],
    )

    interests = models.ManyToManyField(Interest, blank=True)
    interests.verbose_name = _("Mailing Interests")

    language = LanguageField(
        _("Language"), blank=True, max_length=8
    )  # mitigate up-stream bug
    language.lazy_choices = languages_choices

    latest_sync = models.ForeignKey(
        SynchronizationResult,
        related_name="synchronized_subscription",
        on_delete=models.SET_NULL,
        null=True,
    )


class SynchronizationPerson(models.Model):
    sync_result = models.ForeignKey(
        SynchronizationResult, on_delete=models.CASCADE, related_name="persons"
    )
    email = models.CharField(max_length=100)
    first_name = models.CharField(_("First Name"), max_length=255, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=255, blank=True)

    NEW = "new"
    SKIPPED = "import_error"
    NOT_SYNCED = "not_synced"
    SYNC_STATUS_CHOICES = [
        (NEW, _("Newly added to BasxConnect")),
        (SKIPPED, _("Was not added to BasxConnect")),
        (NOT_SYNCED, _("Previously synchronized but not this time")),
    ]
    sync_status = models.CharField(
        _("Synchronization Status"),
        choices=SYNC_STATUS_CHOICES,
        max_length=255,
        blank=True,
    )

    def __str__(self):
        return self.email
