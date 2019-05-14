# Generated by Django 2.1.4 on 2019-05-13 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plugins', '0006_auto_20190308_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultPipingBoolParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField(null=True)),
                ('plugin_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boolean_piping_default', to='plugins.PluginParameter')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultPipingFloatParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(null=True)),
                ('plugin_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='float_piping_default', to='plugins.PluginParameter')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultPipingIntParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(null=True)),
                ('plugin_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='integer_piping_default', to='plugins.PluginParameter')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultPipingPathParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200, null=True)),
                ('plugin_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='path_piping_default', to='plugins.PluginParameter')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultPipingStrParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200, null=True)),
                ('plugin_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='string_piping_default', to='plugins.PluginParameter')),
            ],
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('locked', models.BooleanField(default=True)),
                ('authors', models.CharField(blank=True, max_length=200)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, max_length=800)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('category',),
            },
        ),
        migrations.CreateModel(
            name='PluginPiping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pipeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plugin_pipings', to='pipelines.Pipeline')),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plugins.Plugin')),
                ('previous', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next', to='pipelines.PluginPiping')),
            ],
            options={
                'ordering': ('pipeline',),
            },
        ),
        migrations.AddField(
            model_name='pipeline',
            name='plugins',
            field=models.ManyToManyField(related_name='pipelines', through='pipelines.PluginPiping', to='plugins.Plugin'),
        ),
        migrations.AddField(
            model_name='defaultpipingstrparameter',
            name='plugin_piping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='string_param', to='pipelines.PluginPiping'),
        ),
        migrations.AddField(
            model_name='defaultpipingpathparameter',
            name='plugin_piping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='path_param', to='pipelines.PluginPiping'),
        ),
        migrations.AddField(
            model_name='defaultpipingintparameter',
            name='plugin_piping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='integer_param', to='pipelines.PluginPiping'),
        ),
        migrations.AddField(
            model_name='defaultpipingfloatparameter',
            name='plugin_piping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='float_param', to='pipelines.PluginPiping'),
        ),
        migrations.AddField(
            model_name='defaultpipingboolparameter',
            name='plugin_piping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boolean_param', to='pipelines.PluginPiping'),
        ),
    ]
