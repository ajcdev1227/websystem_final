import datetime
import uuid

from django.db import models

from home.models import CustomUser, Client


class OfficerTenantAssignment(models.Model):
    """
    A relationship between a compliance officer and a tenant.
    This is to facilitate the assignment of tenants to compliance officers.
    """

    officer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Officer',
        help_text='The compliance officer',
    )

    tenant = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Tenant',
        help_text='The tenant assigned to the compliance officer',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['officer', 'tenant'], name='composite_pk')
        ]


class Case(models.Model):
    """
    A compliance case. These cases are analogous to changes to be reviewed.
    """

    id = models.BigAutoField(primary_key=True)

    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID',
        help_text='The external case UUID that\'s safe to expose',
    )

    created_ts = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created On',
        help_text='The timestamp when a case was created',
    )

    updated_ts = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name='Last Action On',
        help_text='The last time the case was updated, status changed, etc.',
    )

    approved_ts = models.DateTimeField(
        null=True,
        default=None,
        verbose_name='Date Approved'
    )
    """Will be null if the submission hasn't yet been approved"""

    rejected_ts = models.DateTimeField(
        null=True,
        default=None,
        verbose_name='Date Rejected'
    )
    """Will be null if the submission hasn't yet been rejected"""

    resource_title = models.CharField(
        max_length=255,
        verbose_name='Title',
        help_text='The title of the resource associated with the case',
    )
    resource_key = models.CharField(
        max_length=255,
        verbose_name='Page',
        help_text='The key/path of the resource/page associated with the case'
    )
    resource_snapshot = models.CharField(
        max_length=10485760,  # 10MiB
        default='[]',
        verbose_name='Resource Snapshot JSON',
        help_text='A snapshot of the resource associated with the case, encoded as a JSON string'
    )

    TYPE_CHOICES = [('cms', 'CMS'), ('crm', 'CRM')]
    type = models.CharField(
        choices=TYPE_CHOICES,
        default='cms',
        verbose_name='Type',
        help_text='The case type',
        max_length=255
    )

    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    status = models.CharField(
        choices=STATUS_CHOICES,
        verbose_name='Status',
        help_text='The current status of the case',
        max_length=255
    )

    reviewed_by = models.ForeignKey(
        CustomUser,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        verbose_name='Reviewed By',
        help_text='The compliance officer who reviewed the case'
    )
    officer_notes = models.CharField(
        max_length=2048,
        null=True,
        blank=True,
        verbose_name='Notes',
        help_text='Any additional notes on the case by the compliance officer',
    )

    tenant = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Tenant',
        help_text='The tenant the case came from',
    )

    def save(self, *args, **kwargs):
        # Set updated_ts to current timestamp when saving the object
        self.updated_ts = datetime.datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.resource_title} - {self.uuid}"

    def get_path(self) -> str:
        """
        Returns the path from the compliance site for the case
        """

        return '/case/' + str(self.uuid)


VALID_CASE_STATUSES = []
"""All valid case statuses"""


# Populate statuses from constant in Case
for status in Case.STATUS_CHOICES:
    VALID_CASE_STATUSES.append(status[0])
