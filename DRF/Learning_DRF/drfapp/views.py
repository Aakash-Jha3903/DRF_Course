# Create your views here : myapp/views.py 
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


from . models import Person
from .serializers import PersonSerializer, UserLoginSerializer, RegiterSerizlizer

@api_view(["GET","POST",])
def index(request):
    courses = {
        "course_name": "Python ",
        "learn": ["Django","DRF","React.js"]       
    }
    if request.method == "GET":
        data = request.GET.get('search')
        print(data)
        print("You hit a GET method")
        return Response(courses)        
    if request.method == "POST":
        data = request.data
        print(data)
        print("You hit a POST method")
        return Response()        
        
    return Response()

    
@api_view(["POST"])
def user_login(request):
    serializer = UserLoginSerializer(data = request.data)  # "data=" likhna jaruri hai, so that we can use the identifier.data i.e.,  serializer.data 
    print(f"before login, .is_valid() **********************:\n {serializer}")
    # print(f"before login, serializer.data.email  **********************:\n {serializer.data.get("email") }")
    print(f"before login, serializer..is_valid()  **********************:\n {serializer.is_valid()}")

    if serializer.is_valid():
        data = serializer.data  # dict. mai convert ho gaya ==> {'email': 'aj7@gmail.com', 'password': '1234'}
        print(f"before login, serializer.data  **********************:\n {serializer.data}")
        return Response({"message":f"success and the data is : {data}"})
    return Response(serializer.errors)

# 1:50:45 - Permissions(login-user or Anonymous-user) in DRF ------------------------------------------------------------------------------------------
from rest_framework.authentication import TokenAuthentication, BaseAuthentication  #SessionAuthentication  #1:50:45 - Permissions(login or not) in DRF 
from rest_framework.permissions import IsAuthenticated  #1:50:45 - Permissions(login or not) in DRF 

class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        print(request.user)   # tells, which user is logined
        return Response({"message":"This is a get-method"})
    
    def post(self,request):
        return Response({"message":"This is a post-method"})
    
    def put(self,request):
        return Response({"message":"This is a put-method"})
    
    def patch(self,request):
        return Response({"message":"This is a patch-method"})
    
    def delete(self,request):
        return Response({"message":"This is a delete-method"})
    
    
@api_view(['GET',"POST","PUT","PATCH","DELETE"])
def person(request):
    if request.method == "GET":
        # objs = Person.objects.all()
        objs = Person.objects.filter(pcolor__isnull=False)
        
        # print("objs : ",objs)
        serializer = PersonSerializer(objs, many=True) # if more than one object 
        # print(f"serializer : {serializer}")
        # print(f"serializer data : {serializer.data}")
                
        # for i in Person.objects.all():
        #     if i.name == "aj":
        #         i.name = "b"
        #         i.save()
        #         break
        
        return Response(serializer.data)
        
    elif request.method == "POST":
        print("**** POST method ***** ")
        data = request.data 
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            print("Data saved successfully using the post method ")
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == "PUT": 
        """ It is used to update the data 
        Its does not supports 'Partial' update method, so we need to give all data for update and it will updates all the fields of a Model-Class  """
        print("**** PUT method ***** ")
        data = request.data 
        serializer = PersonSerializer(data=data)

        if serializer.is_valid():
            new_name = serializer.validated_data.get("name")

        # Check if the new name already exists in the entire database (not just where name="z")
        if Person.objects.filter(name=new_name).exists():
            print("(PUT): Data already exists, not saving")  
            return Response({"message": "Person with this name already exists."}, status=400)
        else:
            serializer.save()  # Save the new record
            print("Data saved successfully using the PUT method ")
            return Response(serializer.data)  # Return saved data

    
    elif request.method == 'PATCH': 
        '''It is used to update the data 
        Its supports 'Partial' update of the fields '''
        print("**** Patch method ***** ")
        data = request.data     
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data = data, partial=True)  # is "obj" is not passed then new object is created !!
        if serializer.is_valid() and serializer.validate(data):
            serializer.save()  # passed data is updated 
            print("Data saved successfully using the PATCH method ")
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == "DELETE":
        print("**** DELETE method ***** ")
        data = request.data
        try:
            obj = get_object_or_404(Person, id=data['id'])  # Returns 404 if not found
            obj.delete()
            print("Data deleted successfully using the DELETE method ")
            return Response({"message": f"Data deleted successfully with id={data['id']}"}, status=200)
        except Exception as e:
            return Response({"message": f"Data not found . Error : {e}"}, status=404)
    
    
    
    
