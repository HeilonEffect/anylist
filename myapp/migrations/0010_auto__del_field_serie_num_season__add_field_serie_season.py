# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Serie.num_season'
        db.delete_column('myapp_serie', 'num_season_id')

        # Adding field 'Serie.season'
        db.add_column('myapp_serie', 'season',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['myapp.SeriesGroup']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Serie.num_season'
        db.add_column('myapp_serie', 'num_season',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['myapp.SeriesGroup']),
                      keep_default=False)

        # Deleting field 'Serie.season'
        db.delete_column('myapp_serie', 'season_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'myapp.altname': {
            'Meta': {'object_name': 'AltName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'myapp.category': {
            'Meta': {'object_name': 'Category', 'ordering': "('name',)"},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.CategoryGroup']"}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'myapp.categorygroup': {
            'Meta': {'object_name': 'CategoryGroup', 'ordering': "('name',)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'myapp.creator': {
            'Meta': {'object_name': 'Creator'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '100', 'null': 'True'}),
            'employ': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Employ']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'myapp.employ': {
            'Meta': {'object_name': 'Employ'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'myapp.genre': {
            'Meta': {'object_name': 'Genre', 'ordering': "('name',)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'myapp.genregroup': {
            'Meta': {'object_name': 'GenreGroup'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.CategoryGroup']"}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['myapp.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'myapp.hero': {
            'Meta': {'object_name': 'Hero'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Creator']"}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_main_hero': ('django.db.models.fields.NullBooleanField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'myapp.product': {
            'Meta': {'object_name': 'Product', 'ordering': "('title',)"},
            'alt_names': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['myapp.AltName']"}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Category']"}),
            'creators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['myapp.Creator']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['myapp.Genre']"}),
            'heroes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['myapp.Hero']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_limit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['myapp.Raiting']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'myapp.raiting': {
            'Meta': {'object_name': 'Raiting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'myapp.serie': {
            'Meta': {'object_name': 'Serie', 'ordering': "('-number',)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['myapp.SeriesGroup']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'})
        },
        'myapp.serielist': {
            'Meta': {'object_name': 'SerieList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.NullBooleanField', [], {'blank': 'True', 'null': 'True'}),
            'serie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Serie']"}),
            'user_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.UserList']"})
        },
        'myapp.seriesgroup': {
            'Meta': {'object_name': 'SeriesGroup'},
            'frozen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255', 'null': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Product']"})
        },
        'myapp.status': {
            'Meta': {'object_name': 'Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'myapp.userlist': {
            'Meta': {'object_name': 'UserList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Product']"}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Status']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['myapp']