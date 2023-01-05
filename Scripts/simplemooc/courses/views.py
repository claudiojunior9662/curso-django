from typing import Concatenate
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Comment
from .forms import ContactCourse, CommentForm

from .decorators import enrollment_required

def index(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    template_name = 'courses/index.html'
    return render(request, template_name, context)

def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
    context['form'] = form
    context['course'] = course
    template_name = 'courses/details.html'
    return render(request, template_name, context)

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(user = request.user, course = course)
    if created:
        # enrollment.active()
        messages.success(request, 'Você foi inscrito com sucesso!')
    else:
        messages.info(request, 'Você já está inscrito neste curso!')
    return redirect('accounts:dashboard')

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso!')
        return redirect('accounts:dashboard')
    template_name = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }
    return render(request, template_name, context)

@login_required
@enrollment_required
def announcements(request, slug):
    course = request.course
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    template_name = 'courses/announcements.html'
    return render(request, template_name, context)

@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcemment = announcement
        comment.save()
        form = CommentForm()
        messages.success(request, 'Seu comentário foi enviado com sucesso!')
    template = 'courses/show_announcement.html'
    context = { 'course': course, 'announcement': announcement, 'form': form }
    return render(request, template, context)
