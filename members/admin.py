from django.contrib import admin
from .models import Schedule, Student, Subject, Teacher, Class, Grade
from django.contrib.auth.hashers import make_password
from .forms import TeacherForm

admin.site.register(Schedule)
admin.site.register(Student)
admin.site.register(Subject)

class TeacherAdmin(admin.ModelAdmin):
    form = TeacherForm

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Teacher, TeacherAdmin)

admin.site.register(Class)
admin.site.register(Grade)
