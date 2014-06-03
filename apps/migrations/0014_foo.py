# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ListedProduct.user'
        db.delete_column('apps_listedproduct', 'user_id')


    def backwards(self, orm):
        # Adding field 'ListedProduct.user'
        db.add_column('apps_listedproduct', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
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
        'apps.listedproduct': {
            'Meta': {'object_name': 'ListedProduct'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.Production']"}),
            'series': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['apps.Serie']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.Status']"})
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
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['apps.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_limit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.Raiting']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'apps.raiting': {
            'Meta': {'object_name': 'Raiting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'})
        },
        'apps.serie': {
            'Meta': {'object_name': 'Serie', 'ordering': "['-number']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.SeriesGroup']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'apps.seriesgroup': {
            'Meta': {'object_name': 'SeriesGroup', 'ordering': "['-number']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.Production']"})
        },
        'apps.status': {
            'Meta': {'object_name': 'Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'})
        },
        'apps.thematicgroup': {
            'Meta': {'object_name': 'ThematicGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['apps']