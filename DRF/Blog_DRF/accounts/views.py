# Create your accounts app views here, accounts/views.py
from rest_framework.response import Response
from rest_framework.views import APIView 
from .serializers import LoginSerializer, RegisterSerializer


class RegisterView(APIView):
    def post(self,request):
        try :
            data = request.data
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            serializer.save()    
            return Response({"message": f"Your account : '{data["username"]}', is created successfully ."}, status=201)
        except Exception as e :
            return Response({"message": f"An error occurred, during registration: {e}"}, status=500)

class LoginView(APIView):
    def post(self,request):
        try :
            data = request.data
            serializer = LoginSerializer(data = data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            response = serializer.get_jwt_token(serializer.data)
            return Response(response, status=200)
        except Exception as e:
            return Response({"message": f"An error occurred, during login: {e}"}, status=500)

