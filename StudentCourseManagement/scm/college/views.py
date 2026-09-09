from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentRegistrationForm, DepartmentForm, TeacherForm, StudentForm, CourseForm, EnrollmentForm, \
    AssignmentForm, SubmissionForm, GradeSubmissionForm, UserUpdateForm, TeacherProfileForm, StudentProfileForm, SubjectForm
from .models import Department, Teacher, Student, Course, Enrollment, Assignment, Submission, Attendance, HOD, Subject
from django.contrib import messages
from django.utils import timezone
from .decorators import teacher_required, student_required, hod_required, admin_required

def home(request):
    user = request.user
    if user.is_superuser:
        return redirect('college:admin_dashboard')
    elif user.groups.filter(name='HOD').exists():
        return redirect('college:hod_dashboard')
    elif user.groups.filter(name='Teacher').exists():
        return redirect('college:teacher_dashboard')
    elif user.groups.filter(name='Student').exists():
        return redirect('college:student_dashboard')
    elif user.is_authenticated:
        return render(request, 'home2.html')
    else:
        pass
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('college:login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth import authenticate, login, logout

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('college:admin_dashboard')
            elif user.groups.filter(name='HOD').exists():
                return redirect('college:hod_dashboard')
            elif user.groups.filter(name='Teacher').exists():
                return redirect('college:teacher_dashboard')
            elif user.groups.filter(name='Student').exists():
                return redirect('college:student_dashboard')
            else:
                return redirect('college:home')
        else:
            messages.error(
                request,
                "Invalid username or password."
            )
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('college:login')

from django.contrib.auth.decorators import login_required

@login_required
@student_required
def student_dashboard(request):
    return render(request, "student_dashboard.html")

@login_required
@teacher_required
def teacher_dashboard(request):
    is_hod = request.user.groups.filter(name='HOD').exists()
    print(is_hod)
    return render(request, "teacher_dashboard.html", {'is_hod':is_hod})

@login_required
@admin_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
@admin_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments':departments})

@login_required
@admin_required
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("college:department_list")
    else:
        form = DepartmentForm()
    return render(request,"department_form.html",{"form": form}
    )

@login_required
@admin_required
def department_update(request, i):
    department = Department.objects.get(id=i)
    if request.method == "POST":
        form = DepartmentForm(request.POST,instance=department)
        if form.is_valid():
            form.save()
            return redirect("college:department_list")
    else:
        form = DepartmentForm(instance=department)
    return render(request,"department_form.html",{"form": form}
    )

@login_required
@admin_required
def department_delete(request, department_id):

    department = get_object_or_404(
        Department,
        id=department_id
    )

    if request.method == "POST":
        department.delete()

        messages.success(
            request,
            f'Department "{department.name}" deleted successfully.'
        )

        return redirect("college:department_list")

    return redirect("college:department_list")

@login_required
@admin_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers':teachers})

@login_required
@admin_required
def teacher_create(request):

    print("===== TEACHER CREATE VIEW CALLED =====")

    if request.method == "POST":

        print("===== TEACHER POST =====")

        form = TeacherForm(request.POST)

        print("FORM CLASS:", form.__class__)

        if form.is_valid():
            print("===== FORM IS VALID =====")
            form.save()
            return redirect("college:teacher_list")

    else:
        form = TeacherForm()

    return render(
        request,
        "teacher_form.html",
        {"form": form}
    )

@login_required
@admin_required
def teacher_update(request, i):
    teacher = Teacher.objects.get(id=i)
    if request.method == "POST":
        form = TeacherForm(request.POST,instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("college:teacher_list")
    else:
        form = TeacherForm(instance=teacher)
    return render(request,"teacher_form.html",{"form": form})

@login_required
@admin_required
def teacher_delete(request, teacher_id):

    teacher = get_object_or_404(
        Teacher,
        id=teacher_id
    )

    if request.method == "POST":
        teacher.delete()

        messages.success(
            request,
            f'Teacher "{teacher.user.username}" deleted successfully.'
        )

        return redirect("college:teacher_list")

    return redirect("college:teacher_list")

@login_required
@admin_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students':students})

@login_required
@admin_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("college:student_list")
    else:
        form = StudentForm()
    return render(request,"student_form.html",{"form": form})

@login_required
@admin_required
def student_update(request, i):
    student = Student.objects.get(id=i)
    if request.method == "POST":
        form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
            return redirect("college:student_list")
    else:
        form = StudentForm(instance=student)
    return render(request,"student_form.html",{"form": form})

@login_required
@admin_required
@login_required
def student_delete(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":
        student.delete()

        messages.success(
            request,
            f'Student "{student.user.username}" deleted successfully.'
        )

        return redirect("college:student_list")

    return redirect("college:student_list")

@login_required
@admin_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses':courses})

@login_required
@admin_required
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("college:course_list")
    else:
        form = CourseForm()
    return render(request,"course_form.html",{"form": form})

@login_required
@admin_required
def course_update(request, i):
    course = Course.objects.get(id=i)
    if request.method == "POST":
        form = CourseForm(request.POST,instance=course)
        if form.is_valid():
            form.save()
            return redirect("college:course_list")
    else:
        form = CourseForm(instance=course)
    return render(request,"course_form.html",{"form": form})

@login_required
@admin_required
def course_delete(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    if request.method == "POST":
        course.delete()

        messages.success(
            request,
            f'Course "{course.course_name}" deleted successfully.'
        )

        return redirect("college:course_list")

    return redirect("college:course_list")

@login_required
@admin_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects':subjects})

@login_required
@admin_required
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("college:subject_list")
    else:
        form = SubjectForm()
    return render(request,"subject_form.html",{"form": form})

@login_required
@admin_required
def subject_update(request, i):
    subject = Subject.objects.get(id=i)
    if request.method == "POST":
        form = SubjectForm(request.POST,instance=subject)
        if form.is_valid():
            form.save()
            return redirect("college:subject_list")
    else:
        form = SubjectForm(instance=subject)
    return render(request,"subject_form.html",{"form": form})

@login_required
@admin_required
def subject_delete(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    if request.method == "POST":
        subject.delete()

        messages.success(
            request,
            f'Subject "{subject.subject_name}" deleted successfully.'
        )

        return redirect("college:subject_list")

    return redirect("college:subject_list")

@login_required
@admin_required
def enrollment_list(request):
    enrollments = Enrollment.objects.select_related('student','course')
    return render(request,'enrollment_list.html',{'enrollments': enrollments})

@login_required
@admin_required
def enrollment_create(request):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Student enrolled successfully.")
            return redirect('college:enrollment_list')
    else:
        form = EnrollmentForm()
    return render(request,'enrollment_form.html',{'form': form})

@login_required
@admin_required
def enrollment_delete(request, enrollment_id):

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id
    )

    if request.method == "POST":
        enrollment.delete()

        messages.success(
            request,
            f'Enrollment "{enrollment.student} - {enrollment.course}" deleted successfully.'
        )

        return redirect("college:enrollment_list")

    return redirect("college:enrollment_list")

@login_required
@student_required
def my_subjects(request):
    student = get_object_or_404(
        Student,
        user=request.user
    )

    enrollments = (
        Enrollment.objects
        .filter(
            student=student,
            subject__isnull=False
        )
        .select_related(
            'course',
            'subject',
            'subject__course'
        )
        .order_by(
            'course__course_name',
            'subject__subject_name'
        )
    )

    return render(
        request,
        'student/my_subjects.html',
        {
            'enrollments': enrollments
        }
    )

@login_required
@teacher_required
def teacher_students(request):
    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    # Only students enrolled in subjects taught by this teacher
    enrollments = (
        Enrollment.objects
        .filter(subject__teacher=teacher)
        .select_related(
            'student',
            'subject',
            'course'
        )
        .order_by(
            'subject__subject_name',
            'student__user__first_name'
        )
    )

    return render(
        request,
        'teacher/students.html',
        {
            'enrollments': enrollments
        }
    )

@login_required
@teacher_required
def create_assignment(request, subject_id):

    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    # Security: teacher can only create assignments
    # for subjects assigned to them
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        teacher=teacher
    )

    if request.method == "POST":

        form = AssignmentForm(request.POST)

        if form.is_valid():

            assignment = form.save(commit=False)

            assignment.subject = subject

            assignment.save()

            return redirect('college:teacher_courses')

    else:

        form = AssignmentForm()

    today = timezone.localdate()
    return render(
        request,
        'teacher/create_assignment.html',
        {
            'form': form,
            'subject': subject,
            'today': today
        }
    )

@login_required
@teacher_required
def teacher_courses(request):

    teacher = Teacher.objects.get(
        user=request.user
    )

    subjects = Subject.objects.filter(
        teacher=teacher
    ).select_related(
        'course',
        'course__department'
    ).order_by(
        'course__course_name',
        'semester',
        'subject_name'
    )

    context = {
        'teacher': teacher,
        'subjects': subjects
    }

    return render(
        request,
        'teacher/courses.html',
        context
    )

@login_required
@student_required
def student_assignments(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    enrollments = Enrollment.objects.filter(
        student=student
    ).select_related(
        'course'
    ).prefetch_related(
        'course__subjects__assignments'
    )

    return render(
        request,
        'student/assignments.html',
        {
            'enrollments': enrollments
        }
    )

@login_required
@student_required
def submit_assignment(request, assignment_id):
    student = get_object_or_404(Student,user=request.user)
    assignment = get_object_or_404(Assignment,id=assignment_id)
    # Ensure the student is enrolled in the course
    enrolled = Enrollment.objects.filter(student=student,course=assignment.subject.course).exists()
    if not enrolled:
        messages.error(request,"You are not enrolled in this course.")
        return redirect("college:student_assignments")
    # Prevent duplicate submissions
    if Submission.objects.filter(assignment=assignment,student=student).exists():
        messages.warning(request,"You have already submitted this assignment.")
        return redirect("college:student_assignments")
    if request.method == "POST":
        form = SubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = student
            submission.save()
            messages.success(request,"Assignment submitted successfully.")
            return redirect("college:student_assignments")
    else:
        form = SubmissionForm()
    return render(request,"student/submit_assignment.html",{"form": form,"assignment": assignment})

@login_required
@teacher_required
def view_submissions(request, assignment_id):
    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        subject__teacher=teacher
    )

    submissions = Submission.objects.filter(
        assignment=assignment
    ).select_related(
        'student'
    )

    return render(
        request,
        'teacher/view_submissions.html',
        {
            'assignment': assignment,
            'submissions': submissions
        }
    )


@login_required
@teacher_required
def course_assignments(request, subject_id):

    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        teacher=teacher
    )

    assignments = Assignment.objects.filter(
        subject=subject
    ).order_by('due_date')

    return render(
        request,
        'teacher/course_assignments.html',
        {
            'subject': subject,
            'assignments': assignments
        }
    )


@login_required
@teacher_required
def edit_assignment(request, assignment_id):
    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        subject__teacher=teacher
    )

    if request.method == "POST":

        form = AssignmentForm(
            request.POST,
            instance=assignment
        )

        if form.is_valid():
            form.save()

            return redirect(
                'college:course_assignments',
                subject_id=assignment.subject_id
            )

    else:

        form = AssignmentForm(
            instance=assignment
        )

    return render(
        request,
        'teacher/edit_assignment.html',
        {
            'form': form,
            'assignment': assignment
        }
    )


@login_required
@teacher_required
def delete_assignment(request, assignment_id):

    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    assignment = get_object_or_404(
        Assignment,
        id=assignment_id,
        subject__teacher=teacher
    )

    if request.method == "POST":

        subject_id = assignment.subject.id

        assignment.delete()

        return redirect(
            'college:course_assignments',
            subject_id=subject_id
        )

    return render(
        request,
        'teacher/delete_assignment.html',
        {
            'assignment': assignment
        }
    )


@login_required
@teacher_required
def grade_submission(request, submission_id):

    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        assignment__subject__teacher=teacher
    )

    if request.method == "POST":

        form = GradeSubmissionForm(
            request.POST,
            instance=submission
        )

        if form.is_valid():

            graded = form.save(
                commit=False
            )

            graded.graded_at = timezone.now()

            graded.save()

            return redirect(
                'college:view_submissions',
                assignment_id=submission.assignment.id
            )

    else:

        form = GradeSubmissionForm(
            instance=submission
        )

    return render(
        request,
        'teacher/grade_submission.html',
        {
            'form': form,
            'submission': submission
        }
    )


