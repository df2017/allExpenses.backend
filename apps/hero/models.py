from django.db import models
from django.contrib import admin


class Hero(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=(('M', 'Male'), ('F', 'Female')), default='F')
    movie = models.CharField(max_length=100)

    objects = models.Manager()

    def __unicode__(self):
        return self.name

class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'movie', 'gender')