from django.db import models
from django.contrib.auth.models import User

class Resource(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Announcement(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    for_all = models.BooleanField(default=True)
    specific_student = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.for_all:
            return f"BROADCAST: {self.message[:50]}..."
        else:
            return f"To {self.specific_student.username}: {self.message[:50]}..."

class MarkQuerySet(models.QuerySet):
    def total_marks(self):
        from django.db.models import Sum
        return self.aggregate(total_marks=Sum('score'))['total_marks']

class MarkManager(models.Manager):
    def get_queryset(self):
        return MarkQuerySet(self.model, using=self._db)

    def total_marks(self):
        return self.get_queryset().total_marks()

class Mark(models.Model):
    GRADE_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_title = models.CharField(max_length=255)
    score = models.IntegerField()
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True, null=True)

    objects = MarkManager()

    def calculate_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 80:
            return 'B'
        elif self.score >= 70:
            return 'C'
        elif self.score >= 60:
            return 'D'
        else:
            return 'F'

    def save(self, *args, **kwargs):
        if not self.grade:
            self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.assignment_title} - {self.student.username} ({self.score}) - Grade: {self.grade}"
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title} at {self.enrolled_at}"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.date} - {self.status}"

