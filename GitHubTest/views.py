from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from GitHubTest.models import MySyllabus, MyUser, PersonalInfo


class Home(View):
    def get(self, request):
        request.session["current"] = ""
        return render(request, "login.html", {"error_msg": ""})

    def post(self, request):
        url_dict = {"A": "/administrator/", "I": "/instructor/", "T": "/TA/"}
        try:
            my_user = MyUser.objects.get(username=request.POST['username'], password=request.POST['password'])
            request.session["current"] = my_user.id
          #  return redirect(url_dict[my_user.type])
            user_type = my_user.type
            if user_type == 'A':
                return redirect("/administrator/")
            elif user_type == 'I' or user_type == 'T':
                return redirect("/PersonalInfo/")
            else:
                return redirect("/")
        except ObjectDoesNotExist:
            return render(request, "login.html", {"error_msg": "Incorrect username or password."})


class AdminView(View):
    def get(self, request):
        current_user = PersonalInfo.objects.get(user=MyUser.objects.get(id=request.session["current"]))
        name = current_user.firstName + " " + current_user.lastName
        user_info = list(PersonalInfo.objects.all().values())
        syllabi = list(MySyllabus.objects.all().values())
        return render(request, "admin.html", {"user_info": user_info, "name": name, "syllabi": syllabi})

    def post(self, request):
        current_user = PersonalInfo.objects.get(user=MyUser.objects.get(id=request.session["current"]))
        name = current_user.firstName + " " + current_user.lastName
        # create new user
        new_user = MyUser(username=request.POST["username"], password=request.POST["password"], type=request.POST["type"])
        new_user.save()
        new_info = PersonalInfo(lastName=request.POST["lastName"], firstName=request.POST["firstName"],
                                officeHours="", officeNumber="",
                                email="", phoneNumber="",
                                syllabus=MySyllabus.objects.get(id=request.POST["syllabus"]),
                                user=new_user)
        new_info.save()
        user_info = list(PersonalInfo.objects.all().values())
        syllabi = list(MySyllabus.objects.all().values())
        return render(request, "admin.html", {"user_info": user_info, "name": name, "syllabi": syllabi})


class PersonalInfoView(View):
    def get(self, request):
        # user = request.session.get("current", False)
        current_user = PersonalInfo.objects.get(user=MyUser.objects.get(id=request.session["current"]))
        # user_info = list(PersonalInfo.objects.filter(user=user))
        return render(request, "TA_UI_page1.html", {"user_info": current_user})

    def post(self, request):
        user = PersonalInfo.objects.get(user=MyUser.objects.get(id=request.session["current"]))
        name = user.firstName + " " + user.lastName
        new_info = PersonalInfo(firstName=user.firstName,
                                lastName=user.lastName,
                                officeHours=request.POST["officeHours"],
                                officeNumber=request.POST["officeNumber"],
                                email=request.POST["email"],
                                phoneNumber=request.POST["phoneNumber"],
                                syllabus=user.syllabus,
                                user=user)

        new_info.save()
        return render(request, "TA_UI_page1.html", {})

