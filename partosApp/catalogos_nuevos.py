from django.db import models

class CatalogoRegimenParto(models.Model):
    """
    Catálogo para Régimen durante el Trabajo de Parto
    Valores: CERO, LIQUIDO, COMUN, OTRO
    """
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'partosApp'
        db_table = 'catalogo_regimen_parto'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Régimen Parto'
        verbose_name_plural = 'Catálogo Regímenes Parto'

    def __str__(self):
        return self.descripcion


class CatalogoTipoRoturaMembrana(models.Model):
    """
    Catálogo para Tipo de Rotura de Membrana
    Valores: IOP, RAM, REM, RPM
    """
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'partosApp'
        db_table = 'catalogo_tipo_rotura_membrana'
        ordering = ['orden', 'descripcion']
        verbose_name = 'Catálogo Tipo Rotura Membrana'
        verbose_name_plural = 'Catálogo Tipos Rotura Membrana'

    def __str__(self):
        return self.descripcion
