# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CategoryGroup'
        db.create_table('myapp_categorygroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
        ))
        db.send_create_signal('myapp', ['CategoryGroup'])

        # Adding model 'Category'
        db.create_table('myapp_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(null=True, max_length=100, blank=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(null=True, max_length=100, blank=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.CategoryGroup'])),
        ))
        db.send_create_signal('myapp', ['Category'])

        # Adding model 'GenreGroup'
        db.create_table('myapp_genregroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.CategoryGroup'])),
        ))
        db.send_create_signal('myapp', ['GenreGroup'])

        # Adding model 'Genre'
        db.create_table('myapp_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.GenreGroup'])),
        ))
        db.send_create_signal('myapp', ['Genre'])

        # Adding model 'AltName'
        db.create_table('myapp_altname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal('myapp', ['AltName'])

        # Adding model 'Employ'
        db.create_table('myapp_employ', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
        ))
        db.send_create_signal('myapp', ['Employ'])

        # Adding model 'Creator'
        db.create_table('myapp_creator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('employ', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.Employ'])),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(null=True, max_length=100, blank=True)),
        ))
        db.send_create_signal('myapp', ['Creator'])

        # Adding model 'Hero'
        db.create_table('myapp_hero', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('actor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.Creator'])),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('is_main_hero', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('myapp', ['Hero'])

        # Adding model 'Product'
        db.create_table('myapp_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.Category'])),
        ))
        db.send_create_signal('myapp', ['Product'])

        # Adding M2M table for field alt_names on 'Product'
        m2m_table_name = db.shorten_name('myapp_product_alt_names')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['myapp.product'], null=False)),
            ('altname', models.ForeignKey(orm['myapp.altname'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'altname_id'])

        # Adding M2M table for field genres on 'Product'
        m2m_table_name = db.shorten_name('myapp_product_genres')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['myapp.product'], null=False)),
            ('genre', models.ForeignKey(orm['myapp.genre'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'genre_id'])

        # Adding M2M table for field creators on 'Product'
        m2m_table_name = db.shorten_name('myapp_product_creators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['myapp.product'], null=False)),
            ('creator', models.ForeignKey(orm['myapp.creator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'creator_id'])

        # Adding M2M table for field heroes on 'Product'
        m2m_table_name = db.shorten_name('myapp_product_heroes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['myapp.product'], null=False)),
            ('hero', models.ForeignKey(orm['myapp.hero'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'hero_id'])

        # Adding model 'Serie'
        db.create_table('myapp_serie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('num_season', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(null=True, max_length=255, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.Product'])),
        ))
        db.send_create_signal('myapp', ['Serie'])

        # Adding model 'Status'
        db.create_table('myapp_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, unique=True)),
        ))
        db.send_create_signal('myapp', ['Status'])

        # Adding model 'UserList'
        db.create_table('myapp_userlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('score', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.Status'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.Product'])),
        ))
        db.send_create_signal('myapp', ['UserList'])

        # Adding model 'SerieList'
        db.create_table('myapp_serielist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('serie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.Serie'])),
            ('user_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['myapp.UserList'])),
            ('like', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('myapp', ['SerieList'])


    def backwards(self, orm):
        # Deleting model 'CategoryGroup'
        db.delete_table('myapp_categorygroup')

        # Deleting model 'Category'
        db.delete_table('myapp_category')

        # Deleting model 'GenreGroup'
        db.delete_table('myapp_genregroup')

        # Deleting model 'Genre'
        db.delete_table('myapp_genre')

        # Deleting model 'AltName'
        db.delete_table('myapp_altname')

        # Deleting model 'Employ'
        db.delete_table('myapp_employ')

        # Deleting model 'Creator'
        db.delete_table('myapp_creator')

        # Deleting model 'Hero'
        db.delete_table('myapp_hero')

        # Deleting model 'Product'
        db.delete_table('myapp_product')

        # Removing M2M table for field alt_names on 'Product'
        db.delete_table(db.shorten_name('myapp_product_alt_names'))

        # Removing M2M table for field genres on 'Product'
        db.delete_table(db.shorten_name('myapp_product_genres'))

        # Removing M2M table for field creators on 'Product'
        db.delete_table(db.shorten_name('myapp_product_creators'))

        # Removing M2M table for field heroes on 'Product'
        db.delete_table(db.shorten_name('myapp_product_heroes'))

        # Deleting model 'Serie'
        db.delete_table('myapp_serie')

        # Deleting model 'Status'
        db.delete_table('myapp_status')

        # Deleting model 'UserList'
        db.delete_table('myapp_userlist')

        # Deleting model 'SerieList'
        db.delete_table('myapp_serielist')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'myapp.altname': {
            'Meta': {'object_name': 'AltName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        },
        'myapp.category': {
            'Meta': {'object_name': 'Category'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.CategoryGroup']"}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'})
        },
        'myapp.categorygroup': {
            'Meta': {'object_name': 'CategoryGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'})
        },
        'myapp.creator': {
            'Meta': {'object_name': 'Creator'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'max_length': '100', 'blank': 'True'}),
            'employ': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Employ']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'myapp.employ': {
            'Meta': {'object_name': 'Employ'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'})
        },
        'myapp.genre': {
            'Meta': {'object_name': 'Genre'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.GenreGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'})
        },
        'myapp.genregroup': {
            'Meta': {'object_name': 'GenreGroup'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.CategoryGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'})
        },
        'myapp.hero': {
            'Meta': {'object_name': 'Hero'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Creator']"}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_main_hero': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'myapp.product': {
            'Meta': {'object_name': 'Product'},
            'alt_names': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['myapp.AltName']", 'symmetrical': 'False'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Category']"}),
            'creators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['myapp.Creator']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['myapp.Genre']", 'symmetrical': 'False'}),
            'heroes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['myapp.Hero']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True'})
        },
        'myapp.serie': {
            'Meta': {'object_name': 'Serie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '255', 'blank': 'True'}),
            'num_season': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Product']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'myapp.serielist': {
            'Meta': {'object_name': 'SerieList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'serie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Serie']"}),
            'user_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.UserList']"})
        },
        'myapp.status': {
            'Meta': {'object_name': 'Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'unique': 'True'})
        },
        'myapp.userlist': {
            'Meta': {'object_name': 'UserList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Product']"}),
            'score': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['myapp.Status']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['myapp']