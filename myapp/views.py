from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from .forms import StudentSignUpForm
from .models import Resource, Mark, Announcement, Enrollment, Attendance
import datetime
from django.db.models import Sum

def my_login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        else:
            return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def home_view(request):
    resources = Resource.objects.all()
    marks = Mark.objects.filter(student=request.user)
    total_marks = marks.aggregate(total_marks=Sum('score'))['total_marks']
    announcements = (Announcement.objects.filter(for_all=True) | Announcement.objects.filter(
        specific_student=request.user)).order_by('-created_at')

    # Fetch course enrollment for the current user
    enrollments = Enrollment.objects.filter(student=request.user)

    # Fetch attendance records for the current user
    today = datetime.date.today()
    attendance = Attendance.objects.filter(student=request.user, date=today)

    context = {
        'user': request.user,
        'welcome_message': "STUDENT PORTAL",
        'resources': resources,
        'marks': marks,
        'total_marks': total_marks,
        'announcements': announcements,
        'enrollments': enrollments,
        'attendance': attendance,
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = StudentSignUpForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
