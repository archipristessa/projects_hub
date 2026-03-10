from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_alter_profilestudent_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilestudent',
            name='course',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, '1 курс'), (2, '2 курс'), (3, '3 курс'), (4, '4 курс'), (5, '5 курс'), (6, '6 курс')], null=True, verbose_name='Курс'),
        ),
    ]