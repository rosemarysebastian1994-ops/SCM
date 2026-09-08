from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class HOD(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    department = models.OneToOneField(
        Department,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    admission_no = models.CharField(max_length=20, unique=True)
    year = models.IntegerField()

    phone = models.CharField(max_length=15)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Course(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    course_name = models.CharField(max_length=100)

    course_code = models.CharField(max_length=20)

    description = models.TextField()

    credits = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course_name', 'department'],
                name='unique_course_per_department'
            )
        ]

    def __str__(self):
        return f"{self.course_name} - {self.department.name}"

class Subject(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20, default=0)
    description = models.TextField(blank=True)
    semester = models.CharField(max_length=20, default="S1")
    credits = models.IntegerField(default=100)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects'
    )
    class Meta:
        ordering = ['semester']
        constraints = [models.UniqueConstraint(fields=['course', 'subject_name'], name='unique_subject_per_course')]

    def __str__(self):
        return self.subject_name

class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)

    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course'
            )
        ]

    # class Meta:
    #     unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} - {self.course}"

class Assignment(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='assignments')

    title = models.CharField(max_length=200)

    description = models.TextField()

    due_date = models.DateTimeField()

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    file = models.FileField(upload_to="submissions/")

    submitted_on = models.DateTimeField(auto_now_add=True)

    marks = models.IntegerField(null=True, blank=True)

    feedback = models.TextField(
        blank=True
    )

    graded_at = models.DateTimeField(
        null=True,
        blank=True
    )

class Attendance(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    date = models.DateField()

    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date}"
