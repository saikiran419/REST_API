from django.db import models
from django.contrib.auth.models import AbstractUser

# 1️⃣ Custom User Model with Role
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

# 2️⃣ Course Model
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'instructor'},
        related_name='courses'
    )
    students = models.ManyToManyField(
        User,
        through='Enrollment',
        related_name='enrolled_courses',
        limit_choices_to={'role': 'student'}
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 3️⃣ Module Model
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Module: {self.title} ({self.course.title})"

# 4️⃣ Lesson Model
class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    content = models.TextField()
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Lesson: {self.title} ({self.module.title})"

# 5️⃣ Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # prevents duplicate enrollments

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"