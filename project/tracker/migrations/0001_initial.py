from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=100)),
                ('level', models.CharField(default='Beginner', max_length=20)),
                ('learning_date', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PracticeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_practiced', models.FloatField()),
                ('activity_description', models.CharField(max_length=500, null=True, blank=True)),
                ('practice_date', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practice_logs', to='tracker.skill')),
            ],
        ),
    ]
