# Generated by Django 2.2.7 on 2019-12-12 08:31

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import web.utils


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_embeddable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=web.utils.now, editable=False)),
                ('updated_at', models.DateTimeField(default=web.utils.now, editable=False)),
                ('text', models.TextField()),
                ('embedding', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('embedding_type', models.IntegerField(blank=True, choices=[(0, 'TF_IDF'), (1, 'BERT')], null=True)),
                ('projection', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Source')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='notiondocument',
            name='title',
        ),
        migrations.DeleteModel(
            name='Embeddable',
        ),
    ]
