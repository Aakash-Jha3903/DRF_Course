# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True #The model BaseModel is abstract, so it cannot be registered with admin.


class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to="blogs_images", blank=True)
    content = models.TextField()
    
    def __str__(self):
        return f"{str(self.title)} by {str(self.user.username)}"