@login_required
@student_required
def my_results(request):
    student = Student.objects.get(user=request.user)

    submissions = Submission.objects.filter(
        student=student
    ).select_related(
        "assignment",
        "assignment__subject",
        "assignment__subject__course"
    )

    return render(
        request,
        "student/results.html",
        {
            "submissions": submissions
        }
    )

from django.db.models import Q
from django.views import View
class SearchCourse(View):
    def post(self, request):
        query=request.POST['q']
        c=Course.objects.filter(Q(course_name__icontains=query)|Q(course_code__icontains=query)|Q(description__icontains=query))
        return render(request, 'search.html', {'courses':c})

import json
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from openai import OpenAI


import json

from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST

from .models import (
    Student,
    Teacher,
    Course,
    Enrollment,
    Assignment,
    Submission
)

@require_POST
def chatbot(request):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        data = json.loads(request.body)
        message = data.get("message", "").lower().strip()

        user = request.user

        # =====================================
        # CHECK IF USER IS A STUDENT
        # =====================================

        student = Student.objects.filter(user=user).first()

        # =====================================
        # CHECK IF USER IS A TEACHER
        # =====================================

        teacher = Teacher.objects.filter(user=user).first()


        # =====================================
        # STUDENT: MY COURSES
        # =====================================

        if student and (
            "my courses" in message
            or "what are my courses" in message
            or "show my courses" in message
            or "enrolled courses" in message
        ):

            enrollments = Enrollment.objects.filter(
                student=student
            ).select_related("course")

            if not enrollments.exists():

                response = "You are not enrolled in any courses yet."

            else:

                courses = [
                    enrollment.course.course_name
                    for enrollment in enrollments
                ]

                response = (
                    "You are enrolled in:<br>• "
                    + "<br>• ".join(courses)
                )

            return JsonResponse({"response": response})


        # =====================================
        # STUDENT: MY ASSIGNMENTS
        # =====================================

        if student and (
            "my assignments" in message
            or "show assignments" in message
            or "assignments" in message
        ):

            assignments = Assignment.objects.filter(
                course__enrollment__student=student
            ).select_related("course")

            if not assignments.exists():

                response = "You don't have any assignments."

            else:

                assignment_list = []

                for assignment in assignments:

                    assignment_list.append(
                        f"{assignment.title} ({assignment.course.course_name})"
                    )

                response = (
                    "Your assignments:<br>• "
                    + "<br>• ".join(assignment_list)
                )

            return JsonResponse({"response": response})


        # =====================================
        # STUDENT: MY RESULTS
        # =====================================

        if student and (
            "my results" in message
            or "my marks" in message
            or "show results" in message
            or "show marks" in message
        ):

            submissions = Submission.objects.filter(
                student=student
            ).select_related("assignment")

            if not submissions.exists():

                response = "No results are available yet."

            else:

                result_list = []

                for submission in submissions:

                    if submission.marks is not None:

                        result_list.append(
                            f"{submission.assignment.title}: "
                            f"{submission.marks} marks"
                        )

                if result_list:

                    response = (
                        "Your results:<br>• "
                        + "<br>• ".join(result_list)
                    )

                else:

                    response = (
                        "Your assignments have not been graded yet."
                    )

            return JsonResponse({"response": response})


        # =====================================
        # STUDENT: TEACHERS
        # =====================================

        if student and (
            "my teachers" in message
            or "who is my teacher" in message
            or "who are my teachers" in message
        ):

            courses = Course.objects.filter(
                enrollment__student=student
            ).select_related("teacher")

            if not courses.exists():

                response = "You are not enrolled in any courses."

            else:

                teacher_list = []

                for course in courses:

                    teacher_list.append(
                        f"{course.course_name}: {course.teacher}"
                    )

                response = (
                    "Your teachers:<br>• "
                    + "<br>• ".join(teacher_list)
                )

            return JsonResponse({"response": response})


        # =====================================
        # TEACHER: MY COURSES
        # =====================================

        if teacher and (
            "my courses" in message
            or "courses i teach" in message
            or "what courses do i teach" in message
        ):

            courses = Course.objects.filter(teacher=teacher)

            if not courses.exists():

                response = "You are not assigned to any courses."

            else:

                course_list = [
                    course.course_name
                    for course in courses
                ]

                response = (
                    "You teach:<br>• "
                    + "<br>• ".join(course_list)
                )

            return JsonResponse({"response": response})


        # =====================================
        # TEACHER: STUDENTS
        # =====================================

        if teacher and (
            "my students" in message
            or "show students" in message
            or "enrolled students" in message
        ):

            courses = Course.objects.filter(
                teacher=teacher
            )

            enrollments = Enrollment.objects.filter(
                course__in=courses
            ).select_related(
                "student",
                "course"
            )

            if not enrollments.exists():

                response = "No students are enrolled in your courses."

            else:

                student_list = []

                for enrollment in enrollments:

                    student_list.append(
                        f"{enrollment.student} "
                        f"({enrollment.course.course_name})"
                    )

                response = (
                    "Students enrolled in your courses:<br>• "
                    + "<br>• ".join(student_list)
                )

            return JsonResponse({"response": response})


        # =====================================
        # HELP / UNKNOWN QUESTION
        # =====================================

        response = """
        I can help you with course management! 🤖<br><br>

        Try asking:<br>
        • What are my courses?<br>
        • Show my assignments<br>
        • Who are my teachers?<br>
        • Show my results<br>
        • What courses do I teach?<br>
        • Show my students
        """

        return JsonResponse({"response": response})


    except Exception as e:

        print("CHATBOT ERROR:", str(e))

        return JsonResponse({
            "response": "Sorry, something went wrong. Please try again."
        }, status=500)