#1:20:00 => ModelViewSet and status in DRF 
from rest_framework import viewsets
from rest_framework import status
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    
    def list(self, request): 
        search = request.GET.get("search")
        queryset = Person.objects.all()
        
        http_method_name = ["GET", "POST"]  # now ModelViewSet allows to these http methods only    
        
        # usr = UserLoginSerializer.objects.all()
        if search:
            queryset = self.queryset.filter(name__startswith=search)
            serializers = PersonSerializer(queryset,many=True)
            # return Response({"status":200,"data":serializers.data})    
            return Response({"status":200,"data":serializers.data},status=status.HTTP_200_OK)    
        return Response({"message":"Search data is not passed in request"})    
        # if usr:
        #     usr_serializers = UserLoginSerializer(usr,many=True)
        #     return Response({"status":200,"data":usr_serializers.data},status=status.HTTP_200_OK)    


    # 2:00:52 - Actions in Django rest framework  ----------------------------------------------------------------------------------
    from rest_framework.decorators import action
    '''     (1) This "Action-Viewset" is a class based-"method"
            (2) decorator is used, with specific HTTP methods
            (3) to call this method, we dont need to specify any specific url in the urls.py !!
            (4) we can call this method via this url : api/people/97-59-29/send_mail_to_person/
            (5) set "details=True", when we recieve something like "pid or slug" from the user
    '''
    @action(detail=True, methods=["POST"])
    def send_mail_to_person_withSlug(self, request, pk=None):
        person_obj = Person.objects.get(pk=pk)
        if not person_obj:
            return Response({"status":False, "message": f"With-slug method ; Person with id {pk} not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = PersonSerializer(person_obj) 
        return Response({'status': True, 'message': f"WITH-SLUG={pk} and serializer.data =>> {serializer.data}"})

    
    @action(detail=False, methods=["POST"])
    def send_mail_to_person(self, request):
        return Response({'status': True, 'message': f"Email sent successfully, With-OUT slug"})



    
# 1:31:08 - Token Authentication in DRF -----------------------------------------------------------------------------------------------
from django.contrib.auth.models import User

class RegisterAPI(APIView):
    def post(self,request):
        data = request.data 
        serializer = RegiterSerizlizer(data=data)
        if not serializer.is_valid():
            return Response({"status":False, "message": serializer.errors},status= status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"status": True, "message": f"User [{data["username"]}] Registered successfully"},status= status.HTTP_201_CREATED)


from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializers = UserLoginSerializer(data=data)
        if not serializers.is_valid():
            return Response({"status":False, "message": serializers.errors},status=status.HTTP_400_BAD_REQUEST)
        usr = authenticate(username=data["username"], password=data["password"])
        
        token,_ = Token.objects.get_or_create(user=usr)
        return Response({"message":"Login Successfully","token":str(token)},status=status.HTTP_201_CREATED)


    
# 1:55:27 - Pagination in DRF  --------------------------------------------------------------------------------------------------------------------------------
from django.core.paginator import Paginator 

class CustomPagination(APIView):
    page_size = 10
    page_size_query_param = 'page_size'
    def get(self,request):
        objs = Person.objects.all()
        page = request.GET.get("page",1)
        page_size = 3   # per_page mai 3 data(dict.) hoga bass
        try :    
            paginator = Paginator(objs, page_size)
            serializers = PersonSerializer(paginator.page(page),many=True)
            return Response({"status":True,"data":serializers.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":False,"message":f"Invalid page or Error : {str(e)}"},status=status.HTTP_400_BAD_REQUEST)




    
        