from django.shortcuts import render
from django.shortcuts import get_object_or_404,redirect
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    return render(request,'index.html')

def Tweet_list(request):
    tweets=Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})
@login_required
def Tweet_create(request):
    if request.method=='POST':
        form=TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TweetForm()
    return render(request,'tweet_form.html',{'form':form})
@login_required
def Tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form=TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form,})
@login_required
def Tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_delete.html',{'tweet':tweet})

def register(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST) 
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form=UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})

def profile(request,username):
    profile_user = get_object_or_404(User, username=username )
    user_tweets=Tweet.objects.filter(user=profile_user).order_by("-created_at")
    following_count = 0
    followers_count = 0
    context={
        'profile_user':profile_user,
        "user_tweets": user_tweets,
        "following_count":following_count,
        "followers_count":followers_count,
    }
    return render(request,'profile.html',context)

   