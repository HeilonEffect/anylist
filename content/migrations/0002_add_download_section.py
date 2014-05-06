# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NavigationItem.url'
        db.add_column('content_navigationitem', 'url',
                      self.gf('django.db.models.fields.CharField')(max_length=60, default=datetime.datetime(2014, 5, 6, 0, 0)),
                      keep_default=False)

        # Adding field 'NavigationSubItem.url'
        db.add_column('content_navigationsubitem', 'url',
                      self.gf('django.db.models.fields.CharField')(max_length=60, default=datetime.datetime(2014, 5, 6, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'NavigationItem.url'
        db.delete_column('content_navigationitem', 'url')

        # Deleting field 'NavigationSubItem.url'
        db.delete_column('content_navigationsubitem', 'url')


    models = {
        'content.navigationitem': {
            'Meta': {'object_name': 'NavigationItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'content.navigationsubitem': {
            'Meta': {'object_name': 'NavigationSubItem'},
            'head': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.NavigationItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['content']