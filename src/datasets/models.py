from django.db import models
from django.contrib.auth.models import User
from colors.models import SchemeMixin, Palette
from cartograms.models import Cartogram, CartogramEntity

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


class Dataset(SchemeMixin, AbstractNameModel):
    PUBLISH_CHOICES = (
        (0, 'Not Published'),
        (1, 'Published'),
        # (2, 'Secret'), # Implemented in a later version
    )

    LICENSE_CHOICES = (
        ('L1', 'Some License 1'),
        ('L2', 'Some License 2'),
        ('L3', 'Some License 3'),
    )

    SCALE_CHOICES = (
        (0, "Quantize"),
        # (1, "Logarithmic"), # Scheduled for v.2
        # (2, "Linear"), # Scheduled for v.2
        # (3, "Exponential"), # Scheduled for v.2
    )

    description = models.TextField(blank=True)
    data_classes = models.SmallIntegerField(null=True) # Will only be null when using a non-quantized scale.
    scale = models.IntegerField(
        choices=SCALE_CHOICES, 
        default=0
    )
    palette = models.ForeignKey(
        Palette,
        null=True
    ) 
    published = models.IntegerField(
        choices=PUBLISH_CHOICES,
        default=0
    )
    license = models.CharField(
        max_length=8,
        choices=LICENSE_CHOICES,
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

    def import_dataset(self):
        """
        Upload file to tmp dir, then process and insert the data 
        """
        # What if there is no document associated with self
        import csv
        document = csv.reader(self.get_datafile())

        # What if the dataset already exist?
        # What if the document is not well formed?
        new_entities = None
        for row in document:

            entity = self.cartogram.entities.get(entity_id=row[0])
            record =  self.records.get_or_create(
                cartogram_entity=entity,
                defaults = {'value': row[1]}
            )
            new_entities = True if record[1] else False
            
        self.save()
        self.get_datafile().seek(0)
        return new_entities

    def validate_datafile(self):
        import csv
        # use CSV.Sniff
        dialect = csv.Sniffer().sniff(self.get_datafile().read(1024))

        if dialect.delimiter == ',':
            pass
        else:
            raise Exception("Incorrect delimiter")

        # check for headers

        self.get_datafile().seek(0)
        document = csv.reader(self.get_datafile())

        # iterate through and match the entity ids, 
        # or just check that the number of values match the number of datasets
        for row in document:
            if len(row) != 2:
                raise Exception("Number of cells in each row must be 2")
            
            try:
                self.cartogram.entities.get(entity_id=row[0])
            except CartogramEntity.DoesNotExist:
                message = "The Cartogram Entity does not exist with an entity_id {0}".format(row[0])
                raise Exception(message)

            # use regex to make sure it only contains numbers or .
            # if type(row[1]) is not float:
            #     print type(row[1])
            #     raise Exception("Values must be a numeric value")
                
        self.get_datafile().seek(0)
        # return information about why it did not validate.
        return True

    def get_datafile(self):
        return self.document.datafile.file.file

    def __unicode__(self):
        return self.name

class DatasetDocument(AbstractModel):
    datafile = models.FileField(upload_to='datasets/%Y/%m/%d')
    dataset = models.OneToOneField(
        Dataset,
        related_name='document'
    )
    owner = models.ForeignKey(
        User,
        related_name="documents"
    )

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

    class Meta:
        db_table = "datasets_dataset_record"

