# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Cartogram.region_label'
        db.add_column(u'cartograms_cartogram', 'region_label',
                      self.gf('django.db.models.fields.CharField')(default='State', max_length=96),
                      keep_default=False)

        # Adding field 'Cartogram.subregion_label'
        db.add_column(u'cartograms_cartogram', 'subregion_label',
                      self.gf('django.db.models.fields.CharField')(default='County', max_length=96),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Cartogram.region_label'
        db.delete_column(u'cartograms_cartogram', 'region_label')

        # Deleting field 'Cartogram.subregion_label'
        db.delete_column(u'cartograms_cartogram', 'subregion_label')


    models = {
        u'cartograms.cartogram': {
            'Meta': {'object_name': 'Cartogram'},
            'cartogram_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_filename': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'region_label': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subregion_label': ('django.db.models.fields.CharField', [], {'max_length': '96'})
        },
        u'cartograms.cartogramentity': {
            'Meta': {'unique_together': "[['entity_id', 'cartogram']]", 'object_name': 'CartogramEntity', 'db_table': "'cartograms_entity'", 'index_together': "[['entity_id', 'cartogram']]"},
            'cartogram': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities'", 'db_column': "'cartogram'", 'to': u"orm['cartograms.Cartogram']"}),
            'entity_id': ('django.db.models.fields.CharField', [], {'max_length': "'16'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['cartograms']