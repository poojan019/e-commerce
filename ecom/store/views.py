from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignUpForm
from .models import Product, Category

def product(request, pk):
    product = Product.objects.get(id=pk)

    return render(request, 'product.html', {'product': product})

def category(request, cat):
    cat = cat.replace('-', ' ')
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, ("That category does not exist."))
        return redirect('home')
    

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Logged In successfully !!!"))
            return redirect('home')
        else:
            messages.success(request, ("Error logging in! Try again!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out successfully !!!"))

    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Log In user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Register successfully !!!"))
            return redirect('home')
        else:
            messages(request, ("Error registering form !!!"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
