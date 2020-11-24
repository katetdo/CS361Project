from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from GitHubTest.models import MyUser


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