@login_required
@teacher_required
def select_course_attendance(request):

    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    subjects = Subject.objects.filter(
        teacher=teacher
    ).select_related('course')

    return render(
        request,
        'teacher/select_course_attendance.html',
        {
            'subjects': subjects
        }
    )

from django.urls import reverse
@login_required
@teacher_required
def mark_attendance(request, subject_id):

    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        teacher=teacher
    )

    enrollments = Enrollment.objects.filter(
        course=subject.course
    ).select_related("student")

    today = timezone.localdate()

    # Get selected date
    selected_date = (
        request.GET.get("date")
        or request.POST.get("date")
        or today.strftime("%Y-%m-%d")
    )

    # SAVE ATTENDANCE
    if request.method == "POST":

        for enrollment in enrollments:

            student = enrollment.student

            status = request.POST.get(
                f"status_{student.id}"
            )

            Attendance.objects.update_or_create(
                student=student,
                subject=subject,
                date=selected_date,
                defaults={
                    "status": status == "present"
                }
            )

        messages.success(
            request,
            "Attendance saved successfully."
        )

        # Return to same selected date
        return redirect(
            f"{request.path}?date={selected_date}"
        )

    # LOAD EXISTING ATTENDANCE
    attendance_records = Attendance.objects.filter(
        subject=subject,
        date=selected_date
    )

    attendance_dict = {
        attendance.student_id: attendance.status
        for attendance in attendance_records
    }

    context = {
        "subject": subject,
        "enrollments": enrollments,
        "attendance_dict": attendance_dict,
        "selected_date": selected_date,
        "today": today,
    }

    return render(
        request,
        "teacher/mark_attendance.html",
        context
    )

