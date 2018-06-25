from django.db import models


class Applicants(models.Model):
    option = models.CharField(db_index = True, max_length=256, help_text='Opción de decarga [Nombre o RUN]')
    rut = models.CharField(db_index = True, blank=True, null=True, max_length=256, help_text='RUN en caso de tenerlo')
    dniID = models.CharField(db_index = True, blank=True, null=True, max_length=256, help_text='Número de Pasaporte')
    names = models.CharField(db_index = True, blank=True, null=True, max_length=256, help_text='Nombres [Escribir como aparece en documento de identidad]')
    surname1 = models.CharField(db_index = True, blank=True, null=True, max_length=256, help_text='Apellido paterno')
    surname2 = models.CharField(db_index = True, blank=True, null=True, max_length=256, help_text='Apellido materno')
    fechaNas = models.DateField(db_index = True, blank=True, null=True, help_text='Fecha de nacimiento')
    idPaisOrigen = models.CharField(db_index = True, blank=True, null=True, max_length=256, help_text='País de origen')
    email = models.EmailField(db_index = True, max_length=256, blank=True, null=True, help_text='Email donde será notificado')
    active = models.BooleanField(default=True, help_text='Indica si esta en proceso activo')

    def __str__(self):
        return '%s %s %s %s %s' % (self.names, self.surname1, self.surname2, self.dniID, self.rut)
