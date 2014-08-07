# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Palette'
        db.create_table(u'colors_palette', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scheme', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('class_name', self.gf('django.db.models.fields.CharField')(max_length=96)),
        ))
        db.send_create_signal(u'colors', ['Palette'])


    def backwards(self, orm):
        # Deleting model 'Palette'
        db.delete_table(u'colors_palette')


    models = {
        u'colors.palette': {
            'Meta': {'object_name': 'Palette'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scheme': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['colors']