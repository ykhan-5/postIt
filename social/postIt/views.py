from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Peep
from django.contrib import messages
from .forms import PeepForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout #Auth stuff 
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


def home(request):
    if request.user.is_authenticated:
        form = PeepForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                peep = form.save(commit=False)
                peep.user = request.user
                peep.save()
                messages.success(request, ("Your Peep has been posted!"))
                return redirect('home')


        peeps = Peep.objects.all().order_by("-created_at")
        return render(request,'home.html',{"peeps":peeps, "form":form})
    else:
      peeps = Peep.objects.all().order_by("-created_at")
      return render(request,'home.html',{"peeps":peeps})

def profile_list(request):
      if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
      else:
          messages.success(request, ("You must be logged in to view this page!"))
          return redirect('home')
      
def profile(request,pk):
    if request.user.is_authenticated: #check logged in or not
        profile = Profile.objects.get(user_id=pk)
        peeps = Peep.objects.filter(user_id=pk)
        
        # Post form logic
        if request.method == "POST":
            # Get current user id 
            current_user_profile = request.user.profile
            #Get form data
            action = request.POST['follow']

            #Decide between follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)

            #Save the profile
            current_user_profile.save()

        return render(request, "profile.html", {"profile":profile, "peeps":peeps})
    else:
        messages.success(request, ("You must be logged in to view this page!"))
        return redirect('home')

def followers(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk: #means it is OUR page 
          profiles = Profile.objects.get(user_id=pk)
          return render(request, 'followers.html', {"profiles": profiles})
        else:
          messages.success(request, ("Not your page buddy."))
          return redirect('home')
    else:
        messages.success(request, ("You must be logged in to view this page!"))
        return redirect('home')

def login_user(request):
    if request.method == 'POST':
      username = request.POST['username']    
      password = request.POST['password']    

      user = authenticate(request, username=username, password=password)
      if user is not None:
          login(request, user)
          messages.success(request, ("You have been logged in, get Posting!"))
          return redirect('home')
      else:
          messages.success(request, ("There was an error logging in, please try again..."))
          return redirect('login')
          

    else:
      return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out, sorry to see you go..."))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #first_name = form.cleaned_data['first_name']
            #last_name = form.cleaned_data['last_name']
            #email = form.cleaned_data['email']

            #log in user
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("You have registered successfully, Welcome!"))
            return redirect('home')
        

    return render(request, "register.html", {'form':form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id) #grabs profile
        #Get Forms
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None,request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            
            user_form.save()
            profile_form.save()

            login(request, current_user)
            messages.success(request, ("You have registered successfully, Welcome!"))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form,'profile_form':profile_form})
    else:
        messages.success(request, ("You must be logged in."))
        return redirect('home')
    

def peep_like(request,pk):
    if request.user.is_authenticated:
      peep = get_object_or_404(Peep, id=pk)
      if peep.likes.filter(id=request.user.id):
        peep.likes.remove(request.user)
      else:
        peep.likes.add(request.user)
      return redirect(request.META.get("HTTP_REFERER")) #redirect to page that "refered you"
    
    
    else:
        messages.success(request, ("You must be logged in."))
        return redirect('home')
    

def peep_show(request,pk):
    peep = get_object_or_404(Peep, id=pk)
    if peep:
        return render(request, "show_peep.html", {'peep':peep})
    else:
        messages.success(request, ("That Post does not exist..."))
        return redirect('home')
    
def delete_peep(request, pk):
    if request.user.is_authenticated:
      peep = get_object_or_404(Peep, id=pk)
      #check owneership of peep
      if request.user.username == peep.user.username:
        #Delete peep 
        peep.delete()
        messages.success(request, ("Deleted successfully."))  
        return redirect(request.META.get("HTTP_REFERER")) #redirect to page that "refered you"
      else:
          messages.success(request, ("Not yours bud."))  
          return redirect('home')
    else:
        messages.success(request, ("Log in to continue..."))
        return redirect(request.META.get("HTTP_REFERER")) #redirect to page that "refered you"
    
def edit_peep(request, pk):
    if request.user.is_authenticated:
      #check owneership of peep
      peep = get_object_or_404(Peep, id=pk)
      if request.user.username == peep.user.username:
        
        form = PeepForm(request.POST or None, instance=peep)
        if request.method == 'POST':
            if form.is_valid():
                peep = form.save(commit=False)
                peep.user = request.user
                peep.save()
                messages.success(request, ("Your Peep has been Updated!"))
                return redirect('home')
        else:
            return render(request, "edit_peep.html", {'form':form, 'peep':peep})    
      else:
          messages.success(request, ("Not yours bud."))  
          return redirect('home')
    else:
        messages.success(request, ("Log in to continue..."))
        return redirect('home') #redirect to page that "refered you"
    
def search(request):
    if request.method == "POST":
        #grab form field input
        search = request.POST['search']
        #Search database
        searched = Peep.objects.filter(body__contains = search)

        return render(request, "search.html", {'search':search,'searched':searched})
    else:
        return render(request, "search.html", {})