from django.db import models

class AbstractColor:
    status = models.BooleanField(default=False)
    name = models.CharField(max_length=96)

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

class Palette(SchemeMixin, AbstractColor):
    class_name = models.CharField(max_length=96)

    def __unicode__(self):
        return self.name

