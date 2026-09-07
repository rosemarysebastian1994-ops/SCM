"""
URL configuration for scm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name='college'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_create'),
    path('departments/edit/<int:i>/', views.department_update, name='department_update'),
    path('departments/delete/<int:i>/', views.department_delete, name='department_delete'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_create, name='teacher_create'),
    path('teachers/edit/<int:i>/', views.teacher_update, name='teacher_update'),
    path('teachers/delete/<int:i>/', views.teacher_delete, name='teacher_delete'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/edit/<int:i>/', views.student_update, name='student_update'),
    path('students/delete/<int:i>/', views.student_delete, name='student_delete'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/edit/<int:i>/', views.course_update, name='course_update'),
    path('courses/delete/<int:i>/', views.course_delete, name='course_delete'),
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/add/', views.enrollment_create, name='enrollment_create'),
    path('enrollments/delete/<int:i>/', views.enrollment_delete, name='enrollment_delete'),
    path('student/my-courses', views.my_courses, name='my_courses'),
    path('teacher/students', views.teacher_students, name='teacher_students'),
    path('subject/<int:subject_id>/assignment/add/',views.create_assignment,name='create_assignment'),
    path('teacher/courses', views.teacher_courses, name='teacher_courses'),
    path("student/assignments/",views.student_assignments,name="student_assignments"),
    path("assignment/<int:assignment_id>/submit/",views.submit_assignment,name="submit_assignment"),
    path("assignment/<int:assignment_id>/submissions/",views.view_submissions,name="view_submissions"),
    path("teacher/course/<int:course_id>/assignments/",views.course_assignments,name="course_assignments"),
    path('assignment/<int:assignment_id>/edit/',views.edit_assignment,name='edit_assignment'),
    path('assignment/<int:assignment_id>/delete/',views.delete_assignment,name='delete_assignment'),
    path("submission/<int:submission_id>/grade/",views.grade_submission,name="grade_submission"),
    path('student/results/', views.my_results, name='my_results'),
    path('search', views.SearchCourse.as_view(), name='search'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('attendance/select-course/', views.select_course_attendance, name='select_course_attendance'),
    path('attendance/mark/<int:subject_id>/',views.mark_attendance,name='mark_attendance'),
    path('student/my_attendance/', views.my_attendance, name='my_attendance'),
    path('courses', views.courses, name='courses'),
    path('departments', views.departments, name='departments'),
    path('contact', views.contact, name='contact'),
    path("attendance/history/", views.attendance_history, name="attendance_history"),
    path("attendance/history/<int:subject_id>/", views.attendance_dates,name="attendance_dates"),
    path("attendance/history/<int:subject_id>/<str:date>/", views.attendance_detail, name="attendance_detail"),
    path("teacher_profile/", views.teacher_profile, name="teacher_profile"),
    path("student_profile", views.student_profile, name="student_profile"),
    path('teacher_profile/edit/', views.edit_teacher_profile, name='edit_teacher_profile'),
    path('student_profile/edit/', views.edit_student_profile, name='edit_student_profile'),
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(
            template_name='password_change.html',
            success_url=reverse_lazy(
                'college:password_change_done'
            )
        ),
        name='password_change'
    ),

    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='password_change_done.html'
        ),
        name='password_change_done'
    ),
    path('hod_dashboard', views.hod_dashboard, name='hod_dashboard'),
    path('hod/assign-subject/<int:subject_id>/', views.assign_subject, name='assign_subject'),
]
