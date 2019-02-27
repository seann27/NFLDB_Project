from django.db import models

# Create your models here.

class Teams(models.Model):
    city = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    color1 = models.CharField(max_length=200)
    color2 = models.CharField(max_length=200)
    logo_img = models.CharField(max_length=200)
    background_img = models.CharField(max_length=200)
    espn_link = models.CharField(max_length=400)

    def __str__(self):
        return (self.city+" "+self.name)
    class Meta:
        verbose_name_plural = "Teams"

class Players(models.Model):
    espnid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=10)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    image = models.CharField(max_length=200)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Players"