# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Categories.url'
        db.add_column('content_categories', 'url',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2014, 5, 9, 0, 0), max_length=50, unique=True),
                      keep_default=False)


        # Changing field 'Categories.img'
        db.alter_column('content_categories', 'img', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True))
        # Adding unique constraint on 'Categories', fields ['img']
        db.create_unique('content_categories', ['img'])


    def backwards(self, orm):
        # Removing unique constraint on 'Categories', fields ['img']
        db.delete_unique('content_categories', ['img'])

        # Deleting field 'Categories.url'
        db.delete_column('content_categories', 'url')


        # Changing field 'Categories.img'
        db.alter_column('content_categories', 'img', self.gf('django.db.models.fields.URLField')(max_length=200))

    models = {
        'content.amw': {
            'Meta': {'object_name': 'AMW'},
            'anime': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['content.Anime']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True'})
        },
        'content.anime': {
            'Meta': {'object_name': 'Anime'},
            'avatars': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['content.Picture']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'en_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['content.Genre']", 'symmetrical': 'False'}),
            'heroes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['content.Hero']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jp_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'length_episode': ('django.db.models.fields.IntegerField', [], {'default': '24'}),
            'limitation': ('django.db.models.fields.IntegerField', [], {}),
            'num_series': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'period': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
            'raiting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Raiting']"}),
            'ru_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'season': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'studios': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['content.Studio']", 'symmetrical': 'False'}),
            'typ': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.AnimeType']"})
        },
        'content.animeseries': {
            'Meta': {'object_name': 'AnimeSeries'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        'content.animetype': {
            'Meta': {'object_name': 'AnimeType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True'})
        },
        'content.categories': {
            'Meta': {'object_name': 'Categories'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        },
        'content.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'content.employer': {
            'Meta': {'object_name': 'Employer'},
            'avatar': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'profession': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['content.Profession']", 'symmetrical': 'False'}),
            'second_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'content.ending': {
            'Meta': {'object_name': 'Ending'},
            'anime': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Anime']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True'})
        },
        'content.genre': {
            'Meta': {'object_name': 'Genre'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Category']"}),
            'description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        },
        'content.hero': {
            'Meta': {'object_name': 'Hero'},
            'avatars': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['content.Picture']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'content.imgtype': {
            'Meta': {'object_name': 'ImgType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'content.opening': {
            'Meta': {'object_name': 'Opening'},
            'anime': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Anime']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True'})
        },
        'content.picture': {
            'Meta': {'object_name': 'Picture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'img_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.ImgType']"})
        },
        'content.preview': {
            'Meta': {'object_name': 'Preview'},
            'anime': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Anime']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'unique': 'True'})
        },
        'content.profession': {
            'Meta': {'object_name': 'Profession'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        'content.raiting': {
            'Meta': {'object_name': 'Raiting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'content.studio': {
            'Meta': {'object_name': 'Studio'},
            'foundation_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['content']