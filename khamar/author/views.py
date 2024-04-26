from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout,authenticate
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
# Create your views here.
class UserRegistrationView(FormView):
    template_name='user_registration.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('home')

    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)
    
    def post(self, request, *args,  **kwargs ) :
        form=self.form_class(data=request.POST)

        if form.is_valid():
            user=form.save()
            return HttpResponse("Registration successful")
        

        return self.form_invalid(form)

class UserLoginView(LoginView):
    template_name = 'user_login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
    

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    
class UserAccountUpdateView(View):
    template_name='profile.html'

    def get(self,request):
        if request.user.is_authenticated:
            form=UserUpdateForm(instance=request.user)
            return render(request,self.template_name,{'form':form})
        else:
            return redirect('home')

    def post(self,request):
        if request.user.is_authenticated:
            form=UserUpdateForm(request.POST,instance=request.user)  
            if form.is_valid():
                form.save()
                messages.success(self.request,"User Profile Information Updated Successfully")
                return redirect('home')
            return render(request,self.template_name,{'form':form})
        else:
            return redirect('home')
          