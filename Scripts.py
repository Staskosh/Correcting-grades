import random

from datacenter.models import (
    Chastisement,
    Commendation,
    Lesson,
    Mark,
    Schoolkid,
)
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def define_schoolkid(schoolboy):
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolboy)
    return  schoolkid


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    schoolkid_chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    schoolkid_chastisement.delete()


def create_commendation(schoolkid, subject):
    text_samples=['Молодец!','Отлично!','Хорошо!','Гораздо лучше, чем я ожидал!','Ты меня приятно удивил!','Великолепно!','Прекрасно!','Ты меня очень обрадовал!','Именно этого я давно ждал от тебя!','Сказано здорово – просто и ясно!']
    text = random.choice(text_samples)
    subject_lessons = Lesson.objects.filter(year_of_study__contains='6', group_letter__contains='А',
                                         subject__title=subject)
    last_class=subject_lessons.order_by('date').first()
    subject = last_class.subject
    created = last_class.date
    teacher = last_class.teacher
    Commendation.objects.create(text=text, created=created, schoolkid=schoolkid, subject=subject, teacher=teacher)


try:
    schoolboy = input('Введите имя ученика')
    schoolkid = schoolkid_define(schoolboy)
    fix_mark = fix_marks(schoolkid)
    remove_chastisements = remove_chastisements(schoolkid)
    try:
        subject = input('Введите название предмета')
        create_commendation = create_commendation(schoolkid, subject)
    except (Lesson.ObjectDoesNotExist, Lesson.AttributeError):
        print("Не удалось найти предмет с таким именем или есть несколько предметов")
except (Schoolkid.ObjectDoesNotExist, Schoolkid.MultipleObjectsReturned):
    print("Не удалось найти ученика с таким именем или есть несколько учеников")

