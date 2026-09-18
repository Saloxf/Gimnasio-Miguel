from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ejercicios", "0005_ejercicio_nombre_original"),
    ]

    operations = [
        migrations.AddField(
            model_name="ejercicio",
            name="dataset_id",
            field=models.CharField(blank=True, db_index=True, max_length=20),
        ),
        migrations.AddField(
            model_name="ejercicio",
            name="gif_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="ejercicio",
            name="imagen_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="ejercicio",
            name="objetivo",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="ejercicio",
            name="parte_cuerpo",
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
