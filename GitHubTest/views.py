from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from GitHubTest.models import MySyllabus, MyUser, MyUserLogin, MyCourse, MySection, MySyllabusComponent


class Home(View):
    def get(self, request):
        request.session["current"] = ""
        syllabi = list(MySyllabus.objects.all())
        return render(request, "login.html", {"syllabi": syllabi, "error_msg": ""})

    def post(self, request):
        msg = "Something went wrong. Please try again."
        if "login" in request.POST:
            try:
                login = MyUserLogin.objects.get(username=request.POST['username'], password=request.POST['password'])
                my_user = MyUser.objects.get(login=login)
                request.session["current"] = my_user.id
                return redirect("/Administrator/" if my_user.type == 'A' else "/PersonalInfo/")
            except ObjectDoesNotExist:
                msg = "Incorrect username or password."
        if "guest" in request.POST:
            return redirect("/Syllabus/" + request.POST["course"])
        syllabi = list(MySyllabus.objects.all())
        return render(request, "login.html", {"syllabi": syllabi,
                                              "error_msg": msg})


def build_course_info(course_objects):
    courses = []
    for course in course_objects:
        sections = []
        section_objects = MySection.objects.filter(course=course)
        for s in section_objects:
            sections.append(str(s.sectionNumber) + " " + s.description + ", " +
                            s.teachingAssistant.firstName + " " + s.teachingAssistant.lastName)
        course = {
            "name": course.courseName,
            "instructor": course.instructor,
            "sections": sections
        }
        courses.append(course)
    return courses


class AdminView(View):
    def get(self, request):
        return render(request, "admin.html", get_admin_template_data())

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
                                    description=request.POST["description"],
                                    course=MyCourse.objects.get(id=request.POST["course"]),
                                    teachingAssistant=MyUser.objects.get(id=request.POST["teaching_assistant"]))
            new_section.save()
        return render(request, "admin.html", get_admin_template_data())


def get_admin_template_data():
    return {
        "tas": list(MyUser.objects.filter(type="T")),
        "instructors": list(MyUser.objects.filter(type="I")),
        "courses": list(MyCourse.objects.all().values()),
        "course_info": build_course_info(MyCourse.objects.all())
    }


class PersonalInfoView(View):
    def get(self, request):
        user = MyUser.objects.get(id=request.session["current"])
        return render(request, "personal_info.html", {"user_info": user})

    def post(self, request):
        user = MyUser.objects.get(id=request.session["current"])
        user.officeHours = request.POST["officeHours"]
        user.email = request.POST["email"]
        user.phoneNumber = request.POST["phoneNumber"]
        user.officeNumber = request.POST["officeNumber"]
        user.save()
        return render(request, "personal_info.html", {"user_info": user})


class InstructorView(View):
    def get(self, request):
        return render(request, "instructor.html", get_instructor_template_data(request.session["current"]))

    def post(self, request):
        if "create_syllabus" in request.POST:
            new_syllabus = MySyllabus(course=MyCourse.objects.get(courseName=request.POST["course"]),
                                      instructor=MyUser.objects.get(id=request.session["current"]),
                                      courseName=request.POST["course"],
                                      courseDescription=request.POST["description"])
            new_syllabus.save()
        elif "delete_syllabus" in request.POST:
            syllabus = MySyllabus.objects.get(id=request.POST["syllabus"])
            syllabus.delete()
        elif "add_component" in request.POST:
            new_component = MySyllabusComponent(syllabus=MySyllabus.objects.get(id=request.POST["syllabus"]),
                                                name=request.POST["name"],
                                                content=request.POST["contents"])
            new_component.save()
        elif "update_components" in request.POST:
            return update_instructor_components(request)
        elif "delete_component" in request.POST:
            component = MySyllabusComponent.objects.get(id=request.POST["component"])
            component.delete()
        return render(request, "instructor.html", get_instructor_template_data(request.session["current"]))


def get_instructor_template_data(session_id):
    user = MyUser.objects.get(id=session_id)
    available_courses = []
    for i in list(MyCourse.objects.filter(instructor=user)):
        try:
            MySyllabus.objects.get(course=i)
        except ObjectDoesNotExist:
            available_courses.append(i)
    return {
        "syllabi": list(MySyllabus.objects.filter(instructor=user).values()),
        "available_courses": available_courses,
        "selected_syllabus": "...",
        "components": []
    }


def update_instructor_components(request):
    data = get_instructor_template_data(request.session["current"])
    selected_syllabus = MySyllabus.objects.get(id=request.POST["update_components"])
    data["selected_syllabus"] = selected_syllabus.courseName
    data["components"] = list(MySyllabusComponent.objects.filter(syllabus=selected_syllabus))
    return render(request, "instructor.html", data)


def render_syllabus(request, course):
    syllabus = MySyllabus.objects.get(courseName=course)
    sections = list(MySection.objects.filter(course=MyCourse.objects.get(courseName=course)))
    components = list(MySyllabusComponent.objects.filter(syllabus=syllabus).values())
    return render(request, "syllabus.html", {"syllabus": syllabus,
                                             "instructor": syllabus.instructor,
                                             "sections": sections,
                                             "components": components})