@login_required
@teacher_required
def attendance_history(request):

    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    subjects = Subject.objects.filter(
        teacher=teacher
    ).select_related(
        'course'
    ).order_by(
        'course__course_name',
        'semester',
        'subject_name'
    )

    return render(
        request,
        "teacher/attendance_history.html",
        {
            "subjects": subjects
        }
    )

@login_required
@teacher_required
def attendance_dates(request, subject_id):

    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    # Ensure this subject is assigned to the logged-in teacher
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        teacher=teacher
    )

    dates = Attendance.objects.filter(
        subject=subject
    ).values_list(
        "date",
        flat=True
    ).distinct().order_by("-date")

    return render(
        request,
        "teacher/attendance_dates.html",
        {
            "subject": subject,
            "dates": dates
        }
    )

from datetime import datetime


@login_required
@teacher_required
def attendance_detail(request, subject_id, date):

    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    # Ensure subject belongs to logged-in teacher
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        teacher=teacher
    )

    attendance_date = datetime.strptime(
        date,
        "%Y-%m-%d"
    ).date()

    attendances = Attendance.objects.filter(
        subject=subject,
        date=attendance_date
    ).select_related(
        "student"
    )

    return render(
        request,
        "teacher/attendance_detail.html",
        {
            "subject": subject,
            "attendance_date": attendance_date,
            "attendances": attendances
        }
    )

