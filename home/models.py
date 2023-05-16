from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


OCUPACION_OPCIONES = [
    ('empleado','Empleado'),
    ('independiente','Independiente'),
    ('pensionado','Pensionado'),
    ('ama_casa','Ama de casa'),
    ('estudiante','Estudiante'),
]

FRECUENCIA_ACTIVIDAD_FISICA_OPCIONES = [
    ('diario','Diario'),
    ('menor_tres_veces_semana','Menos de 3 días por semana'),
    ('tres_veces_semana','3 días por semana'),
    ('mayor_tres_veces_semana','Más de 3 días por semana'),
    ('una_vez_semana','Un día por semana'),
    ('no','No aplica'),
]

TEST_RESPONSE_TYPE = [
    ('text','Campo tipo texto'),
    ('bool','Campo positivo o negativo'),
]

class Diagnostico(models.Model):
    code = models.CharField('Código', max_length=20)
    description = models.CharField('Descripción', max_length=200)
    created_at = models.DateField('Fecha de creación', auto_now_add=True)
    is_active = models.BooleanField('Activo', default=True)
    
    """
    foranea a diagnostico
    
    cie-10 tabla nacional de diagnosticos para pacientes. estandariza
    
    codigo
    descripcion
    cresated_at
    activo bool mostrar solo activos
    str codigo-descrpcion
    """
    
    def __str__(self):
        return f"{self.code} - {self.description}"
    
    class Meta:
        verbose_name = 'Diagnóstico médico'
        verbose_name_plural = 'Diagnósticos médicos'

class Paciente(models.Model):
    cedula = models.CharField('Cédula', max_length=10, primary_key=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=120)
    fecha_nacimiento = models.DateField('Fecha de nacimiento')
    edad = models.IntegerField(default=0, editable=False)
    telefono = models.CharField('Teléfono', max_length=15)
    email = models.EmailField(blank=True, null=True)
    acompanante = models.CharField('Nombre del acompañante', max_length=120, blank=True, null=True)
    parentesco = models.CharField(max_length=60, blank=True, null=True)
    telefono_acompanante = models.CharField('Teléfono del acompañante', max_length=15, blank=True, null=True)
    ocupacion = models.CharField('Ocupación', max_length=60, choices = OCUPACION_OPCIONES)
    profesion = models.CharField('Profesión', max_length=120, blank=True, null=True)
    seguridad_social = models.CharField(max_length=240)
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, verbose_name='Diagnóstico médico')
    motivo_consulta = models.TextField('Motivo de consulta')
    cronologia_de_patologia = models.TextField('Cronología de la patología')
    actividad_fisica = models.BooleanField('Actividad física', default = False)
    tipo_actividad_fisica = models.CharField('Tipo de actividad física', max_length=240, blank=True, null=True)
    frecuencia_actividad_fisica = models.CharField('Frecuencia de la actividad física', max_length=60, choices = FRECUENCIA_ACTIVIDAD_FISICA_OPCIONES, default = 'no')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
    conclusion  = models.TextField('Conclusión', null=True, blank=True)

    def get_edad(self):
        age = datetime.now().date() - (self.fecha_nacimiento + timedelta(days = +7))
        self.edad = age.days/365

    def get_cedula(self):
        return self.cedula

    def user_directory_path(instance, filename):
        return 'paciente_{0}/{1}'.format(instance.get_cedula(), filename)

    adjuntar_documento = models.FileField(upload_to=user_directory_path, blank=True, null=True)


    def __str__(self):
        return f'{self.nombre} - {self.cedula}'

    def save(self, *args, **kwargs):
        self.get_edad()
        super(Paciente, self).save(*args, **kwargs)

class Evolucion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    evolucion = models.TextField('Evolución')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Fecha de creación')

    def __str__(self):
        return f"{self.paciente} - {timezone.localtime(self.created_at).strftime('%Y/%m/%d - %H:%M')}"

    class Meta:
        verbose_name = "Evolución"
        verbose_name_plural = "Evoluciones"

class Categoria(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.nombre}'
    
    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

class Test(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True,null=True)
    categoria = models.ForeignKey(Categoria, on_delete = models.CASCADE)
    subcategoria = models.CharField(max_length=120)
    tipo_resultado = models.CharField(max_length=60, choices = TEST_RESPONSE_TYPE, default = 'bool')

    def __str__(self):
        return f'{self.categoria} - {self.subcategoria} - {self.nombre}'

class PacienteTest(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    test = models.ForeignKey(Test, on_delete = models.CASCADE)
    resultado = models.TextField()

    def __str__(self):
        return f'{self.test} - {self.resultado}'


class Person(models.Model):
    name = models.CharField(max_length=128)


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through="Membership")


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
    
class Image(models.Model):
    image = models.ImageField(upload_to="images")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class Product(models.Model):
    name = models.CharField(max_length=100)