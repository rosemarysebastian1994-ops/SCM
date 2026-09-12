from .models import Department, Student, Teacher

def menu_links(request):
    d= Department.objects.all()
    return {'links':d}

def user_profile(request):
    student = None
    teacher = None

    if request.user.is_authenticated:

        try:
            student = Student.objects.select_related(
                'user',
                'department'
            ).get(user=request.user)
        except Student.DoesNotExist:
            pass

        try:
            teacher = Teacher.objects.select_related(
                'user',
                'department'
            ).get(user=request.user)
        except Teacher.DoesNotExist:
            pass

    return {
        'logged_in_student': student,
        'logged_in_teacher': teacher,
    }