# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GenreGroup'
        db.create_table('apps_genregroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
        ))
        db.send_create_signal('apps', ['GenreGroup'])

        # Adding model 'Raiting'
        db.create_table('apps_raiting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=8, unique=True)),
        ))
        db.send_create_signal('apps', ['Raiting'])

        # Adding model 'Genre'
        db.create_table('apps_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140, unique=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.GenreGroup'])),
            ('eng_name', self.gf('django.db.models.fields.CharField')(null=True, max_length=140)),
        ))
        db.send_create_signal('apps', ['Genre'])

        # Adding model 'ThematicGroup'
        db.create_table('apps_thematicgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
        ))
        db.send_create_signal('apps', ['ThematicGroup'])

        # Adding model 'Category'
        db.create_table('apps_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
            ('avatar', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.ThematicGroup'])),
        ))
        db.send_create_signal('apps', ['Category'])

        # Adding model 'Production'
        db.create_table('apps_production', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('avatar', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('old_limit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['apps.Raiting'])),
        ))
        db.send_create_signal('apps', ['Production'])

        # Adding M2M table for field genres on 'Production'
        m2m_table_name = db.shorten_name('apps_production_genres')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm['apps.production'], null=False)),
            ('genre', models.ForeignKey(orm['apps.genre'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'genre_id'])

        # Adding model 'Hero'
        db.create_table('apps_hero', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('avatar', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('apps', ['Hero'])

        # Adding model 'Anime'
        db.create_table('apps_anime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['apps.Production'])),
        ))
        db.send_create_signal('apps', ['Anime'])

        # Adding model 'Manga'
        db.create_table('apps_manga', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['apps.Production'])),
        ))
        db.send_create_signal('apps', ['Manga'])


    def backwards(self, orm):
        # Deleting model 'GenreGroup'
        db.delete_table('apps_genregroup')

        # Deleting model 'Raiting'
        db.delete_table('apps_raiting')

        # Deleting model 'Genre'
        db.delete_table('apps_genre')

        # Deleting model 'ThematicGroup'
        db.delete_table('apps_thematicgroup')

        # Deleting model 'Category'
        db.delete_table('apps_category')

        # Deleting model 'Production'
        db.delete_table('apps_production')

        # Removing M2M table for field genres on 'Production'
        db.delete_table(db.shorten_name('apps_production_genres'))

        # Deleting model 'Hero'
        db.delete_table('apps_hero')

        # Deleting model 'Anime'
        db.delete_table('apps_anime')

        # Deleting model 'Manga'
        db.delete_table('apps_manga')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'})
        },
        'apps.genre': {
            'Meta': {'ordering': "['id']", 'object_name': 'Genre'},
            'eng_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '140'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.GenreGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140', 'unique': 'True'})
        },
        'apps.genregroup': {
            'Meta': {'object_name': 'GenreGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
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
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['apps.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_limit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.Raiting']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        },
        'apps.raiting': {
            'Meta': {'object_name': 'Raiting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '8', 'unique': 'True'})
        },
        'apps.thematicgroup': {
            'Meta': {'object_name': 'ThematicGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        }
    }

    complete_apps = ['apps']