from django.contrib import admin
from GitHubTest.models import MyUserLogin, MyUser, MySyllabus, MyCourse, MySection, MySyllabusComponent

admin.site.register(MyUserLogin)
admin.site.register(MyUser)
admin.site.register(MySyllabus)
admin.site.register(MySyllabusComponent)
admin.site.register(MyCourse)
admin.site.register(MySection)

# Register your models here.
