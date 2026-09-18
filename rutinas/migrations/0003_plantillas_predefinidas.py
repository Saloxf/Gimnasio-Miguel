from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ejercicios", "0006_ejercicio_dataset_media"),
        ("rutinas", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlantillaRutina",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                ("objetivo", models.CharField(choices=[("ganancia_muscular", "Ganancia muscular"), ("fuerza", "Fuerza"), ("perdida_grasa", "Pérdida de grasa"), ("condicion_fisica", "Condición física"), ("mantenimiento", "Mantenimiento")], max_length=30)),
                ("descripcion", models.TextField(blank=True)),
                ("nivel", models.CharField(default="principiante", max_length=20)),
                ("dias_semana", models.PositiveSmallIntegerField(default=3)),
                ("activa", models.BooleanField(default=True)),
            ],
            options={"ordering": ["objetivo", "nombre"]},
        ),
        migrations.CreateModel(
            name="EjercicioDePlantilla",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("orden", models.PositiveIntegerField(default=1)),
                ("series_objetivo", models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1)])),
                ("repeticiones_objetivo", models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1)])),
                ("descanso_segundos", models.PositiveIntegerField(default=90)),
                ("ejercicio", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="ejercicios.ejercicio")),
                ("plantilla", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ejercicios", to="rutinas.plantillarutina")),
            ],
            options={"ordering": ["orden"]},
        ),
        migrations.AddConstraint(
            model_name="ejerciciodeplantilla",
            constraint=models.UniqueConstraint(fields=("plantilla", "ejercicio"), name="ejercicio_unico_por_plantilla"),
        ),
    ]
