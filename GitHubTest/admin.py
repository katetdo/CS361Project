from django.contrib import admin
from GitHubTest.models import MyUser, MySyllabus, MyCourse, MySection

admin.site.register(MyUser)
admin.site.register(MySyllabus)
admin.site.register(MyCourse)
admin.site.register(MySection)

# Register your models here.
