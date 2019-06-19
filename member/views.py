from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect

class index(View):
    template_name='index.html'
    def get(self,request):
        return render(request,self.template_name,{})
    def post(self,request,*args, **kwargs):
        username=request.POST['username']
        print(username)
        try:
            user = User.objects.get(username=username)
        except:
            user = User.objects.create(
                username=username,
                email=request.POST['email']
            )
            user.set_password(request.POST['password'])
            user.save()
        return render(request, self.template_name, {})



class Login(View):

    def post(self,request,*args, **kwargs):
        try:
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if (user is not None):
                auth.login(request, user)
                return redirect('/chat')
        except:
            return render(request, self.template_name, {"message": "login fail"})


class Logout(View):
    template_name='index.html'
    def get(self, request):
        auth.logout(request)
        return redirect('index')
