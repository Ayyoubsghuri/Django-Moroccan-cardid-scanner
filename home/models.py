from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

User = get_user_model()
# Create your models here.


class Type_Command(models.Model):
    TypeCommand = models.CharField(max_length=200, unique=True)
    Res = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    description = models.TextField(max_length=130, null=True, unique=False)
    add_on = models.DateTimeField(auto_now=True)

    @property
    def tslug(self, *args, **kwargs):
        r = slugify(self.TypeCommand)
        return r

    def __str__(self):
        return self.TypeCommand


class Cityonne(models.Model):
    CIN = models.CharField(max_length=15, unique=True)

    nom = models.CharField(max_length=40, default="none")
    nom_ar = models.CharField(max_length=40, default="none")

    prenom = models.CharField(max_length=40, unique=False)
    prenom_ar = models.CharField(max_length=40, default="none")

    add_on = models.DateTimeField(auto_now=True)
    datenaissance = models.DateField()
    adresse_now = models.CharField(max_length=160)
    adresse_now_ar=models.CharField(max_length=160, default="none")
    
    sexe = models.CharField(max_length=10)
    etat_civil = models.CharField(max_length=10)

    file_de = models.CharField(max_length=30, default="none")
    file_de_ar = models.CharField(max_length=30, default="none")

    et_de = models.CharField(max_length=30, default="none")
    et_de_ar = models.CharField(max_length=30, default="none")

    adresse_back = models.CharField(max_length=40, default="none")
    adresse_back_ar = models.CharField(max_length=40, default="none")

    Verified_Information = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, default="none")

    def __str__(self):
        return self.CIN


class Demande(models.Model):
    CIN = models.ForeignKey(
        Cityonne, on_delete=models.SET_NULL, null=True, unique=False, blank=True)
    Res = models.ForeignKey(
        User, unique=False, on_delete=models.CASCADE, default="Null")
    TypeCommand = models.ForeignKey(Type_Command, null=True, on_delete=models.SET_NULL,
                                    related_name='TypeCmd', db_constraint=False, blank=True)
    add_on = models.DateTimeField(auto_now=True)
    Done = models.BooleanField(null=True, default=False)

    class Meta:
        ordering = ["-add_on"]



