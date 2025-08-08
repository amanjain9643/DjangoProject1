from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
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

@login_required(login_url='/delete-receipe/')
def delete_receipe(request,id):
    queryset=Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/receipes/')

@login_required(login_url='/update-receipe/')
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

def login_page(request):
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request,"INVALID USERNAME")
            return redirect('/login/')
        
        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,"INVALID  PASSWORD")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/receipes/')

            
    return render(request,"login.html")
def register_page(request):

    if request.method=='POST':
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,"USERNAME ALREADY EXISTS")
            return redirect("/register/")
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        messages.info(request,"ACCOUNT CREATED SUCCESFULLY")
        user.save()
        return redirect("/login/")
    return render(request,"register.html")

@login_required(login_url='/logout/')
def logout_page(request):
    logout(request)
    return redirect('/login')