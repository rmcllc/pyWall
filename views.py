from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User, Message, Comment

def index(request):
    return render(request, 'login.html')

def registerUser(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()    
        print(pw_hash)
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        
        request.session['userid'] = user.id
    return redirect('/myWall')

def validateUser(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/myWall')
        return redirect('/')

def myWall(request):
    context = {
    'userInfo': User.objects.get(id=request.session['userid']),
    'allPosts': Message.objects.all(),
    }


    return render(request, 'index.html', context)

def newPost(request):
    errors = Message.objects.message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/myWall')
    else:
        Message.objects.create(user_id=User.objects.get(id=request.session['userid']) ,post=request.POST['newMessage'])


    return redirect('/myWall')

def delete_session(request):
    try:
        del request.session['userid']
    except KeyError:
        print("Can't Delete from session")
        
    return redirect('/')