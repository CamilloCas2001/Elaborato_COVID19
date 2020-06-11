from django.db import models

# Create your models here.


class Italia(models.Model):
    data = models.CharField(max_length=25)
    stato = models.CharField(max_length=5)
    ricoverati_con_sintomi = models.IntegerField()
    terapia_intensiva = models.IntegerField()
    totale_ospedalizzati = models.IntegerField()
    isolamento_domiciliare = models.IntegerField()
    totale_positivi = models.IntegerField()
    variazione_totale_positivi = models.IntegerField()
    nuovi_positivi = models.IntegerField()
    dimessi_guariti = models.IntegerField()
    deceduti = models.IntegerField()
    totale_casi = models.IntegerField()
    tamponi = models.IntegerField()