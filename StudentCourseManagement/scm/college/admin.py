from django.contrib import admin
from college.models import Department, Teacher, Student, Course, Enrollment, Assignment, Submission, Attendance, Subject, HOD
from django import forms

# Register your models here.
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Attendance)
admin.site.register(Subject)
admin.site.register(HOD)

class TeacherAdminForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = "__all__"

    def clean_user(self):
        user = self.cleaned_data.get("user")

        if user and Student.objects.filter(user=user).exists():
            raise forms.ValidationError(
                "This user is already registered as a Student."
            )

        return user


class StudentAdminForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = "__all__"

    def clean_user(self):
        user = self.cleaned_data.get("user")

        if user and Teacher.objects.filter(user=user).exists():
            raise forms.ValidationError(
                "This user is already registered as a Teacher."
            )

        return user

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherAdminForm
    list_display = (
        "user",
        "phone",
        "qualification",
        "department",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = (
        "user",
        "admission_no",
        "year",
        "phone",
        "department",
    )