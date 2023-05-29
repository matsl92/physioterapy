from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


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

class Diagnosis(models.Model):
    diagnosis_code = models.CharField('código', max_length=20)
    diagnosis_description = models.CharField('descripción', max_length=200)
    created_at = models.DateField('fecha de creación', auto_now_add=True)
    is_active = models.BooleanField('activo', default=True)
    
    """
    foranea a diagnosiso
    activo bool mostrar solo activos
    """
    
    def __str__(self):
        return f"{self.diagnosis_code} - {self.diagnosis_description}"
    
    class Meta:
        verbose_name = 'Diagnóstico médico'
        verbose_name_plural = 'Diagnósticos médicos'

class Patient(models.Model):
    cedula = models.CharField('cédula', max_length=10, primary_key=True)
    fecha_ingreso = models.DateTimeField('fecha de ingreso', auto_now_add=True)
    nombre = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=120)
    fecha_nacimiento = models.DateField('fecha de nacimiento')
    edad = models.IntegerField(default=0, editable=False)
    telefono = models.CharField('teléfono', max_length=15)
    email = models.EmailField(blank=True, null=True)
    acompanante = models.CharField('nombre del acompañante', max_length=120, blank=True, null=True)
    parentesco = models.CharField(max_length=60, blank=True, null=True)
    telefono_acompanante = models.CharField('teléfono del acompañante', max_length=15, blank=True, null=True)
    ocupacion = models.CharField('ocupación', max_length=60, choices = OCUPACION_OPCIONES)
    profesion = models.CharField('profesión', max_length=120, blank=True, null=True)
    seguridad_social = models.CharField(max_length=240)
    diagnosiso = models.ForeignKey(Diagnosis, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, verbose_name='diagnóstico médico')
    motivo_consulta = models.TextField('motivo de consulta')
    cronologia_de_patologia = models.TextField('cronología de la patología')
    actividad_fisica = models.BooleanField('actividad física', default = False)
    tipo_actividad_fisica = models.CharField('tipo de actividad física', max_length=240, blank=True, null=True)
    frecuencia_actividad_fisica = models.CharField('frecuencia de la actividad física', max_length=60, choices = FRECUENCIA_ACTIVIDAD_FISICA_OPCIONES, default = 'no')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
    conclusion  = models.TextField('conclusión', null=True, blank=True)

    def get_edad(self):
        age = datetime.now().date() - (self.fecha_nacimiento + timedelta(days = +7))
        self.edad = age.days/365

    def get_cedula(self):
        return self.cedula

    def user_directory_path(instance, filename):
        return 'paciente_{0}/{1}'.format(instance.get_cedula(), filename)

    documento_adjunto = models.FileField('Adjuntar documento', upload_to=user_directory_path, blank=True, null=True)


    def __str__(self):
        return f'{self.nombre} - {self.cedula}'

    def save(self, *args, **kwargs):
        self.get_edad()
        super(Patient, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

class Evolution(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE, verbose_name='Paciente')
    evolution_record = models.TextField('Evolución')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Fecha de creación')

    def __str__(self):
        return f"{self.patient} - {timezone.localtime(self.created_at).strftime('%Y/%m/%d - %I:%M %p')}"

    class Meta:
        verbose_name = "Evolución"
        verbose_name_plural = "Evoluciones"

class Category(models.Model):
    category_name = models.CharField('nombre',max_length=120)

    def __str__(self):
        return f'{self.category_name}'
    
    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'

class Test(models.Model):
    test_name = models.CharField('nombre', max_length=120)
    test_description = models.TextField('descripción', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name='categoría')
    subcategory = models.CharField('subcategoría', max_length=120)
    result_type = models.CharField('tipo de resultado', max_length=60, choices = TEST_RESPONSE_TYPE, default = 'bool')

    def __str__(self):
        return f'{self.category} - {self.subcategory} - {self.test_name}'

class PatientTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE, verbose_name='paciente')
    test = models.ForeignKey(Test, on_delete = models.CASCADE)
    result = models.TextField('resultado')

    def __str__(self):
        return f'{self.test} - {self.result}'
    
    class Meta:
        verbose_name = 'test de paciente'
        verbose_name_plural = 'tests de pacientes'

