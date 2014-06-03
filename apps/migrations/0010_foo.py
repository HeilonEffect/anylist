# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserList'
        db.delete_table('apps_userlist')

        # Removing M2M table for field content on 'UserList'
        db.delete_table(db.shorten_name('apps_userlist_content'))


    def backwards(self, orm):
        # Adding model 'UserList'
        db.create_table('apps_userlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('apps', ['UserList'])

        # Adding M2M table for field content on 'UserList'
        m2m_table_name = db.shorten_name('apps_userlist_content')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userlist', models.ForeignKey(orm['apps.userlist'], null=False)),
            ('listedproduct', models.ForeignKey(orm['apps.listedproduct'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userlist_id', 'listedproduct_id'])


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
            'Meta': {'object_name': 'Genre'},
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        },
        'apps.raiting': {
            'Meta': {'object_name': 'Raiting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '8', 'unique': 'True'})
        },
        'apps.serie': {
            'Meta': {'ordering': "['-number']", 'object_name': 'Serie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.SeriesGroup']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'apps.seriesgroup': {
            'Meta': {'ordering': "['-number']", 'object_name': 'SeriesGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['apps.Production']"})
        },
        'apps.status': {
            'Meta': {'object_name': 'Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True'})
        },
        'apps.thematicgroup': {
            'Meta': {'object_name': 'ThematicGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        }
    }

    complete_apps = ['apps']