from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import New


# Create your views here.
def home(request):
    if request.method == "POST":
        add = request.POST['add']
        usr = request.user
        new = New(todo=add, user=usr)
        new.save()
        messages.success(request, ('todo added successfully '))
        return redirect('view')

    else:
        return render(request, 'home.html', {})


def view(request):
    obj = New.objects.filter(user=request.user)
    return render(request, 'view.html', {'object': obj})


def edit(request, pk):
    obj = New.objects.get(id=pk)
    if request.method == 'POST':
        obj.todo = request.POST['edit']
        obj.save()
        messages.success(request, ('todo edited successfully '))
        return redirect('view')
    else:
        return render(request, 'edit.html', {'object':obj})


def delete(request, pk):
    obj = get_object_or_404(New, id=pk)
    obj.delete()
    return redirect('view')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('login successful'))
            return redirect('home')
        else:
            messages.success(request, ('invalid details .try signing up if you dont have an account'))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        usernames = [user.username for user in User.objects.all()]
        emails = [user.email for user in User.objects.all()]
        if password1 == password2:

            if email in emails:
                messages.success(request, ('user already exist. sign in instead'))
                return redirect('login')

            elif username in usernames:
                messages.success(request, ('username already taken. try something else'))
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, last_name=last_name, first_name=first_name, email=email, password=password1)
                user.save()
                user = authenticate(request, username=username, password=password1)
                login(request, user)
                messages.success(request, ('sign-up successful'))
                return redirect('home')
        else:
            messages.success(request, ('invalid details'))
            return redirect('register')

    else:
        return render(request, 'register.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ('logout successful'))
    return redirect('home')

