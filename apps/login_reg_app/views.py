from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User



def index(request):
    return render(request, 'login_reg_app/index.html')

def login(request):
    if request.method == 'POST':
        valid = User.objects.login(request.POST)

        if valid[0] is False:
            print_messages(request, valid[1])
            return redirect('users:index')

        else:
            return success(request, valid[1])
    return redirect('users:index')

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.ERROR, message)

def success(request, user):
    request.session['user'] = {
        'id' : user.id,

    }
    return redirect(reverse('learning:q_of_day'))

def register(request):
    if request.method == 'POST':

        valid = User.objects.register(request.POST)

        if valid[0] is False:
            print_messages(request, valid[1])
            return redirect('learning:console')

        else:
            return redirect('learning:console')

def teacher_login(request):
    if request.method == 'POST':
        if not User.objects.admin_exists():
            return redirect('learning:console')
        else:
            valid = User.objects.login(request.POST)
            if valid[0] is False:
                print_messages(request, valid[1])
                return redirect('users:index')
            if valid[1].is_admin is False:
                errors = []
                errors.append("You do not have teacher privilages.")
                print_messages(request, errors)
                return redirect('users:index')
            else:
                request.session['user'] = {
                    'id' : valid[1].id,
                }
                return redirect('learning:console')
    else:
        return redirect('users:index')
