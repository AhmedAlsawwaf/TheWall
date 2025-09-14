from django.shortcuts import render,redirect
from .models import User,Message,Comment
from django.contrib import messages
import bcrypt
from django.urls import reverse
# Create your views here.
def index (request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.validate_registration(request.POST)
        if errors:
            return render(request,'index.html',{'reg_errors': errors,'reg_values': request.POST.dict(),})
        else:
            password = request.POST.get('password')
            hashedPassword = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        User.objects.create(first_name = request.POST.get('first_name'),
                            last_name = request.POST.get('last_name'),
                            email = request.POST.get('email'),
                            password = hashedPassword)
        request.session['first_name'] = request.POST.get('first_name')
        messages.success(request,'successfully create user')
        return redirect(reverse('wall:main'))
    return render(request, 'index.html')

def login(request):
    if request.method != 'POST':
        return redirect(reverse('wall:main'))
    errors = User.objects.validate_login(request.POST)
    if request.method == 'POST':
        if errors:
            return render(request,'index.html',{'login_errors': errors,'login_values': request.POST.dict()})
        else:    
            user = User.objects.filter(email=request.POST['email']).first()
            if not user or not bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):    
                return redirect(reverse('wall:main'))
            else:
                request.session['user_logged_in'] = user.id
                messages.success(request,'successfully Logged in')
                return redirect('wall:view_wall')

def view_wall(request):
    user = User.objects.get(id = request.session.get('user_logged_in'))
    posts = Message.objects.all().order_by('-created_at')
    context={
        'user':user,
        'post':posts
    }
    return render(request,'wall.html',context)

def create_message(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        
        text = request.POST.get('post_message')
        Message.objects.create(user=user, message=text)
    return redirect(reverse('wall:view_wall'))

def create_comment(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        
        post_id = request.POST.get('message_id')
        post = Message.objects.get(id=post_id)
        
        text = request.POST.get('comment')
        Comment.objects.create(comment= text, user= user,message =post)
    return redirect(reverse('wall:view_wall'))

def logout(request):
    if request.method == 'POST':
        request.session.flush()
        return redirect('wall:main')