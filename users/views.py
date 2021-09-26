from users.signals import profileCreate
from users.models import Profile
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, MessageForm, ProfileForm, SkillForm
from .utils import searchProfiles, paginateProfiles

def users(request):
    profiles , search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {'profiles':profiles, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'users/profiles.html', context)

def singleProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile':profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/single profile.html', context)

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        
        else:
            messages.error(request, 'Wrong username or password')
    
    return render(request, 'users/login_register.html')


def logoutUser(request):
    messages.info(request, 'User logged out')
    logout(request)
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save() 

            messages.success(request, 'User created successfully')
            login(request, user)
            return redirect('edit profile')

        else:
            messages.error(request, 'An error has occurred')

    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)
    
@login_required(login_url='login')  
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()

    context = {'profile':profile, 'skills':skills}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')  
def editProfile(request):
    profile = request.user.profile

    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request, 'users/edit profile.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/create skill.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):

    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('account')
            
    context = {'form' : form}

    return render(request, 'users/update skill.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    
    if request.method == 'POST':
        skill.delete()
        return redirect('account')


    context = {'object':skill}

    return render(request, 'delete template.html',context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    allMessages = profile.messages.all()
    messageCount = allMessages.count()
    unreadMessages = profile.messages.filter(is_read=False).count()
    context = {'allMessages':allMessages, 'messageCount':messageCount, 'unreadMessages':unreadMessages}

    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request, 'users/message.html', context)


def sendMessage(request, pk):
    reciever = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.reciever = reciever

        if sender:
            message.name = sender.name
            message.email = sender.email    
        
        message.save()

        return redirect('single profile', pk=reciever.id)

    context = {'form':form, 'reciever':reciever}
    return render(request, 'users/send message.html', context)