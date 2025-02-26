# Create your models here : myapp.models
from django.db import models
    
    
class Color(models.Model):
    color_name = models.CharField(max_length=50)
    def __str__(self):
        return str(self.color_name)    

class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    pcolor = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="persons", null=True, blank=True)

    def __str__(self):
        return str(self.name)
        

