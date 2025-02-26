from rest_framework import serializers
from .models import Person, Color


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"
    

class PersonSerializer(serializers.ModelSerializer):
    pcolor = ColorSerializer()
    color_info = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = "__all__"
        depth = 1
        
    def get_color_info(self,obj):   # get_  prefix 
        color_obj = Color.objects.get(id=obj.pcolor.id)
        # return "Bharat"
        return {"color_name":color_obj.color_name,"hex":"#000"}

    def validate(self, data):
        speacial_character = "!@#$%^&*()+=;<=>?-/\''._`|~"
        if any(char in speacial_character for char in data['name']):
            raise serializers.ValidationError("Person name should not contain any special characters")
        
        if data['age'] < 0:
            raise serializers.ValidationError("Age should be greater than zero")
        return data
