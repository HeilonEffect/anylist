# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Genre.eng_name'
        db.delete_column('apps_genre', 'eng_name')


    def backwards(self, orm):
        # Adding field 'Genre.eng_name'
        db.add_column('apps_genre', 'eng_name',
                      self.gf('django.db.models.fields.CharField')(null=True, max_length=140),
                      keep_default=False)


    models = {
        'apps.anime': {
            'Meta': {'object_name': 'Anime'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['apps.Production']"})
        },
        'apps.category': {
            'Meta': {'object_name': 'Category'},
            'avatar': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.ThematicGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'apps.genre': {
            'Meta': {'object_name': 'Genre'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.GenreGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '140'})
        },
        'apps.genregroup': {
            'Meta': {'object_name': 'GenreGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'apps.hero': {
            'Meta': {'object_name': 'Hero'},
            'avatar': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'apps.manga': {
            'Meta': {'object_name': 'Manga'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['apps.Production']"})
        },
        'apps.production': {
            'Meta': {'object_name': 'Production'},
            'avatar': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['apps.Genre']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_limit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.Raiting']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'apps.raiting': {
            'Meta': {'object_name': 'Raiting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'})
        },
        'apps.thematicgroup': {
            'Meta': {'object_name': 'ThematicGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['apps']