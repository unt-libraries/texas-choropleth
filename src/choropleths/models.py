from django.db import models
from django.contrib.auth.models import User
from datasets.models import Dataset, PublishedMixin

# Create your models here.
class AbstractModel(models.Model):
    status = models.BooleanField(default=False)
    name = models.CharField(max_length=96)

    class Meta:
        abstract= True

class SchemeMixin(models.Model):
    SCHEME_CHOICES = (
        (1, 'Sequential'),
        (2, 'Diverging'),
        (3, 'Qualitative'),
    )

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
    SCALE_CHOICES = (
        (0, "Quantize"),
        # (1, "Logarithmic"), # Scheduled for v.2
        # (2, "Linear"), # Scheduled for v.2
        # (3, "Exponential"), # Scheduled for v.2
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    dataset = models.OneToOneField(Dataset, null=True)
    description = models.TextField(blank=True)
    data_classes = models.SmallIntegerField(null=True) # Will only be null when using a non-quantized scale.
    scale = models.IntegerField(
        choices=SCALE_CHOICES, 
        default=0
    )
    palette = models.ForeignKey(
        Palette,
        null=True,
        to_field="class_name"
    ) 
    owner = models.ForeignKey(User, related_name="choropleths")

    def __unicode__(self):
        return self.name
