from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from fakecsv.utils import dataset_upload


class Schema(TimeStampedModel):
    class SeparatorSymbol(models.TextChoices):
        COMMA = ",", _("Comma (,)")
        DOT = ".", _("Dot (.)")
        TILDA = "~", _("Tilda (~)")
        COLON = ":", _("Colon (:)")
        SEMI_COLON = ";", _("Semi colon (:)")

    class StringChar(models.TextChoices):
        DOUBLE_QUOTE = '"', _('Double quote (")')
        SINGLE_QUOTE = "'", _("Single quote (')")

    title = models.CharField(
        max_length=40
    )
    column_separator = models.CharField(
        max_length=2,
        choices=SeparatorSymbol.choices,
        default=SeparatorSymbol.COMMA
    )
    string_character = models.CharField(
        max_length=2,
        choices=StringChar.choices,
        default=StringChar.DOUBLE_QUOTE
    )

    def __str__(self):
        return self.title


class Column(models.Model):
    class Type(models.TextChoices):
        FULL_NAME = "FULL_NAME", _("Full name")
        JOB = "JOB", _("Job")
        EMAIL = "EMAIL", _("Email")
        DOMAIN_NAME = "DOMAIN_NAME", _("Domain name")
        PHONE_NUMBER = "PHONE_NUMBER", _("Phone number")
        COMPANY_NAME = "COMPANY_NAME", _("Company name")
        TEXT = "TEXT", _("Text")
        INTEGER = "INTEGER", _("Integer")
        ADDRESS = "ADDRESS", _("Address")
        # DATE = "Date", _("Date")

    class Action(models.TextChoices):
        ADD = "ADD", _('Add')
        UPDATE = "UPDATE", _("Update")
        DELETE = "DELETE", _("DELETE")

    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=40
    )
    type = models.CharField(
        max_length=40,
        choices=Type.choices,
        default=Type.FULL_NAME
    )
    extra_data = models.JSONField(
        default={
            'start_range': 0,
            'end_range': 100
        }
    )
    order = models.IntegerField(
        help_text='Order by ASC'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order', )


class Dataset(TimeStampedModel):
    class Status(models.TextChoices):
        READY = "READY", _("Ready")
        PROCESSING = "PROCESSING", _("Processing")

    rows = models.PositiveIntegerField(
        validators=(MaxValueValidator(10000), )
    )

    schema = models.ForeignKey(
        Schema,
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        max_length=40,
        choices=Status.choices,
        default=Status.PROCESSING
    )

    result_file = models.FileField(
        upload_to=dataset_upload,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('created', )
