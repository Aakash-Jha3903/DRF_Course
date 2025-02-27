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
    # pcolor = ColorSerializer(read_only=True)
    color_info = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = "__all__"
        # depth = 1

    def create(self, validated_data):  # Overridding the create() method, @GPT
        pcolor_data = validated_data.pop("pcolor", None)
        if pcolor_data: 
            color_instance, _ = Color.objects.get_or_create(**pcolor_data)
        else:
            color_instance = None
        person = Person.objects.create(pcolor=color_instance, **validated_data)
        return person

    def get_color_info(self,obj):   # get_  prefix
        if obj.pcolor:
            return {"id": obj.pcolor.id, "color_name": obj.pcolor.color_name}
        return None

    def validate(self, data):
        speacial_character = "!@#$%^&*()+=;<=>?-/\''._`|~"
        if any(char in speacial_character for char in data['name']):
            raise serializers.ValidationError("Person name should not contain any special characters")
        
        if data['age'] < 0:
            raise serializers.ValidationError("Age should be greater than zero")
        return data
