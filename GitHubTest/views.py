from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from GitHubTest.models import MySyllabus, MyUser, MyUserLogin, MyCourse, MySection


class Home(View):
    def get(self, request):
        request.session["current"] = ""
        return render(request, "login.html", {"error_msg": ""})

    def post(self, request):
        url_dict = {"A": "/administrator/", "I": "/instructor/", "T": "/TA/"}
        try:
            login = MyUserLogin.objects.get(username=request.POST['username'], password=request.POST['password'])
            my_user = MyUser.objects.get(login=login)
            request.session["current"] = my_user.id
            # return redirect(url_dict[my_user.type])
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
        return render(request, "admin.html", self.get_template_data())

    def post(self, request):
        if "create_user" in request.POST:
            new_login = MyUserLogin(username=request.POST["username"], password=request.POST["password"])
            new_login.save()
            new_user = MyUser(login=new_login, type=request.POST["type"],
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
        return render(request, "admin.html", self.get_template_data())

    def get_template_data(self):
        return {
            "tas": list(MyUser.objects.filter(type="T")),
            "instructors": list(MyUser.objects.filter(type="I")),
            "courses": list(MyCourse.objects.all().values()),
            "course_info": self.build_course_info(MyCourse.objects.all())
        }

    def build_course_info(self, course_objects):
        courses = []
        for course in course_objects:
            sections = []
            section_objects = MySection.objects.filter(course=course)
            for s in section_objects:
                sections.append(str(s.sectionNumber) + ", " +
                                s.teachingAssistant.firstName + " " + s.teachingAssistant.lastName)
            course = {
                "name": course.courseName,
                "instructor": course.instructor,
                "sections": sections
            }
            courses.append(course)
        return courses


class PersonalInfoView(View):
    def get(self, request):
        user = MyUser.objects.get(id=request.session["current"])
        return render(request, "TA_UI_page1.html", {"user_info": user})

    def post(self, request):
        user = MyUser.objects.get(id=request.session["current"])
        user.officeHours = request.POST["officeHours"]
        user.email = request.POST["email"]
        user.phoneNumber = request.POST["phoneNumber"]
        user.officeNumber = request.POST["officeNumber"]
        user.save()
        return render(request, "TA_UI_page1.html", {"user_info": user})