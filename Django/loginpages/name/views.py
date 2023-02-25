from django.shortcuts import render,redirect
from .import views
from django.template import loader  
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from loginpages import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from .tokens import generate_token
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
# Create your views here.  
from django.http import HttpResponse  
# Create your views here.
def home(request):
    return render(request,"home.html")
def signup(request):
    if(request.method=="POST"):
        username=request.POST["username"]
        password1=request.POST["password1"]
        firstname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        Email=request.POST["Email"]
        password2=request.POST["password2"]
        
        if User.objects.filter(username=username):
            messages.error(request,"username already exists! please try another one")
            return redirect('home')

        
        if password1!=password2:
            messages.error(request,"passwords didnt match")
            return redirect('signup')
        info=User.objects.create_user(username,Email,password1)
        info.first_name=firstname
        info.last_name=lastname
        info.active=False
        info.save()
        messages.success(request,"Registered succesfully")
        #welcome email writing
        subject="welcome to IIT jodhpur"
        message="hello"+info.first_name+"thankyou for joining IIT jodhpur \n thanking you \n karanam preethi"
        from_email=settings.EMAIL_HOST_USER
        to_list=[info.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        
        #Email adress confirmation email
        #domain of the website
        current_site = get_current_site(request)
        subject2="confirm your email from IIT jodhpur"
        #dictionary
        message2=render_to_string('email_confirm.html',{
            'name':info.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(info.pk)),
            'token':generate_token.make_token(info)
        })
        #email object
        email=EmailMessage(
            subject2,
            message2,
            settings.EMAIL_HOST_USER,
            [info.email],
        )
        email.fail_silently=True
        email.send()
        return redirect("signin")
    return render(request,"signup.html")

def signin(request):
    if(request.method=="POST"):
        username=request.POST["username"]
        password1=request.POST["password1"]

        authen=authenticate(username=username,password=password1)
        print(username, password1)
        #if  not authenticate it will return none
        if authen is not None:
            login(request,authen)
            firstname=authen.first_name
            return render(request,"website.html",{'firstname':firstname,'authen':authen})
        else:
            messages.error(request,"signin failed due to bad credentials")
            return redirect('home')
    return render(request,"signin.html")
def website(request):
    if(request.method=="POST"):
        username=request.POST["username"]
        password1=request.POST["password1"]

    authen=authenticate(username=username,password1=password)
    return render(request,"website.html")

def signout(request):
    logout(request)
    messages.success(request,"logged out")
    return redirect('home')

def activate(request,uidb64):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        info=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        info=None
    if info is not None and generate_token.check_token(info,token):
        info.is_active=True
        info.save()
        login(request,info)
        return redirect('home')
    else:
        return render(request,"activation failed")
