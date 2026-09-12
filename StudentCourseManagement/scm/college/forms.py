from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Department, Teacher, Student, Course, Subject, Enrollment, Assignment, Submission, FeeStructure, \
    StudentFee, Payment
from django.utils import timezone

class StudentRegistrationForm(UserCreationForm):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        })
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )

    admission_no = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter admission number'
        })
    )

    year = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter year'
        })
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

class TeacherRegistrationForm(UserCreationForm):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        })
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )

    qualification = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter qualification'
        })
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter department name'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter department description',
                'rows': 4
            }),
        }

from django import forms
from .models import Teacher, Student


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['user'].widget.attrs.update({
            'class': 'form-select'
        })

        self.fields['department'].widget.attrs.update({
            'class': 'form-select'
        })

    def clean_user(self):
        user = self.cleaned_data.get('user')

        if user and Student.objects.filter(user=user).exists():
            raise forms.ValidationError(
                "This user is already registered as a Student."
            )

        return user

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'admission_no', 'year', 'phone', 'department']

        widgets = {'user': forms.Select(attrs={'class': 'form-select'}),
               'admission_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter admission number'}),
               'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter academic year'}),
               'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
               'department': forms.Select(attrs={'class': 'form-select'}), }

    def clean(self):
        cleaned_data = super().clean()

        user = cleaned_data.get("user")

        print("SELECTED USER:", user)

        if user:
            print(
                "IS STUDENT:",
                Student.objects.filter(user=user).exists()
            )

            if Student.objects.filter(user=user).exists():
                self.add_error(
                    "user",
                    "This user is already registered as a Teacher."
                )

        return cleaned_data


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

        widgets = {
            'department': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'course_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter course name',
                }
            ),

            'course_code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter course code',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter course description',
                    'rows': 4,
                }
            ),

            'credits': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter credits',
                    'min': 1,
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        course_name = cleaned_data.get('course_name')
        department = cleaned_data.get('department')

        if course_name and department:

            course_exists = Course.objects.filter(
                course_name__iexact=course_name.strip(),
                department=department
            ).exclude(
                pk=self.instance.pk
            ).exists()

            if course_exists:
                raise forms.ValidationError(
                    'A course with this name already exists in this department.'
                )

        return cleaned_data

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

        widgets = {
            'course': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'subject_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter subject name',
                }
            ),

            'subject_code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter subject code',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter subject description',
                    'rows': 4,
                }
            ),

            'semester': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'credits': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter credits',
                    'min': 1,
                }
            ),

            'teacher': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
        }

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'

        widgets = {
            'student': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'course': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'subject': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
        }

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
                attrs={'type': 'datetime-local',
                       'class': 'form-control'},
                format='%Y-%m-%dT%H:%M')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['due_date'].widget.attrs['min'] = (timezone.localtime().strftime('%Y-%m-%dT%H:%M'))

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']

        if due_date < timezone.now():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date

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

class FeeStructureForm(forms.ModelForm):

    semester = forms.ChoiceField(
        choices=[
            ('S1', 'Semester 1'),
            ('S2', 'Semester 2'),
            ('S3', 'Semester 3'),
            ('S4', 'Semester 4'),
            ('S5', 'Semester 5'),
            ('S6', 'Semester 6'),
            ('S7', 'Semester 7'),
            ('S8', 'Semester 8'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    class Meta:
        model = FeeStructure

        fields = [
            'course',
            'semester',
            'fee_name',
            'amount',
            'due_date',
            'description'
        ]

        widgets = {
            'course': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'fee_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Tuition Fee'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter amount',
                    'step': '0.01'
                }
            ),

            'due_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Optional description'
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        course = cleaned_data.get('course')
        semester = cleaned_data.get('semester')
        fee_name = cleaned_data.get('fee_name')

        if course and semester and fee_name:

            exists = FeeStructure.objects.filter(
                course=course,
                semester=semester,
                fee_name__iexact=fee_name.strip()
            ).exclude(
                pk=self.instance.pk
            ).exists()

            if exists:
                raise forms.ValidationError(
                    "This fee already exists for this course and semester."
                )

        return cleaned_data

class StudentFeeForm(forms.ModelForm):

    class Meta:
        model = StudentFee

        fields = [
            'student',
            'fee_structure',
            'payment_plan',
        ]

        widgets = {
            'student': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'fee_structure': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'payment_plan': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        student = cleaned_data.get('student')
        fee_structure = cleaned_data.get('fee_structure')

        if student and fee_structure:

            exists = StudentFee.objects.filter(
                student=student,
                fee_structure=fee_structure
            ).exclude(
                pk=self.instance.pk
            ).exists()

            if exists:
                raise forms.ValidationError(
                    "This fee has already been assigned to this student."
                )

        return cleaned_data

class PaymentForm(forms.ModelForm):

    class Meta:

        model = Payment

        fields = [
            'student_fee',
            'amount',
            'payment_method',
            'transaction_id',
            'remarks',
        ]

        widgets = {

            'student_fee': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0.01'
                }
            ),

            'payment_method': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'transaction_id': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter transaction ID'
                }
            ),

            'remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Optional remarks'
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        student_fee = cleaned_data.get('student_fee')
        amount = cleaned_data.get('amount')

        if student_fee and amount:

            if amount <= 0:

                raise forms.ValidationError(
                    "Payment amount must be greater than zero."
                )

            if amount > student_fee.balance:

                raise forms.ValidationError(
                    f"Payment cannot exceed the "
                    f"remaining balance of "
                    f"₹{student_fee.balance:.2f}."
                )

        return cleaned_data
