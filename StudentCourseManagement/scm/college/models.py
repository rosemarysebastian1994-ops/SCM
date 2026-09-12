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

    is_approved = models.BooleanField(default=False)

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

    is_approved = models.BooleanField(default=False)

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

class FeeStructure(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='fee_structures'
    )

    semester = models.CharField(
        max_length=20
    )

    fee_name = models.CharField(
        max_length=100
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    due_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'semester', 'fee_name'],
                name='unique_fee_structure'
            )
        ]

    def __str__(self):
        return (
            f"{self.course.course_name} - "
            f"{self.semester} - "
            f"{self.fee_name}"
        )

class StudentFee(models.Model):

    PAYMENT_PLAN_CHOICES = [
        ('QUARTERLY', 'Quarterly'),
        ('HALF_YEARLY', 'Half-Yearly'),
        ('YEARLY', 'Yearly'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='fees'
    )

    fee_structure = models.ForeignKey(
        FeeStructure,
        on_delete=models.CASCADE,
        related_name='student_fees'
    )

    payment_plan = models.CharField(
        max_length=20,
        choices=PAYMENT_PLAN_CHOICES,
        default='YEARLY'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'fee_structure'],
                name='unique_student_fee_structure'
            )
        ]

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.fee_structure}"
        )

    @property
    def amount_due(self):
        return self.fee_structure.amount

    @property
    def amount_paid(self):
        return sum(
            payment.amount
            for payment in self.payments.all()
        )

    @property
    def balance(self):
        return self.amount_due - self.amount_paid

    @property
    def installment_count(self):

        return {
            'QUARTERLY': 4,
            'HALF_YEARLY': 2,
            'YEARLY': 1,
        }[self.payment_plan]

    @property
    def installment_amount(self):
        return (
            self.amount_due /
            self.installment_count
        )

    @property
    def status(self):

        if self.amount_paid <= 0:
            return 'PENDING'

        if self.amount_paid < self.amount_due:
            return 'PARTIAL'

        return 'PAID'

class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
        ('BANK', 'Bank Transfer'),
        ('ONLINE', 'Online'),
    ]

    student_fee = models.ForeignKey(
        StudentFee,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return (
            f"{self.student_fee.student.user.username} - "
            f"₹{self.amount}"
        )

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
