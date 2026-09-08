from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def role_required(role_name):
    """
    Generic decorator to restrict access based on Django Group.
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            # Superuser/Admin access
            if role_name == "Admin" and request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Group-based access
            if request.user.groups.filter(name=role_name).exists():
                return view_func(request, *args, **kwargs)

            raise PermissionDenied

        return wrapper

    return decorator


def teacher_required(view_func):
    return role_required("Teacher")(view_func)


def student_required(view_func):
    return role_required("Student")(view_func)


def hod_required(view_func):
    return role_required("HOD")(view_func)


def admin_required(view_func):
    return role_required("Admin")(view_func)