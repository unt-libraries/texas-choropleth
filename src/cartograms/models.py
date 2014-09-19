from django.db import models

class AbstractCartogram(models.Model):
    status = models.BooleanField(default=True)
    name = models.CharField(max_length=96)

    class Meta:
        abstract = True


class Cartogram(AbstractCartogram): # Initially named Map, but changed to avoid interfering with keyword
    cartogram_id = models.CharField(
        max_length=16,
        unique=True
    )
    region_label = models.CharField(max_length=96)
    subregion_label = models.CharField(max_length=96)
    json_filename = models.CharField(max_length=96)

    def __unicode__(self):
        return self.name


class CartogramEntity(AbstractCartogram):
    entity_id = models.CharField(max_length=16) 
    cartogram = models.ForeignKey(
        Cartogram,
        related_name="entities",
        db_column="cartogram"  #change the column name since Cartogram already has a cartogram_id field
    ) 

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = [
            ['entity_id', 'cartogram']
        ]
        index_together = [
            ['entity_id', 'cartogram']
        ]
        db_table="cartograms_entity"