from django.db.models import Count

@login_required
@student_required
def my_attendance(request):
    student = get_object_or_404(
        Student,
        user=request.user
    )

    enrollments = (
        Enrollment.objects
        .filter(
            student=student,
            subject__isnull=False
        )
        .select_related(
            'course',
            'subject',
            'subject__course'
        )
    )

    attendance_data = []

    for enrollment in enrollments:

        subject = enrollment.subject

        total_classes = Attendance.objects.filter(
            student=student,
            subject=subject
        ).count()

        present_classes = Attendance.objects.filter(
            student=student,
            subject=subject,
            status=True
        ).count()

        absent_classes = total_classes - present_classes

        if total_classes > 0:
            percentage = (
                present_classes / total_classes
            ) * 100
        else:
            percentage = 0

        attendance_data.append({
            'course': enrollment.course,
            'subject': subject,
            'total_classes': total_classes,
            'present_classes': present_classes,
            'absent_classes': absent_classes,
            'percentage': round(percentage, 2)
        })

    return render(
        request,
        'student/my_attendance.html',
        {
            'attendance_data': attendance_data
        }
    )

def courses(request):
    c = Course.objects.all()
    return render(request, 'courses.html', {'courses':c})

def departments(request):
    d = Department.objects.all()
    return render(request, 'departments.html', {'departments':d})

