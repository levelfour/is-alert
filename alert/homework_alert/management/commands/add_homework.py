# coding: utf-8
import re
import MySQLdb
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from homework_alert.models import Homework

class Command(BaseCommand):
    help = 'Scrape IS2015-Wiki and add homework'

    def handle(self, *args, **options):
        conn = MySQLdb.connect(db='wikidb', user='django', passwd='django-hermite')
        cur = conn.cursor()
        main_page_id = 1
        cur.execute("SELECT page_latest FROM page WHERE page_id = %s", main_page_id)
        rev_id = cur.fetchall()[0][0]
        cur.execute("SELECT rev_text_id FROM revision WHERE rev_id = %s", rev_id)
        text_id = cur.fetchall()[0][0]
        cur.execute("SELECT old_text FROM text WHERE old_id = %s", text_id)
        contents = cur.fetchall()[0][0]
        table = re.search(r'<table class="wikitable" id="alert">(.*?)</table>', contents, re.S).group()
        for tr in re.findall(r'<tr>(.*?)</tr>', table, re.S)[1:]:
            tds = re.findall(r'<td>(.*?)</td>', tr, re.S)
            deadline, lecture, name = tuple(tds)
            m = re.match(r'^(\d{1,2})/(\d{1,2})(\(.*?\))?(\s*(\d{2}):(\d{2})(:(\d{2}))?)?$', deadline)
            if not m is None:
                g = m.groups()
                g = map(lambda x: int(x) if str(x).isdigit() else 0, g)
                deadline = {'month': g[0], 'day': g[1], 'hour': g[4], 'min': g[5], 'sec': g[7]}
            if re.match(r'^\[\[.*\]\]$', lecture):
                lecture = lecture[2:-2]
            if re.match(r'^\[\[.*\]\]$', name):
                name = name[2:-2]
            try:
                homework = Homework.objects.get(lecture=lecture, name=name)
            except Homework.DoesNotExist as e:
                year = datetime.now().year
                if datetime.now().month > int(deadline['month']) + 1:
                    year += 1
                date = datetime(year, deadline['month'], deadline['day'], deadline['hour'], deadline['min'], deadline['sec'])
                Homework.objects.create(lecture=lecture, name=name, deadline=timezone.make_aware(date, timezone.get_current_timezone()))
                print u'Add [{}] {}'.format(lecture, name)
