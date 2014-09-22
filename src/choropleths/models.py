from django.db import models
from django.contrib.auth.models import User
from datasets.models import Dataset, PublishedMixin, SCALE_CHOICES

SCHEME_CHOICES = (
    (1, 'Sequential'),
    (2, 'Diverging'),
    (3, 'Qualitative'),
)


class AbstractModel(models.Model):
    status = models.BooleanField(default=False)
    name = models.CharField(max_length=96)

    class Meta:
        abstract = True


class SchemeMixin(models.Model):
    SCHEME_CHOICES = SCHEME_CHOICES

    scheme = models.IntegerField(
        choices=SCHEME_CHOICES,
        null=True
    )

    class Meta:
        abstract = True


class Palette(SchemeMixin, AbstractModel):
    class_name = models.CharField(max_length=96, unique=True)

    def __unicode__(self):
        return self.name


class Choropleth(PublishedMixin, SchemeMixin, AbstractModel):
    SCALE_CHOICES = SCALE_CHOICES
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    dataset = models.OneToOneField(Dataset, null=True)
    description = models.TextField(blank=True)
    data_classes = models.SmallIntegerField(null=True)
    scale = models.IntegerField(
        choices=SCALE_CHOICES,
        default=0
    )
    palette = models.ForeignKey(
        Palette,
        null=True,
    )
    thumbnail = models.ImageField(upload_to="thumbnails", null=True)
    owner = models.ForeignKey(User, related_name="choropleths")

    def get_dataset_id(self):
        """
        Double dispatch method for getting the Dataset id from the generic
        context object.
        """
        if hasattr(self.dataset, 'id'):
            return self.dataset.id
        return

    def get_choropleth_id(self):
        """
        Double dispatch method for getting the Choropleth id from the generic
        context object.
        """
        return self.id

    def has_records(self):
        """
        Double dispatch method for checking if the generic context object
        has records associated with it.
        """
        if hasattr(self.dataset, 'records'):
            return self.dataset.records.exists()
        return False

    def __unicode__(self):
        return self.name
