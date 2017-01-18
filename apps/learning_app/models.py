from django.db import models
from ..login_reg_app.models import User
import datetime
from django.db.models import Avg



class TimeManager(models.Manager):
    def check_time(self, student_id, question_on):
        if self.filter(student=User.objects.get(id=student_id)).filter(question=question_on):
            return True
        else:
            return False

    def start_time(self, student_id, question_on):
        self.create(student=User.objects.get(id=student_id), question=question_on, time_finished=datetime.datetime.now())

    def end_time(self, student_id, question_on):
        time = self.filter(student=User.objects.get(id=student_id)).filter(question=question_on)
        time2 = time[0]
        time2.time_finished = datetime.datetime.now()
        time2.is_done = True
        time2.save()


    def get_times(self, student):
        times = self.filter(student=student).order_by('question')
        student_times = []
        for time in times:
            student_times.append((time.time_finished - time.created_at).seconds)
        return student_times

    def avg_times(self):
        avg_times = {}
        questions = self.order_by().values('question').distinct()
        for number in questions:
            temp = Time.objects.filter(question=number['question']).filter(is_done=True).filter(student__is_admin=False)
            if temp:
                total = 0
                for entry in temp:
                    total += (entry.time_finished - entry.created_at).seconds
                avg_times[number['question']] = (total/len(temp))
        return avg_times



class Learning(models.Model):
    question_day = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def pic_url(self):
        return 'learning_app/img/q-of-day-'  +str(self.question_day) + '.png'

class Time(models.Model):
    student = models.ForeignKey('login_reg_app.User', related_name='time_taken')
    question = models.IntegerField()
    time_finished = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TimeManager()
