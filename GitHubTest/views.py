from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from GitHubTest.models import MySyllabus, MyUser, MyCourse, MySection


class Home(View):
    def get(self, request):
        request.session["current"] = ""
        return render(request, "login.html", {"error_msg": ""})

    def post(self, request):
        url_dict = {"A": "/administrator/", "I": "/instructor/", "T": "/TA/"}
        try:
            my_user = MyUser.objects.get(username=request.POST['username'], password=request.POST['password'])
            request.session["current"] = my_user.id
            #return redirect(url_dict[my_user.type])
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
        current_user = MyUser.objects.get(id=request.session["current"])
        user_info = list(MyUser.objects.all().values())
        courses = list(MyCourse.objects.all().values())
        return render(request, "admin.html", {"user_info": user_info, "courses": courses})

    def post(self, request):
        if "create_user" in request.POST:
            new_user = MyUser(username=request.POST["username"], password=request.POST["password"],
                              type=request.POST["type"],
                              lastName=request.POST["lastName"], firstName=request.POST["firstName"],
                              officeHours="", officeNumber="", email="", phoneNumber="")
            new_user.save()
        elif "create_course" in request.POST:
            new_course = MyCourse(courseName=request.POST["course_name"],
                                  instructor=MyUser.objects.get(id=request.POST["instructor"]))
            new_course.save()
        elif "create_section" in request.POST:
            new_section = MySection(sectionNumber=request.POST["section_number"],
                                    course=MyCourse.objects.get(id=request.POST["course"]),
                                    teachingAssistant=MyUser.objects.get(id=request.POST["teaching_assistant"]))
            new_section.save()
        user_info = list(MyUser.objects.all().values())
        courses = list(MyCourse.objects.all().values())
        return render(request, "admin.html", {"user_info": user_info, "courses": courses})



class PersonalInfoView(View):
    def get(self, request):
        current_user = MyUser.objects.get(id=request.session["current"])
        return render(request, "TA_UI_page1.html", {"user_info": current_user})

    def post(self, request):
        user = MyUser.objects.get(id=request.session["current"])
        name = user.firstName + " " + user.lastName
        user.officeHours = request.POST["officeHours"]
        user.email = request.POST["email"]
        user.phoneNumber = request.POST["phoneNumber"]
        user.officeNumber = request.POST["officeNumber"]
        user.save()
        return render(request, "TA_UI_page1.html", {"user_info": user})