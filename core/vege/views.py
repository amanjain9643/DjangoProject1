from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
# Create your views here.
def receipes(request):

    if request.method=="POST":
        data=request.POST
        receipe_image=request.FILES.get('receipe_image')
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
        print(receipe_name)
        print(receipe_description)
        print(receipe_image)

        Recipe.objects.create(
             recipe_name=receipe_name,
            recipe_description=receipe_description,
            recipe_image=receipe_image)
        
        return redirect('/receipes/')
    queryset=Recipe.objects.all()

    if request.GET.get('search'):
        queryset=queryset.filter(recipe_name__icontains=request.GET.get('search'))
    context={"receipes":queryset}
    return render(request,"receipes.html",context)


def home(request):
    return HttpResponse("i am good")

def delete_receipe(request,id):
    queryset=Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/receipes/')

def update_receipe(request,id):
    queryset=Recipe.objects.get(id=id)
    if request.method=='POST':
        data=request.POST
        receipe_image=request.FILES.get('receipe_image')
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')

        queryset.recipe_name=receipe_name,
        queryset.recipe_description=receipe_description
        if receipe_image:
            queryset.receipe_image=receipe_image
        queryset.save()
        return redirect('/receipes/')
    context={"receipe":queryset}
    return render(request,"update_receipes.html",context)
