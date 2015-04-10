# coding: utf-8
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.utils import timezone
from homework_alert.models import User, UserHomework, Homework

class Command(BaseCommand):
    help = 'Send mail to alert user about unfinished homeworks'

    def notify(self, user, homeworks):
        homework_list = u''
        for homework in homeworks:
            homework_list += u'・[{}] {}\n'.format(homework.lecture, homework.name)
        message = u'''明日{}までに提出の課題のうち，以下の課題が未提出になっています．

{}
提出期限を確認し，遅れないように提出してください．
なお，既に提出した場合は
http://alert.hermite.jp/homework/
よりログインし，提出済みにチェックしてください．'''.format((datetime.date.today() + datetime.timedelta(1)).strftime('%m月%d日').decode('utf-8'), homework_list)
        send_mail('[hermite]未提出の課題通知', message, 'info@alert.hermite.jp', [user.email], fail_silently=False)
        print 'sent mail to {}'.format(user.email)

    def handle(self, *args, **options):
        for user in User.objects.all():
            homeworks = []
            for homework in Homework.objects.filter(deadline__gt=timezone.now(), deadline__lt=timezone.now()+datetime.timedelta(2)):
                if not homework.is_done(user.id):
                    homeworks.append(homework)
            if homeworks != []:
                self.notify(user, homeworks)