def contact(request):
    return render(request, 'contact.html')

@login_required
@teacher_required
def teacher_profile(request):
    return render(request, 'teacher_profile.html')

@login_required
@student_required
def student_profile(request):
    return render(request, 'student_profile.html')

@login_required
@teacher_required
def edit_teacher_profile(request):
    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )
    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        teacher_form = TeacherProfileForm(
            request.POST,
            instance=teacher
        )

        if user_form.is_valid() and teacher_form.is_valid():

            user_form.save()
            teacher_form.save()

            return redirect('college:teacher_profile')

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        teacher_form = TeacherProfileForm(
            instance=teacher
        )

    return render(
        request,
        'edit_teacher_profile.html',
        {
            'user_form': user_form,
            'teacher_form': teacher_form
        }
    )

@login_required
@student_required
def edit_student_profile(request):

    student = Student.objects.get(user=request.user)

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        student_form = StudentProfileForm(
            request.POST,
            instance=student
        )

        if user_form.is_valid() and student_form.is_valid():

            user_form.save()
            student_form.save()

            return redirect('college:student_profile')

    else:

        user_form = UserUpdateForm(instance=request.user)

        student_form = StudentProfileForm(instance=student)

    return render(
        request,
        'edit_student_profile.html',
        {
            'user_form': user_form,
            'student_form': student_form
        }
    )

@login_required
@hod_required
def hod_dashboard(request):

    hod = get_object_or_404(
        HOD,
        user=request.user
    )

    subjects = Subject.objects.filter(
        course__department=hod.department
    ).select_related(
        'course',
        'teacher',
        'teacher__user'
    ).order_by(
        'course__course_name',
        'semester',
        'subject_name'
    )

    teachers = Teacher.objects.filter(
        department=hod.department
    ).select_related('user')

    return render(
        request,
        'hod_dashboard.html',
        {
            'hod': hod,
            'subjects': subjects,
            'teachers': teachers,
        }
    )

@login_required
@hod_required
def assign_subject(request, subject_id):

    # Get logged-in HOD
    hod = get_object_or_404(
        HOD,
        user=request.user
    )

    # Get subject only if it belongs to HOD's department
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        course__department=hod.department
    )

    # Get teachers only from HOD's department
    teachers = Teacher.objects.filter(
        department=hod.department
    )

    if request.method == "POST":

        teacher_id = request.POST.get("teacher")

        teacher = get_object_or_404(
            Teacher,
            id=teacher_id,
            department=hod.department
        )

        # Assign teacher to subject
        subject.teacher = teacher
        subject.save()

        teacher_name = (
            teacher.user.get_full_name()
            or teacher.user.username
        )

        messages.success(
            request,
            f"{subject.subject_name} has been assigned to "
            f"{teacher_name}."
        )

        return redirect("college:hod_dashboard")

    return render(
        request,
        "assign_subject.html",
        {
            "subject": subject,
            "teachers": teachers,
        })
