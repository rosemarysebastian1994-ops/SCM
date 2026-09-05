from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Department, Teacher, Student, Course, Enrollment, Assignment, Submission

class StudentRegistrationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select()
    )

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']

class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = [
            'title',
            'description',
            'due_date'
        ]

        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].input_formats = ['%Y-%m-%dT%H:%M']

class SubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = ['file']

class GradeSubmissionForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = [
            "marks",
            "feedback"
        ]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'phone', 'qualification', 'department'
        ]


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['admission_no', 'year', 'phone', 'department']