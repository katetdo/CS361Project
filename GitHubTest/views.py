from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from .models import MySyllabus, MyUser, PersonalInfo


class Home(View):
    def get(self, request):
        request.session["current"] = ""
        return render(request, "login.html", {"error_msg": ""})

    def post(self, request):
        url_dict = {"A": "/administrator/", "I": "/instructor/", "TA": "/TA/"}
        try:
            my_user = MyUser.objects.get(username=request.POST['username'], password=request.POST['password'])
            request.session["current"] = my_user.id
          #  return redirect(url_dict[my_user.type])
            user_type = my_user.type
            if user_type == 'A':
                return redirect("/administrator/")
            else:
                return redirect("/")
        except ObjectDoesNotExist:
            return render(request, "login.html", {"error_msg": "Incorrect username or password."})


class AdminView(View):
    # Todo....
    def get(self, request):
        return render(request, "admin.html", {})


'''   def post(self,request):
       try:
           myAdmin = Admins.objects.get(name=request.POST['name'], password=request.POST['password'])
          request.session["current"] = myAdmin.id
          # to do...put where to redirect
           return redirect("/Admin")
       except Exception as e:


           return render(request,"admin.html",{})
    '''


class TAView(View):
    # Todo....
    def get(self, request):
        request.session["current"] = ""

        # Todo....
        return render(request, "TA_UI_page2.html.html", {})

    def post(self, request):
        # try:
        #     myuser = MyUser.objects.get(name=request.POST['name'], password=request.POST['password'], type=request.POST['type'])
        #     request.session["current"] = myuser.id
        #     # to do...put where to redirect
        #     return redirect("/")
        # except Exception as e:
        #
        # Todo....
        return render(request, "TA_UI_page2.html.html", {})


class InstructorView(View):
    # Todo....
    def get(self, request):
        request.session["current"] = ""
        return render(request, "TA_UI_page1.html.html", {})

    def post(self, request):
        return render(request, "TA_UI_page1.html.html", {})



