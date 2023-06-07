from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.core.validators import EmailValidator
# Create your views here.
def register_view(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
        
            if password1 != password2:
                error_message = "Passwords do not match."
                return render(request, 'users/register.html', {'error_message': error_message})
            
            
            email_validator = EmailValidator()
            try:
                email_validator(email)
            except ValidationError:
                error_message = "Invalid email format."
    
        
                return render(request, 'users/register.html', {'error_message': error_message})
            
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
        

            
            # Customize the logic for successful registration as needed
            return redirect('login')  # Replace 'home' with the appropriate URL name for your home page
                          
        return render(request,'users/register.html')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Customize the logic for successful login as needed
            return redirect('home')  # Replace 'home' with the appropriate URL name for your home page
        else:
            error_message = "Invalid username or password."
            return render(request, 'users/login.html', {'error_message': error_message})
    
    return render(request, 'users/login.html')    

def logout_view(request):
    logout(request)
    # Customize the logic for successful logout as needed
    return redirect('home')  # Replace 'home' with the appropriate URL name for your home page
