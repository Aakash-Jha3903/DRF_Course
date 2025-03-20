# Create your home app views here, home/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 

from .serializers import BlogSerializer
from .models import Blog

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

from django.core.paginator import Paginator

class PublicBlogView(APIView):
    
    def get(self,request):
        try :
            blogs = Blog.objects.all().order_by("?") # random order 
            if not blogs:
                return Response({"message":"No blogs found"}, status=status.HTTP_404_NOT_FOUND)

            page_number = request.GET.get('page',1)
            page_size = 2
            paginator = Paginator(blogs,page_size)  #http://127.0.0.1:8000/api/home/all_blogs/?page=4



            serializer = BlogSerializer(paginator.page(page_number),many=True)
            return Response({"Total data found":len(serializer.data),"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":f"Invalid page or Something went wrong, Error : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self,request):
        try :
            blogs = Blog.objects.filter(user=request.user)
            # print("request.user or request.user.username : ",request.user)  # aj3
            # print("request.user.id : ",request.user.id)     # 9 ********************************

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = Blog.objects.filter(Q(content__icontains=search) |  Q(title__icontains=search) | Q(user = search))

            if not blogs:
                return Response({"message":"No blogs found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = BlogSerializer(blogs,many=True)
            return Response({"Total data found":len(serializer.data),"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":f"Error : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
        
    def post(self, request):
        try :
            request.data["user"] = request.user.id  # Auto-assign user 
            # request.data["user"] = 9 # Kuch bhi dedo, bass exist karna chahiye so that it can take the "pk"
            data = request.data
            serializer = BlogSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            serializer.save()
            return Response({"message":"Blog Created Successfully","data":serializer.data}, status=201)
        except Exception as e:
            return Response({"message": f"An error occurred, during blog creation: {e}"}, status=500)

            
    def patch(self,request):
        try :
            # blog = Blog.objects.get(user=request.user, id=request.data.get('id'))
            blog = Blog.objects.filter(uuid=request.data.get('uuid'))

            if not blog.exists():
                return Response({"message":"Blog not found, or invalid 'uuid' ! "}, status=status.HTTP_404_NOT_FOUND)
            

            if request.user != blog[0].user :
            # if request.user != blog[0].user or not request.user.is_superuser:
                return Response({"request.user":str(request.user),
                                 "blog[0].user":str(blog[0].user),
                    "message":f"You({request.user}) are not authorized to update this blog"}, status=403)

            # serializer = BlogSerializer(blog, data=request.data, partial=True)
            serializer = BlogSerializer(blog[0],data=request.data, partial=True)

            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            serializer.save()
            return Response({"message":f"Blog Updated Successfully by {request.user}","data":serializer.data}, status=200)
        except Exception as e:
            return Response({"message": f"Blog not found or Error : {e}"}, status=404)

    def delete(self,request):
        try:
            blog = Blog.objects.filter(uuid=request.data.get('uuid'))
            if not blog.exists():
                return Response({"message":"Blog not found, or invalid 'uuid' ! "}, status=status.HTTP_404_NOT_FOUND)

            if request.user!= blog[0].user:
                return Response({"request.user":str(request.user),
                                 "blog[0].user":str(blog[0].user),
                    "message":f"You({request.user}) are not authorized to DELETE this blog"}, status=403)
            blog[0].delete()
            return Response({"message":f"Blog Deleted Successfully by {request.user}"}, status=200)
        except Exception as e:
            return Response({"message": f"Blog not found or Error : {e}"}, status=404)

            
            

        