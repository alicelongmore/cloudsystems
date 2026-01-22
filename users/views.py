from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsernamePasswordResetForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your account has been created! You can now log in.'
            )
            return redirect('login')
        else:
            messages.warning(request, 'Unable to create account. Please correct the errors below.')
    else:
        form = UserRegisterForm()

    return render(
        request,
        'users/sign_up.html',
        {
            'form': form,
            'title': 'Student Registration'
        }
    )


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been successfully updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Student Profile',
    }
    return render(request, 'users/profile.html', context)

def username_password_reset(request):
    if request.method == 'POST':
        form = UsernamePasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password has been reset successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UsernamePasswordResetForm()
    return render(request, 'users/password_reset.html', {'form': form, 'title': 'Reset Password'})