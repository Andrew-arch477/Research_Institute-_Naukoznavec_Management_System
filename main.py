import django
import os

# Налаштування Django для роботи поза середовищем сервера
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()


from members.models import Subject, Teacher, Class, Student, Schedule, Grade


while True:
    a = input("Що ви хочете зробити? 1-додати учня, 2-додати вчителя, 3-додати предмет, 4-додати клас, 5-додати урок до розкладу, 6-додати оцінку \n"
    "7-подивитися учнів, 8-подивитися вчителя, 9-подивитися предмети, 10-подивитися класи, 11-подивитися розклад, 12-подивитися оцінки \n "
    "13-видалити учня, 14-видалити вчителя, 15-видалити предмет, 16-видалити клас, 17-видалити урок з розкладу, 18-видалити оцінку \n"
    "19-оновити учня, 20-оновити вчителя, 21-оновити предмет, 22-оновити клас, 23-оновити розклад, 24-оновити оцінку \n"
    "exit-Вийти \n")

    if a == "exit":
        break

    # add
    if a == "1":
        name = input("Ім'я:")
        surname = input("Прізвище:")
        class_hi_visits_name = input("Який клас відвідує учень:")

        try:
            class_hi_visits = Class.objects.get(name=class_hi_visits_name)
            student = Student(name=name, surname=surname, class_hi_visits=class_hi_visits)
            student.save()
            print("Учня додано.")
        except Class.DoesNotExist:
            print("Клас не існує.")

    if a == "2":
        name = input("Ім'я:")
        surname = input("Прізвище:")
        age = input("Вік:")
        subject = input("Предмет який викладає:")

        try:
            subject = Subject.objects.get(name=subject)
            teacher = Teacher(name=name, surname=surname, age = age, subject=subject)
            teacher.save()
            print("Вчителя додано.")
        except Subject.DoesNotExist:
            print("Предмет не існує.")


    if a == "3":
        name = input("Ім'я:")
        description = input("Опис (що на ньому викладається):")

        subject = Subject(name=name, description=description)
        subject.save()
        print("Предмет додано.")

    if a == "4":
        name = input("Ім'я:")
        year = int(input("Рік створення класу:"))


        class_ = Class(name=name, year=year)
        class_.save()
        print("Клас додано.")

    if a == "5":
        day = input("День:")
        time = int(input("Час (початку):"))
        subject_ = input("Предмет:")
        class_assigned = input("Який клас приймає участь:")
        teacher = input("Викладач:")

        try:
            subject = Subject.objects.get(name=subject_)
        except Subject.DoesNotExist:
            print("Предмет не знайдено.")
            exit()

        try:
            class_assigned = Class.objects.get(name=class_assigned)
        except Class.DoesNotExist:
            print("Клас не знайдено.")
            exit()

        try:
            teacher = Teacher.objects.get(surname=teacher)
        except Teacher.DoesNotExist:
            print("Викладача не знайдено.")
            exit()

            lesson = Schedule(subject=subject_, time=time, class_assigned=class_assigned, teacher=teacher)
            lesson.save()
            print("Урок додано.")

    if a == "6":
        date = input("День:")
        subject = input("Предмет:")
        score = input("Оцінка:")
        student = input("Учень:")

        try:
            subject = Subject.objects.get(name=subject)
        except Subject.DoesNotExist:
            print("Предмет не знайдено.")
            exit()

        try:
            student = Student.objects.get(name=student)
        except Student.DoesNotExist:
            print("Учня не знайдено.")
            exit()


            grade = Grade(student=student, subject = subject, score=score, date=date)
            grade.save()
            print("Оцінку додано.")

    #show
    if a == "7":
        print(Student.objects.all())

    if a == "8":
        print(Teacher.objects.all())

    if a == "9":
        print(Subject.objects.all())

    if a == "10":
        print(Class.objects.all())

    if a == "11":
        print(Schedule.objects.all())

    if a == "12":
        print(Grade.objects.all())

    # delete
    if a == "13":
        name = input("Ім'я:")
        surname = input("Прізвище:")

        try:
            student_to_delete = Student.objects.get(name = name, surname = surname)
            student_to_delete.delete()
            print("Учня видалено.")
        except Student.DoesNotExist:
            print("Учня не існує.")

    if a == "14":
        name = input("Ім'я:")
        surname = input("Прізвище:")

        try:
            teacher_to_delete = Teacher.objects.get(name = name, surname = surname)
            teacher_to_delete.delete()
            print("Вчителя видалено.")
        except Teacher.DoesNotExist:
            print("Вчителя не існує.")

    if a == "15":
        name = input("Ім'я:")

        try:
            subject_to_delete = Subject.objects.get(name = name)
            subject_to_delete.delete()
            print("Предмет видалено.")
        except Teacher.DoesNotExist:
            print("Предмету не існує.")

    if a == "16":
        name = input("Ім'я:")

        try:
            class_to_delete = Class.objects.get(name = name)
            class_to_delete.delete()
            print("Клас видалено.")
        except Teacher.DoesNotExist:
            print("Клас не існує.")


    if a == "17":
        day = input("День:")
        time = int(input("Час (початку):"))
        subject_ = input("Предмет:")

        try:
            schedule_to_delete = Schedule.objects.get(day = day, time = time, subject = subject_)
            schedule_to_delete.delete()
            print("Урок видалено.")
        except Schedule.DoesNotExist:
            print("Уроку не існує.")

    if a == "18":
        date = input("День:")
        subject = input("Предмет:")
        score = input("Оцінка:")
        student = input("Учень:")

        try:
            grade_to_delete = Schedule.objects.get(date = date, subject = subject, score = score, student = student)
            grade_to_delete.delete()
            print("Оцінку видалено.")
        except Grade.DoesNotExist:
            print("Оцінки не існує.")

    #refresh
    