from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Learning, Time
from django.contrib import messages
from django.db.models import Count
from ..login_reg_app.views import print_messages


def index(request):                             #localhost redirects to login page
    return redirect('users:index')

def q_of_day(request):
    qod = Learning.objects.all()                          #Loads the quetion of the day after successful login
    context = {
        'page': qod[0],
    }
    return render(request, 'learning_app/q_of_day.html', context)

def q_of_day_answer(request, id):              #Checks answer to QofD based on ID and either returns error or redirects to seccess page, question_on gets -1 and success page will increment again
    if request.method == 'POST':
        if id == '1':
            if request.POST['answer'] == '3':
                user = User.objects.get(id=request.session['user']['id'])
                user.question_on = user.question_on - 1
                user.save()
                return redirect('learning:correct', id=2)
        if id == '2':
            if request.POST ['answer']== '4100':
                user = User.objects.get(id=request.session['user']['id'])
                user.question_on = user.question_on - 1
                user.save()
                return redirect('learning:correct', id=2)
        incorrect(request)
        return redirect('learning:q_of_day')

def correct(request, id):                           # adds stars for correct answer and loads correct page, increments question_on
    user = User.objects.get(id=request.session['user']['id'])
    if id == '1':
        Time.objects.end_time(user.id, user.question_on)
    user.stars = user.stars + 2
    user.question_on = user.question_on + 1
    user.save()
    return redirect('learning:correct_page')

def correct_page(request):                         #holder route to prevent refreshing browswer from getting student more stars
    user = User.objects.get(id=request.session['user']['id'])
    context={
        'user': user,
    }
    return render(request, 'learning_app/correct.html', context)

def progress(request):                          # checks what question student is on and loads complete page if done
    user = User.objects.get(id=request.session['user']['id'])
    context={
        'user': user,
    }
    if user.question_on == 7:
        return render(request, 'learning_app/complete.html', context)
    if user.question_on == 5:                   # if student is far enough ahead will load additional questions
        is_ahead = ahead_check(request, user)
        if not is_ahead:
            return render(request, 'learning_app/complete.html', context)
    valid = Time.objects.check_time(user.id, user.question_on)      #checks if student has already started next quesetion and sets created_at if not
    if not valid:
        Time.objects.start_time(user.id, user.question_on)
    return render(request, 'learning_app/third_grade.html', context)


def incorrect(request):                         # creates incorrect error and runs print_mesages
    errors = []
    errors.append("I am sorry but that is incorrect.  Please try again.")
    print_messages(request, errors)

def third_answer(request, id):                      # checks answer of third grade questions and either sends correct or incorrect
    if request.method == 'POST':
        if id == '1':
            if request.POST['answer'] == 'green,white,red,dark blue,orange,purple,black,pink,light blue,yellow':
                return redirect('learning:correct', id=1)
        if id == '2':
            if request.POST['answer'] == '25,15,45':
                return redirect('learning:correct', id=1)
        if id == '3':
            if request.POST['answer'] == '7:10':
                return redirect('learning:correct', id=1)
        if id == '4':
            if request.POST['answer'] == '3':
                return redirect('learning:correct', id=1)
        if id == '5':
            if request.POST['answer'] == '15':
                return redirect('learning:correct', id=1)
        if id == '6':
            if request.POST['answer'] == '120,35,80,70':
                return redirect('learning:correct', id=1)
        incorrect(request)
        return redirect('learning:progress')

def ahead_check(request, user):             #checks if student is far enough ahead of the class to load additional content
    students = User.objects.all()
    sum = 0
    count = 0
    for student in students:
        sum += student.question_on
        count += 1
    if user.question_on >= (sum/count+2):
        return True
    else:
        return False

def console(request):                   #checks if Learning db is emply and creates entry for QofD if needed - then loads admin console wilh all user info and question of the day.
    if User.objects.admin_exists():
        if 'user' not in request.session:
            return redirect('users:index')
        user = User.objects.get(id=request.session['user']['id'])
        if user.is_admin == False:
            return redirect('users:index')
    if Learning.objects.count() == 0:
        Learning.objects.create()
    qod = Learning.objects.all()
    context = {
        'page': qod[0],
        'students': User.objects.filter(is_admin=False),
        'qod': [1, 2],
    }
    return render(request, 'learning_app/admin.html', context)


def set_qofd(request, id):              #Sets QofD from drop down in admin console
    qod = Learning.objects.all()[0]
    qod.question_day = id
    qod.save()
    return redirect('learning:console')

def logout(request):                    #Logs user out of session
    request.session.clear()
    return redirect('users:index')

def student_detail(request, id):        #gets time taken per question for student selected as well as average time taken for all students
    student = User.objects.get(id=id)
    context = {
        'student_times': Time.objects.get_times(student),
        'average_times': sorted(Time.objects.avg_times().items()),
        'name': student.name,
    }
    return render(request, 'learning_app/student_detail.html', context)

def stuck(request):                     #When stumped button is clicked - generates list of students working on same quesitona and passes as messages
    student = User.objects.get(id=request.session['user']['id'])
    students = User.objects.filter(question_on=student.question_on).exclude(id=student.id).exclude(is_admin=True)
    errors = []
    for student in students:
        errors.append(student.name + " is also working on this problem. Perhaps you can work together.")
    print_messages(request, errors)
    return redirect('learning:progress')

def delete(request, id):
    User.objects.delete_user(id)
    return redirect('learning:console')
