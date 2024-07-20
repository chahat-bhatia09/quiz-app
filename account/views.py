from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            # messages.info(request, message="You are already logged in")
            return redirect("index")
        return render(request, template_name="account/login.html") #If user is not logged in render login.html

    def post(self, request):
        uname = request.POST.get("username", "") #get post data
        passwd = request.POST.get("password", "")
        user = authenticate(username=uname, password=passwd) #check if it matches
        if user is not None: #not none means user found
            login(request, user) #log them in and display success message
            messages.success(request, message="You have logged in successfully")
            request.session.set_expiry(300)
            if user.is_staff:  # Check if the user is an admin
                return redirect("controls")
            else:
                return redirect("index") #normal user is redirected to home page
        else:
            messages.warning(request, message="Either username or password is incorrect") #if user not found
        return render(request, template_name="account/login.html")





@method_decorator(login_required, name="dispatch")
class Logout(View):
    def get(self, request):
        return render(request, template_name='account/logout_confirmation.html')

    def post(self, request):
        if request.POST.get('confirm_logout') == 'yes': #check button response
            logout(request)
            messages.success(request, message="You have logged out successfully.")
            return redirect("login")
        else:
            # messages.info(request, message="Logout canceled.")
            return redirect("index")



class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            # messages.info(request, message="You are already logged in")
            return redirect("index")
        return render(request, template_name="account/register.html")

    def post(self, request):
        uname = request.POST.get("username", "")
        passwd = request.POST.get("password", "")
        user = User.objects.filter(username=uname).first() #checks if same name exists, and returns a query set of the same username
        #if it exists then returns the name but if is found to be none means this username is available
        if user is None: #procedd if username is available
            user = User(username=uname)
            user.set_password(passwd)
            user.save() #save the user
            login(request, user) #log them in
            messages.success(request,message="New user successfully created")
            return redirect("index")
        else:
            messages.info(request, message="This username is taken please choose another username")
            return redirect("register")
