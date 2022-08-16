import imp
import profile
from pyexpat.errors import messages
import re
from ssl import create_default_context
from tkinter.messagebox import NO
from click import password_option
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from matplotlib.pyplot import get
from .models import post,comment, userprofile
from django.contrib.auth.models import User ,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import PostForm ,CommentForm
from django.views.generic.edit  import UpdateView,DeleteView 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin



def index(request):
    # user_object=User.objects.get(username=request.user.username)
    # user_profile=Profile.objects.get(user=user_object)
    return render(request,'landing.html')

# def signup (request):
# #     if request.method=="POST": 
# #         username=request.POST['username']
# #         email=request.POST['email']
# #         password=request.POST['password']
# #         password2=request.POST['password2']
# #         if(password==password2):
# #             if User.objects.filter(email=email).exists():
# #                 messages.info(request,'Such An Email-Id exists')
# #                 return redirect('signup')
# #             elif User.objects.filter(username=username).exists():
# #                  messages.info(request,'Username taken')
# #                  return redirect('signup')
# #             else:
# #                 user=User.objects.create_user(username=username,email=email,password=password)
# #                 user.save()
# #                 user_login=auth.authenticate(username=user,password=password)
# #                 auth.login(request,user_login)

# #                 user_model =User.objects.get(username=username)
# #                 new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
# #                 new_profile.save()
            
#                 return redirect('settings')


# #         else:
# #             messages.info(request,'Password Not Matching')
# #             return redirect('signup')


# #     else:
# #         return render(request,'signup.html')

# def login(request):
# #     if request.method=="POST":
    
# #         username=request.POST['username']
# #         print(username)
# #         password=request.POST['password']
# #         user=auth.authenticate(username=username,password=password)
# #         if user is not None:
# #             auth.login(request,user)
# #             return redirect('/')
# #         else:
          
# #             messages.info(request,'Invalid Credentials')
#             return redirect('posts')
# #     else:
        
# #         return render(request,'login.html')
# #     #remember to make changes in html
# # 
# def logout(request):
# #     auth.logout(request)
#     return redirect('signin')

# #
# def  upload(request):
#     return HttpResponse("<h1>hello</h1>")


# def settings(request):
        
# #         check = Profile.objects.filter(user=request.user)
# #         if(len(check)>0):
# #             user_profile=Profile.objects.get(user=request.user)
# #             if request.method=="POST":
# #                     print("hello")
# #                     bio=request.POST['bio']
# #                     organisation=request.POST['organisation']
# #                     role=request.POST['role']
# #                     yof=request.POST['yof']

    
# #                     user_profile.bio=bio
# #                     user_profile.organisation = organisation
# #                     user_profile.role=role
# #                     user_profile.yof=yof
# #                     if request.FILES.get('image')==None:
# #                      image=user_profile.profileimg
# #                      user_profile.profileimg =image
# #                     else:
# #                         image=request.FILES.get('image')
# #                         user_profile.profileimg =image
# #                     user_profile.save()
#                     return redirect('settings')
        

# #             return render(request,'settings.html',{'user_profile':user_profile})
# #         else:
# #               return render(request,'settings.html')

          
class PostView(LoginRequiredMixin,View):
    def get(self ,request,*args,**kwargs):
        posts =post.objects.all().order_by('-created_at')
        form = PostForm()
        context={
            'postlist':posts,
            'form':form 
        }
        return render(request, 'posts.html',context)  

    def post(self,request,*args,**kwargs):
        posts =post.objects.all().order_by('-created_at')
        form = PostForm(request.POST,request.FILES)

        if form.is_valid():
             new_post = form.save(commit=False)
             new_post.user=request.user
             new_post.save()
        context={
            'postlist':posts,
            'form':form 
        }
        return render(request, 'posts.html',context)  

class PostDetailView(LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):
        post_single = post.objects.get(pk=pk)
        form=CommentForm()
        comments=comment.objects.filter(post=post_single).order_by('-created_at')
        context={
            'post':post_single,
            'form':form,
            'comments':comments

        }
        return render (request,'post_single.html',context) 
    def post(self ,request,pk,*args,**kwargs ):
        post_single =post.objects.get(pk=pk)
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user=request.user
            new_comment.post=post_single
            new_comment.save()
    
        comments=comment.objects.filter(post=post_single).order_by('-created_at')
        context={
            'post':post_single,
            'form':form,
            'comments':comments
        }
        return render (request,'post_single.html',context) 


class PostEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=post 
    fields=['content','image']
    template_name='post_edit.html'
    
    def get_success_url(self):
        pk=self.kwargs['pk'] 
        return reverse_lazy('post_single',kwargs={'pk':pk})
    def test_func(self):
        post =self.get_object()
        if self.request.user == post.user:
            return True
        else:
            False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=post
    template_name='delete.html'
    success_url=reverse_lazy('posts')
    def test_func(self):
        post =self.get_object()
        if self.request.user == post.user:
            return True
        else:
            False

class CommentDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=comment
    template_name='delete_comment.html'
    
    def get_success_url(self):
        pk=self.kwargs['post_pk']
        return reverse_lazy('post_single',kwargs={'pk':pk})
    
    def test_func(self):
        post =self.get_object()
        if self.request.user == post.user:
            return True
        else:
            False


class ProfileView(View):
    def get(self,request,pk,*args,**kwargs):
        
        profile=userprofile.objects.get(pk=pk)
        user=profile.user
        posts=post.objects.filter(user=user).order_by('-created_at')
        context={
            'user':user,
            'profile':profile,
            'posts':posts
        }
        return render(request,'profile.html',context)

class ProfileEditView(UpdateView):
    model=userprofile
    fields=['name','bio','yof','profileimg','organisation','role','LinkProfile']
    template_name="profile_edit.html"
    def get_success_url(self):
        pk=self.kwargs['pk'] 
        return reverse_lazy('profile',kwargs={'pk':pk})
    def test_func(self):
        profile =self.get_object()
        if self.request.user == profile.user:
            return True
        else:
            False
class LikePost(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post_single=post.objects.get(pk=pk)

        isDislike=False;
        
        for Dislike in post_single.dislikes.all():
            if Dislike == request.user:
                isDislike=True
                break
        if isDislike:
            post_single.dislikes.remove(request.user)


        islike=False;
        
        for like in post_single.likes.all():
            if like == request.user:
                islike=True
                break
        # if islike:
        #     post_single.likes.remove(request.user)
        if not islike:
            post_single.likes.add(request.user)

        next=request.POST.get('next','/')
        return HttpResponseRedirect(next)
        
class DislikePost(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post_single=post.objects.get(pk=pk)
        islike=False;
        
        for like in post_single.likes.all():
            if like == request.user:
                islike=True
                break
        if islike:
            post_single.likes.remove(request.user)

        
        isDislike=False;
        
        for Dislike in post_single.dislikes.all():
            if Dislike == request.user:
                isDislike=True
                break
        # if isDislike:
        #     post_single.dislikes.remove(request.user)
        if not isDislike:
            post_single.dislikes.add(request.user)
        next=request.POST.get('next','/')
        return HttpResponseRedirect(next)
# def CommentReply(View):
#     def post(self,request,post_pk,pk,*args,**kwargs):

        




        













 

 


      