# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dataset'
        db.create_table(u'datasets_dataset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scheme', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('data_classes', self.gf('django.db.models.fields.SmallIntegerField')(null=True)),
            ('scale', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('palette', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['colors.Palette'], null=True)),
            ('published', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('license', self.gf('django.db.models.fields.CharField')(max_length=8, null=True)),
            ('cartogram', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartograms.Cartogram'], on_delete=models.PROTECT)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='datasets', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'datasets', ['Dataset'])

        # Adding model 'DatasetDocument'
        db.create_table('datasets_dataset_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('datafile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('dataset', self.gf('django.db.models.fields.related.OneToOneField')(related_name='document', unique=True, to=orm['datasets.Dataset'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='documents', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'datasets', ['DatasetDocument'])

        # Adding model 'DatasetRecord'
        db.create_table('datasets_dataset_record', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cartogram_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartograms.CartogramEntity'], on_delete=models.PROTECT)),
            ('value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=25, decimal_places=6, blank=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='records', to=orm['datasets.Dataset'])),
        ))
        db.send_create_signal(u'datasets', ['DatasetRecord'])


    def backwards(self, orm):
        # Deleting model 'Dataset'
        db.delete_table(u'datasets_dataset')

        # Deleting model 'DatasetDocument'
        db.delete_table('datasets_dataset_document')

        # Deleting model 'DatasetRecord'
        db.delete_table('datasets_dataset_record')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
        },
        u'colors.palette': {
            'Meta': {'object_name': 'Palette'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scheme': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'datasets.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'cartogram': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cartograms.Cartogram']", 'on_delete': 'models.PROTECT'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_classes': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'datasets'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'palette': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['colors.Palette']", 'null': 'True'}),
            'published': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'scale': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'scheme': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'datasets.datasetdocument': {
            'Meta': {'object_name': 'DatasetDocument', 'db_table': "'datasets_dataset_document'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datafile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'dataset': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'document'", 'unique': 'True', 'to': u"orm['datasets.Dataset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['auth.User']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'datasets.datasetrecord': {
            'Meta': {'object_name': 'DatasetRecord', 'db_table': "'datasets_dataset_record'"},
            'cartogram_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cartograms.CartogramEntity']", 'on_delete': 'models.PROTECT'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'records'", 'to': u"orm['datasets.Dataset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '25', 'decimal_places': '6', 'blank': 'True'})
        }
    }

    complete_apps = ['datasets']