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



# 1:31:08 - Token Authentication in DRF ---------------------------------------------
from django.contrib.auth.models import User
class RegiterSerizlizer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50)

    def create(self,validated_data):
        user = User.objects.create_user(username=validated_data["username"],email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        # print(user)  #Aakash Jha7 <= username
        # print(validated_data) #{'username': 'Aakash Jha7', 'email': 'aj7@gmail.com', 'password': '1234'}

        return user # return validated_data,  DONO HI KAM KAR RAHE HAI !!


    def validate(self, data):
        if data["username"]:
            if User.objects.filter(username=data["username"]).exists(): 
                raise serializers.ValidationError("User already exists, with this username !")
        if data["email"]:
            if User.objects.filter(email=data["email"]).exists(): 
                raise serializers.ValidationError("User already exists, with this Email !")
        return data