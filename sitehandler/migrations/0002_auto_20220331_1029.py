# Generated by Django 3.0.4 on 2022-03-31 04:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sitehandler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctorname', models.CharField(max_length=50)),
                ('doctoremail', models.EmailField(max_length=50)),
                ('patientname', models.CharField(max_length=50)),
                ('patientemail', models.EmailField(max_length=50)),
                ('appointmentdate', models.DateField(max_length=10)),
                ('appointmenttime', models.TimeField(max_length=10)),
                ('symptoms', models.CharField(max_length=100)),
                ('status', models.BooleanField()),
                ('prescription', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=16)),
                ('gender', models.CharField(max_length=10)),
                ('phonenumber', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('birthdate', models.DateField()),
                ('bloodgroup', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Receptionist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=16)),
                ('gender', models.CharField(max_length=10)),
                ('phonenumber', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('birthdate', models.DateField()),
                ('bloodgroup', models.CharField(max_length=5)),
            ],
        ),
        migrations.AlterField(
            model_name='doctor',
            name='phonenumber',
            field=models.CharField(max_length=10),
        ),
    ]
