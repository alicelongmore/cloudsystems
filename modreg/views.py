from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from .models import Module
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse


def home(Request):
    return render(Request, 'modreg/home.html', {'title': 'Welcome'})

def about(Request):
    return render(Request, 'modreg/about.html', {'title': 'Welcome'})

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"""
        New enquiry received:

        Name: {name}
        Email: {email}
        Subject: {subject}

        Message:
        {message}
        """

        send_mail(
            subject=f"Student Enquiry: {subject}",
            message=full_message,
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=['alice.longmore2@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, "Your enquiry has been sent successfully!")
        return redirect('modreg:contact') 

    return render(request, 'modreg/contact.html', {'title': 'Contact'})


def modules(request):
    modules = Module.objects.all()
    context = {'modules': modules}
    return render(request, 'modreg/modules.html', context)

from .models import Module
def modules(request):
    daily_module = {'modules': Module.objects.all(), 'title': 'Modules'}
    return render(request, 'modreg/modules.html', daily_module)


@login_required
def toggle_module_registration(request, pk):
    module = get_object_or_404(Module, pk=pk)
    user = request.user

    # Must be available
    if not module.availability:
        messages.error(request, "You cannot register for this module as it is unavailable.")
        return redirect(module.get_absolute_url())

    # Check course eligibility
    user_groups = user.groups.all()
    module_groups = module.courses_registered.all()

    if not user_groups.intersection(module_groups):
        messages.error(request, "You are not enrolled on a course that offers this module.")
        return redirect(module.get_absolute_url())

    # Toggle registration
    if user in module.students.all():
        module.students.remove(user)
        messages.success(request, "You have unregistered from this module.")
    else:
        module.students.add(user)
        messages.success(request, "You have registered for this module.")

    return redirect(module.get_absolute_url())

@login_required
def my_registrations(request):
    user = request.user

    # User's course (only one allowed)
    course = user.groups.first()

    # Modules the user is registered for
    modules = Module.objects.filter(students=user)

    context = {
        'user_obj': user,
        'course': course,
        'modules': modules,
    }

    return render(request, 'modreg/my_registrations.html', context)

class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class PostListView(ListView):
    model = Module
    ordering = ['-code']
    template_name = 'modreg/modules.html'
    context_object_name = 'modules'
    paginate_by = 5 # Optional pagination
    
class PostDetailView(DetailView):
    model = Module
    template_name = 'modreg/module_detail.html'
    slug_field = 'code'
    slug_url_kwarg = 'code'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Module
    fields = ['name', 'code', 'credit', 'availability', 'description', 'category', 'courses_registered']
    template_name = 'modreg/module_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        # save ManyToMany field manually
        selected_groups = self.request.POST.getlist('courses_registered')
        if selected_groups:
            form.instance.courses_registered.set(selected_groups)
        return response

    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context

    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Module
    fields = ['name', 'code', 'credit', 'category', 'availability', 'description', 'courses_registered' ]
    
    def test_func(self):
        module = self.get_object()
        return self.request.user == module.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Module
    success_url = reverse_lazy('modreg:modules')
    
    def test_func(self):
        module = self.get_object()
        return self.request.user == module.author