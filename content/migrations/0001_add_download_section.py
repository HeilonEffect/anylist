# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NavigationItem'
        db.create_table('content_navigationitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('content', ['NavigationItem'])

        # Adding model 'NavigationSubItem'
        db.create_table('content_navigationsubitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('head', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.NavigationItem'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('content', ['NavigationSubItem'])


    def backwards(self, orm):
        # Deleting model 'NavigationItem'
        db.delete_table('content_navigationitem')

        # Deleting model 'NavigationSubItem'
        db.delete_table('content_navigationsubitem')


    models = {
        'content.navigationitem': {
            'Meta': {'object_name': 'NavigationItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'content.navigationsubitem': {
            'Meta': {'object_name': 'NavigationSubItem'},
            'head': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.NavigationItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['content']