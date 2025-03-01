# Register your models here.``
from django.contrib import admin
from . models import Blog 
# admin.site.register(BaseModel)  # The model BaseModel is abstract, so it cannot be registered with admin.
admin.site.register(Blog)