from django.shortcuts import render, redirect
from django.views import View
from .models import MySyllabus, MyUser, PersonalInfo, Admins



class Home(View):
    # Todo....
    def get(self,request):
        request.session["current"] = ""
        return render(request,"home.html",{})

    def post(self,request):
        try:
            myuser = MyUser.objects.get(name=request.POST['name'], password=request.POST['password'], type=request.POST['type'])
            request.session["current"] = myuser.id
            # to do...put where to redirect
            return redirect("/")
        except Exception as e:
            return render(request,"home.html",{})


class TAView(View):
    # Todo....
    def get(self,request):
        request.session["current"] = ""

        # Todo....
        return render(request,"TA_UI_page2.html.html",{})

    def post(self,request):
        # try:
        #     myuser = MyUser.objects.get(name=request.POST['name'], password=request.POST['password'], type=request.POST['type'])
        #     request.session["current"] = myuser.id
        #     # to do...put where to redirect
        #     return redirect("/")
        # except Exception as e:
        #
            #Todo....
            return render(request,"TA_UI_page2.html.html",{})

class InstructorView(View):
    # Todo....
    def get(self,request):
        request.session["current"] = ""
        return render(request,"TA_UI_page1.html.html",{})

    def post(self,request):

            return render(request,"TA_UI_page1.html.html",{})


class AdminView(View):
    # Todo....
    def get(self,request):

        return render(request,"admin.html",{})

    # Todo....
    def post(self,request):
        try:
            myAdmin = Admins.objects.get(name=request.POST['name'], password=request.POST['password'])
            request.session["current"] = myAdmin.id
            # to do...put where to redirect
            return redirect("/Admin")
        except Exception as e:

            return render(request,"admin.html",{})
      
class Login(View):
    def get(self, request):
        return render(request, "", {"error_msg": ""})   # TODO add template

    def post(self, request):
        is_valid = False
        try:
            m_user = MyUser.objects.get(username=request.POST["username"])
            is_valid = (m_user.password == request.POST["password"])
        except:
            return render(request, "", {"error_msg": "User not found."})
        if is_valid:
            request.session["current"] = m_user.id
            return redirect("")                         # TODO redirect to correct page based on user type.
        else:
            return render(request, "", {"error_msg": ""})       # TODO add template
