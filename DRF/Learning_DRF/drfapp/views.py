# Create your views here : myapp/views.py 
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


from . models import Person
from .serializers import PersonSerializer, UserLoginSerializer

@api_view(["GET","POST","DELETE",])
def index(request):
    courses = {
        "course_name": "Python ",
        "learn": ["Django","DRF","React.js"]       
    }
    if request.method == "GET":
        data = request.GET.get('search')
        print(data)
        print("You hit a get method")
        return Response(courses)        
    elif request.method == "POST":
        data = request.data
        print(data)
        print("You hit a POST method")
        return Response()        
        
    return Response()
    # return HttpResponse(request, "<h1> yo </h1>")
    
    
@api_view(["POST"])
def user_login(request):
    serializer = UserLoginSerializer(data = request.data)
    if serializer.is_valid():
        data = serializer.data
        return Response({"message":f"success and the data is : {data}"})
    return Response(serializer.errors)

class PersonAPI(APIView):
    def get(self,request):
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
    
    
    
    
#1:20:00
from rest_framework import viewsets
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    
    def list(self, request): 
        search = request.GET.get("search")
        if search:
            queryset = self.queryset.filter(name__startswith=search)
        serializers = PersonSerializer(queryset,many=True)
        return Response({"status":200,"data":serializers.data})    
    
    
    
    
    