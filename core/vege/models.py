from django.db import models

from django.contrib.auth.models import User
# Create your models here.




class Recipe(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    recipe_name=models.CharField(max_length=100)
    recipe_description=models.TextField()
    recipe_image=models.ImageField(upload_to="receipe/")
    
    def __str__(self):
        return "recipe_name"+self.recipe_name+"recipe_description"+self.recipe_description