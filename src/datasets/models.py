import os
import csv
from decimal import *

from django.db import models
from django.contrib.auth.models import User
from cartograms.models import Cartogram, CartogramEntity
from .validators import import_validator

SCALE_CHOICES = (
    (0, "Quantize"),
    (1, "Logarithmic"),
    # (2, "Linear"), # Scheduled for v.2
    # (3, "Exponential"), # Scheduled for v.2
)

class AbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        abstract = True


class AbstractNameModel(AbstractModel):
    name = models.CharField(max_length=96)

    class Meta:
        abstract = True

class PublishedMixin(models.Model):
    PUBLISH_CHOICES = (
        (0, 'No'),
        (1, 'Yes'),
        # (2, 'Secret'), # Implemented in a later version
    )
    published = models.IntegerField(
        choices=PUBLISH_CHOICES,
        default=0
    )
    class Meta:
        abstract = True

class Dataset(PublishedMixin, AbstractNameModel):
    LICENSE_CHOICES = (
        ('L1', 'Some License 1'),
        ('L2', 'Some License 2'),
        ('L3', 'Some License 3'),
    )

    description = models.TextField(blank=True)
    label = models.CharField(
        max_length=48,
        blank=True,
    )
    license = models.CharField(
        max_length=8,
        choices=LICENSE_CHOICES,
        blank=True,
        null=True
    ) 
    cartogram = models.ForeignKey(
        Cartogram,
        on_delete=models.PROTECT
    )
    owner = models.ForeignKey(
        User,
        related_name="datasets",
        null=True,
        on_delete=models.SET_NULL
    )

    def has_records(self):
        return self.records.exists()

    def has_choropleth(self):
        return hasattr(self, 'choropleth')

    def get_max_record(self):
        if self.records.exists():
            max_value = self.records.all().aggregate(models.Max('value'))
            return max_value['value__max']

    def get_min_record(self):
        if self.records.exists():
            min_value = self.records.all().aggregate(models.Min('value'))
            return min_value['value__min']

    def get_scales(self):
        """
        Scales are stored with the Choropleth
        However, the elible options are determined based on
        the min and max of the dataset
        """
        scales = [SCALE_CHOICES[0]]
        min_value = self.get_min_record()
        max_value = self.get_max_record()

        if abs(min_value) > 0 and abs(max_value):
            scales.append(SCALE_CHOICES[1])

        return scales

    def import_dataset(self):
        """
        Import datafile records into the DatasetRecord
        """
        document = csv.reader(self.get_datafile().read().splitlines())

        imported_records = dict([('created', 0), ('updated', 0)])
        for row_num, row in enumerate(document):
            #skip over the headers
            if row_num == 0:
                continue
            elif len(row) == 0:
                continue
            else:
                is_null = True if not row[2] else False
                if is_null:
                    row[2] = None

                entity = self.cartogram.entities.get(entity_id=row[0])
                record, created =  self.records.get_or_create(
                    cartogram_entity=entity,
                    defaults = {'value': row[2]}
                )

                # Update the value only if it has changed
                new_records = 0
                updated_records = 0
                if not created:
                    if (is_null and record.value != row[2]) or (not is_null and record.value != Decimal(row[2])):
                        record.value = row[2]
                        record.save()
                        imported_records['updated'] += 1
                if created:
                    imported_records['created'] += 1

        self.save()
        self.get_datafile().seek(0)
        print imported_records
        return imported_records

    def get_datafile(self):
        return self.document.datafile

    def __unicode__(self):
        return self.name

class DatasetDocument(AbstractModel):
    datafile = models.FileField(
        upload_to='datasets/%Y/%m/%d',
        validators=[import_validator]
    )
    dataset = models.OneToOneField(
        Dataset,
        related_name='document'
    )
    owner = models.ForeignKey(
        User,
        related_name="documents"
    )

    def __unicode__(self):
        return os.path.basename(self.datafile.name)

    class Meta:
        db_table = 'datasets_dataset_document'


class DatasetRecord(AbstractModel):
    cartogram_entity = models.ForeignKey(
        CartogramEntity,
        on_delete=models.PROTECT
    )
    value = models.DecimalField(
        max_digits=25,
        decimal_places=6,
        null=True,
        blank=True
    )
    dataset = models.ForeignKey(
        Dataset,
        related_name="records"
    )

    def replace_datafile(self, document):
        self.objects.remove

    def get_entity_id(self):
        return self.cartogram_entity.entity_id

    def get_entity_name(self):
        return self.cartogram_entity.name

    class Meta:
        db_table = "datasets_dataset_record"

