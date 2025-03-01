
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog 

class BlogSerializer(serializers.ModelSerializer):  #Model !!
    class Meta:
        model = Blog
        exclude = ["created_at","updated_at"]
        
    