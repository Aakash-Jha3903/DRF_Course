from rest_framework import serializers
from .models import Person, Color

class ColorSerializer(serializers.Serializer):
    class Meta:
        model = Color
        field = ["color_name","id"]
    

class PersonSerializer(serializers.ModelSerializer):
    pcolor = ColorSerializer()
    country = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = "__all__"
        # depth = 1
        
    def get_country(self,obj):
        return "Bharat"

    def validate(self, data):
        speacial_character = "!@#$%^&*()+=;<=>?-/\''._`|~"
        if any(char in speacial_character for char in data['name']):
            raise serializers.ValidationError("Person name should not contain any special characters")
        
        if data['age'] < 0:
            raise serializers.ValidationError(
                "Age should be greater than zero")
        return data
