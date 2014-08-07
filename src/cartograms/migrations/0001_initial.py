# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cartogram'
        db.create_table(u'cartograms_cartogram', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('cartogram_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('json_filename', self.gf('django.db.models.fields.CharField')(max_length=96)),
        ))
        db.send_create_signal(u'cartograms', ['Cartogram'])

        # Adding model 'CartogramEntity'
        db.create_table('cartograms_entity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('entity_id', self.gf('django.db.models.fields.CharField')(max_length='16')),
            ('cartogram', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entities', db_column='cartogram', to=orm['cartograms.Cartogram'])),
        ))
        db.send_create_signal(u'cartograms', ['CartogramEntity'])

        # Adding unique constraint on 'CartogramEntity', fields ['entity_id', 'cartogram']
        db.create_unique('cartograms_entity', ['entity_id', 'cartogram'])

        # Adding index on 'CartogramEntity', fields ['entity_id', 'cartogram']
        db.create_index('cartograms_entity', ['entity_id', 'cartogram'])


    def backwards(self, orm):
        # Removing index on 'CartogramEntity', fields ['entity_id', 'cartogram']
        db.delete_index('cartograms_entity', ['entity_id', 'cartogram'])

        # Removing unique constraint on 'CartogramEntity', fields ['entity_id', 'cartogram']
        db.delete_unique('cartograms_entity', ['entity_id', 'cartogram'])

        # Deleting model 'Cartogram'
        db.delete_table(u'cartograms_cartogram')

        # Deleting model 'CartogramEntity'
        db.delete_table('cartograms_entity')


    models = {
        u'cartograms.cartogram': {
            'Meta': {'object_name': 'Cartogram'},
            'cartogram_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_filename': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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