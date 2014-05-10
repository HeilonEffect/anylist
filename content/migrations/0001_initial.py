# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Raiting'
        db.create_table('content_raiting', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('content', ['Raiting'])

        # Adding model 'ImgType'
        db.create_table('content_imgtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('content', ['ImgType'])

        # Adding model 'AnimeType'
        db.create_table('content_animetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('content', ['AnimeType'])

        # Adding model 'Picture'
        db.create_table('content_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('img', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('img_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.ImgType'])),
        ))
        db.send_create_signal('content', ['Picture'])

        # Adding model 'Category'
        db.create_table('content_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('content', ['Category'])

        # Adding model 'Genre'
        db.create_table('content_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Category'])),
        ))
        db.send_create_signal('content', ['Genre'])

        # Adding model 'Profession'
        db.create_table('content_profession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
        ))
        db.send_create_signal('content', ['Profession'])

        # Adding model 'Employer'
        db.create_table('content_employer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('second_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('avatar', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('content', ['Employer'])

        # Adding M2M table for field profession on 'Employer'
        m2m_table_name = db.shorten_name('content_employer_profession')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('employer', models.ForeignKey(orm['content.employer'], null=False)),
            ('profession', models.ForeignKey(orm['content.profession'], null=False))
        ))
        db.create_unique(m2m_table_name, ['employer_id', 'profession_id'])

        # Adding model 'Studio'
        db.create_table('content_studio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('foundation_date', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal('content', ['Studio'])

        # Adding model 'Hero'
        db.create_table('content_hero', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('content', ['Hero'])

        # Adding M2M table for field avatars on 'Hero'
        m2m_table_name = db.shorten_name('content_hero_avatars')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hero', models.ForeignKey(orm['content.hero'], null=False)),
            ('picture', models.ForeignKey(orm['content.picture'], null=False))
        ))
        db.create_unique(m2m_table_name, ['hero_id', 'picture_id'])

        # Adding model 'Anime'
        db.create_table('content_anime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('jp_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ru_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('en_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('season', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('num_series', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('length_episode', self.gf('django.db.models.fields.IntegerField')(default=24)),
            ('period', self.gf('django.db.models.fields.IntegerField')(default=7)),
            ('raiting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Raiting'])),
            ('limitation', self.gf('django.db.models.fields.IntegerField')()),
            ('typ', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.AnimeType'])),
        ))
        db.send_create_signal('content', ['Anime'])

        # Adding M2M table for field genres on 'Anime'
        m2m_table_name = db.shorten_name('content_anime_genres')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('anime', models.ForeignKey(orm['content.anime'], null=False)),
            ('genre', models.ForeignKey(orm['content.genre'], null=False))
        ))
        db.create_unique(m2m_table_name, ['anime_id', 'genre_id'])

        # Adding M2M table for field studios on 'Anime'
        m2m_table_name = db.shorten_name('content_anime_studios')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('anime', models.ForeignKey(orm['content.anime'], null=False)),
            ('studio', models.ForeignKey(orm['content.studio'], null=False))
        ))
        db.create_unique(m2m_table_name, ['anime_id', 'studio_id'])

        # Adding M2M table for field avatars on 'Anime'
        m2m_table_name = db.shorten_name('content_anime_avatars')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('anime', models.ForeignKey(orm['content.anime'], null=False)),
            ('picture', models.ForeignKey(orm['content.picture'], null=False))
        ))
        db.create_unique(m2m_table_name, ['anime_id', 'picture_id'])

        # Adding M2M table for field heroes on 'Anime'
        m2m_table_name = db.shorten_name('content_anime_heroes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('anime', models.ForeignKey(orm['content.anime'], null=False)),
            ('hero', models.ForeignKey(orm['content.hero'], null=False))
        ))
        db.create_unique(m2m_table_name, ['anime_id', 'hero_id'])

        # Adding model 'Opening'
        db.create_table('content_opening', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('anime', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Anime'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('content', ['Opening'])

        # Adding model 'Ending'
        db.create_table('content_ending', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('anime', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Anime'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('content', ['Ending'])

        # Adding model 'Preview'
        db.create_table('content_preview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('anime', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Anime'])),
        ))
        db.send_create_signal('content', ['Preview'])

        # Adding model 'AnimeSeries'
        db.create_table('content_animeseries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('content', ['AnimeSeries'])

        # Adding model 'AMW'
        db.create_table('content_amw', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('content', ['AMW'])

        # Adding M2M table for field anime on 'AMW'
        m2m_table_name = db.shorten_name('content_amw_anime')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('amw', models.ForeignKey(orm['content.amw'], null=False)),
            ('anime', models.ForeignKey(orm['content.anime'], null=False))
        ))
        db.create_unique(m2m_table_name, ['amw_id', 'anime_id'])

        # Adding model 'Categories'
        db.create_table('content_categories', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('img', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('content', ['Categories'])


    def backwards(self, orm):
        # Deleting model 'Raiting'
        db.delete_table('content_raiting')

        # Deleting model 'ImgType'
        db.delete_table('content_imgtype')

        # Deleting model 'AnimeType'
        db.delete_table('content_animetype')

        # Deleting model 'Picture'
        db.delete_table('content_picture')

        # Deleting model 'Category'
        db.delete_table('content_category')

        # Deleting model 'Genre'
        db.delete_table('content_genre')

        # Deleting model 'Profession'
        db.delete_table('content_profession')

        # Deleting model 'Employer'
        db.delete_table('content_employer')

        # Removing M2M table for field profession on 'Employer'
        db.delete_table(db.shorten_name('content_employer_profession'))

        # Deleting model 'Studio'
        db.delete_table('content_studio')

        # Deleting model 'Hero'
        db.delete_table('content_hero')

        # Removing M2M table for field avatars on 'Hero'
        db.delete_table(db.shorten_name('content_hero_avatars'))

        # Deleting model 'Anime'
        db.delete_table('content_anime')

        # Removing M2M table for field genres on 'Anime'
        db.delete_table(db.shorten_name('content_anime_genres'))

        # Removing M2M table for field studios on 'Anime'
        db.delete_table(db.shorten_name('content_anime_studios'))

        # Removing M2M table for field avatars on 'Anime'
        db.delete_table(db.shorten_name('content_anime_avatars'))

        # Removing M2M table for field heroes on 'Anime'
        db.delete_table(db.shorten_name('content_anime_heroes'))

        # Deleting model 'Opening'
        db.delete_table('content_opening')

        # Deleting model 'Ending'
        db.delete_table('content_ending')

        # Deleting model 'Preview'
        db.delete_table('content_preview')

        # Deleting model 'AnimeSeries'
        db.delete_table('content_animeseries')

        # Deleting model 'AMW'
        db.delete_table('content_amw')

        # Removing M2M table for field anime on 'AMW'
        db.delete_table(db.shorten_name('content_amw_anime'))

        # Deleting model 'Categories'
        db.delete_table('content_categories')


    models = {
        'content.amw': {
            'Meta': {'object_name': 'AMW'},
            'anime': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['content.Anime']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'content.anime': {
            'Meta': {'object_name': 'Anime'},
            'avatars': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['content.Picture']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'en_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['content.Genre']"}),
            'heroes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['content.Hero']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jp_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'length_episode': ('django.db.models.fields.IntegerField', [], {'default': '24'}),
            'limitation': ('django.db.models.fields.IntegerField', [], {}),
            'num_series': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'period': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
            'raiting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Raiting']"}),
            'ru_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'season': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'studios': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['content.Studio']"}),
            'typ': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.AnimeType']"})
        },
        'content.animeseries': {
            'Meta': {'object_name': 'AnimeSeries'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        'content.animetype': {
            'Meta': {'object_name': 'AnimeType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'content.categories': {
            'Meta': {'object_name': 'Categories'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'content.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'content.employer': {
            'Meta': {'object_name': 'Employer'},
            'avatar': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'profession': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['content.Profession']"}),
            'second_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'content.ending': {
            'Meta': {'object_name': 'Ending'},
            'anime': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Anime']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'content.genre': {
            'Meta': {'object_name': 'Genre'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Category']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'content.hero': {
            'Meta': {'object_name': 'Hero'},
            'avatars': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['content.Picture']"}),
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
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
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
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
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