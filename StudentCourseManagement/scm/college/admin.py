from django.contrib import admin
from college.models import Department, Teacher, Student, Course, Enrollment, Assignment, Submission, Attendance, Subject, HOD

# Register your models here.
admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Attendance)
admin.site.register(Subject)
admin.site.register(HOD)
