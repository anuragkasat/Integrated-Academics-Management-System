from django.contrib import admin
from django.db.models import Sum
from .models import Resource, Announcement, Mark, Course, Enrollment, Attendance

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'description']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['message', 'created_at', 'for_all', 'specific_student']

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['assignment_title', 'student', 'score', 'total_marks']
    readonly_fields = ['total_marks']

    def total_marks(self, obj):
        total = Mark.objects.filter(student=obj.student).aggregate(total_marks=Sum('score'))['total_marks']
        return total if total is not None else 0

    total_marks.short_description = 'Total Marks'
    total_marks.admin_order_field = 'total_marks'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'date', 'status']
