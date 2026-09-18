from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ejercicios", "0006_ejercicio_dataset_media"),
        ("rutinas", "0003_plantillas_predefinidas"),
    ]

    operations = [
        migrations.AddField(
            model_name="plantillarutina",
            name="grupo_muscular",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="plantillas_rutina",
                to="ejercicios.grupomuscular",
            ),
        ),
    ]
