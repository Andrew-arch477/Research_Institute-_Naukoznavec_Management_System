from django.http import HttpResponse
from django.template import loader
from members.models import Student, Teacher, Class, Subject, Schedule, Grade
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, DeleteView
from members.forms import StudentForm, TeacherForm, ScheduleForm, SubjectForm, ClassForm, GradeForm, Teacher_Login_Form

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


#Student

class Student_Create_View(LoginRequiredMixin, FormView):
    template_name = 'Student_2.html'
    form_class = StudentForm
    success_url = '/members/students_2/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Student.objects.all()
        return context

    def form_valid(self, form):
        
        try:
          Student.objects.create(
              name=form.cleaned_data['name'],
              surname=form.cleaned_data['surname'],
              class_hi_visits=form.cleaned_data['class_hi_visits']
          )
          return super().form_valid(form)
      
        except Class.DoesNotExist:
          form.add_error('class_hi_visits', 'Клас не знайдено')
          return self.form_invalid(form)

class Student_Update_View(LoginRequiredMixin, FormView):
    template_name = 'Student_Update.html'
    form_class = StudentForm
    success_url = '/members/students_2/'

    def form_valid(self, form):
        student_id = self.kwargs.get('pk')

        try:
            student = Student.objects.get(pk=student_id)
            student.name = form.cleaned_data['name']
            student.surname = form.cleaned_data['surname']
            student.class_hi_visits = form.cleaned_data['class_hi_visits']
            student.save()
            return super().form_valid(form)
        
        except Student.DoesNotExist:
            form.add_error(None, "Студента не знайдено.")
            return self.form_invalid(form)

class Student_Delete_View(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'Student_Delete.html'
    success_url = '/members/students_2/'

class Student_work(TemplateView):
  template_name = 'Student.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["students"] = Student.objects.all()
    return context

  def post(self, request):
    action = request.POST.get("action")

    if action == "add":
      return self.add_student(request)
    elif action == "delete":
      return self.delete_student(request)
    elif action == "update":
      return self.update_student(request)


  def add_student(self, request):
    name = request.POST.get("name")
    surname = request.POST.get("surname")
    class_hi_visits = request.POST.get("class_hi_visits")

    try:
      student_class = Class.objects.get(name=class_hi_visits)
      Student.objects.create(name=name, surname=surname, class_hi_visits=student_class)
      return HttpResponse("Учня додано!")
    except Class.DoesNotExist:
      return HttpResponse("Такого класу не існує!")

  def delete_student(self, request):
    name = request.POST.get("name")
    surname = request.POST.get("surname")
    class_hi_visits = request.POST.get("class_hi_visits")

    try:
      student_class = Class.objects.get(name=class_hi_visits)
      student = Student.objects.get(name=name, surname=surname, class_hi_visits=student_class)
      student.delete()
      return HttpResponse("Учня видалено!")
    except (Class.DoesNotExist, Student.DoesNotExist):
      return HttpResponse("Такого учня не існує!")

  def update_student(self, request):
    old_name = request.POST.get("old_name")
    old_surname = request.POST.get("old_surname")
    old_class_hi_visits = request.POST.get("old_class_hi_visits")

    new_name = request.POST.get("new_name")
    new_surname = request.POST.get("new_surname")
    new_class_hi_visits = request.POST.get("new_class_hi_visits")

    try:
      old_class = Class.objects.get(name=old_class_hi_visits)
      student = Student.objects.get(name=old_name, surname=old_surname, class_hi_visits=old_class)

      if new_class_hi_visits:
        new_class = Class.objects.get(name=new_class_hi_visits)
        student.class_hi_visits = new_class

      if new_name:
        student.name = new_name

      if new_surname:
        student.surname = new_surname

      student.save()
      return HttpResponse("Дані учня оновлено!")
    except (Class.DoesNotExist, Student.DoesNotExist):
      return HttpResponse("Такого учня або класу не існує!")

class Student_form_work(LoginRequiredMixin, FormView):
    template_name = 'Student_2.html'
    form_class = StudentForm
    success_url = "/members/students_2/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Student.objects.all()
        return context

    def form_valid(self, form):
        action = self.request.POST.get("action")

        if action == "add":
            return self.add_student(form)
        elif action == "update":
            return self.update_student(form)
        elif action == "delete":
            return self.delete_student()
        else:
            return HttpResponse("Невідома дія")

    def add_student(self, form):
      name = form.cleaned_data['name']
      surname = form.cleaned_data['surname']
      class_hi_visits = form.cleaned_data['class_hi_visits']

      try:
        Student.objects.create(
          name=name,
          surname=surname,
          class_hi_visits=class_hi_visits
        )
        return super().form_valid(form)

      except Class.DoesNotExist:
        form.add_error('class_hi_visits', 'Клас не знайдено')
        return self.form_invalid(form)

    def update_student(self, form, pk):
        try:
            student = Student.objects.get(id=pk)

            student.name = form.cleaned_data['name']
            student.surname = form.cleaned_data['surname']
            student.class_hi_visits = form.cleaned_data['class_hi_visits']

            student.save()
            return super().form_valid(form)
        except Student.DoesNotExist:
            form.add_error(None, "Student not found.")
            return self.form_invalid(form)
  
    def delete_student(self, student_id):
        try:
            student = Student.objects.get(pk=student_id)
            student.delete()
            return reverse_lazy(self.success_url)
        except Student.DoesNotExist:
            return HttpResponse("Student not found")

#Teacher

class Teacher_form_work(FormView):
  template_name = 'Teacher.html'
  form_class = TeacherForm
  success_url = "/members/teachers/"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["teachers"] = Teacher.objects.all()
    return context
  
  def post(self, form):
    action = self.request.POST.get("action")

    if action == "add":
      return self.add_teacher(form)
    elif action == "delete":
      return self.delete_teacher(form)
    elif action == "update":
      return self.update_teacher(form)

  def add_teacher(self, form):
    name = form.cleaned_data["name"]
    surname = form.cleaned_data["surname"]
    age = form.cleaned_data["age"]
    subject = form.cleaned_data["subject"]

    try:
      Teacher.objects.create(
        name=name,    
        surname=surname,
        age=age,
        subject=subject
        )
      return super().form_valid(form)
        
    except Subject.DoesNotExist:
      form.add_error('subject', 'Такого предмету не існує!')
      return self.form_invalid(form)

  def delete_teacher(self, form):
    name = form.cleaned_data["name"]
    surname = form.cleaned_data["surname"]
    age = form.cleaned_data["age"]
    subject = form.cleaned_data["subject"]

    try:
      teacher = Teacher.objects.get(
        name = name,
        surname = surname,
        age=age,
        subject=subject
        )
      teacher.delete()
      return super().form_valid(form)
    except Subject.DoesNotExist:
      return HttpResponse("Такого предмету не існує!")

  def update_teacher(self, request):
    old_name = request.POST.get("old_name")
    old_surname = request.POST.get("old_surname")
    old_age = request.POST.get("old_age")
    old_subject = request.POST.get("old_subject")

    new_name = request.POST.get("new_name")
    new_surname = request.POST.get("new_surname")
    new_age = request.POST.get("new_age")
    new_subject = request.POST.get("new_subject")

    try:
      old_subject = Subject.objects.get(name=old_subject)
      teacher = Teacher.objects.get(name=old_name, surname=old_surname, age=old_age, subject = old_subject)

      if new_subject:
        new_subject = Subject.objects.get(name=new_subject)
        teacher.subject = new_subject
                
      if new_name:
        teacher.name = new_name
                
      if new_surname:
        teacher.surname = new_surname
        
      if new_age:
        teacher.age = new_age
                
      teacher.save()
      return HttpResponse("Дані вчителя оновлено!")
    except (Subject.DoesNotExist, Teacher.DoesNotExist):
      return HttpResponse("Такого предмету або вчителя не існує!")

class Teacher_work(TemplateView):
  template_name = 'Teacher.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["teachers"] = Teacher.objects.all()
    return context
  
  def post(self, request):
    action = request.POST.get("action")

    if action == "add":
      return self.add_teacher(request)
    elif action == "delete":
      return self.delete_teacher(request)
    elif action == "update":
      return self.update_teacher(request)

  def add_teacher(self, request):
    name = request.POST.get("name")
    surname = request.POST.get("surname")
    age = request.POST.get("age")
    subject = request.POST.get("subject")

    try:
      teachers_subject = Subject.objects.get(name=subject)
      Teacher.objects.create(name=name, surname=surname, age=age, subject = teachers_subject)
      return HttpResponse("Вчителя додано!")
    except Subject.DoesNotExist:
      return HttpResponse("Такого предмету не існує!")

  def delete_teacher(self, request):
    name = request.POST.get("name")
    surname = request.POST.get("surname")
    age = request.POST.get("age")
    subject = request.POST.get("subject")

    try:
      teachers_subject = Subject.objects.get(name=subject)
      teacher = Teacher.objects.get(name=name, surname=surname, age=age, subject = teachers_subject)
      teacher.delete()
      return HttpResponse("Вчителя видалено!")
    except Subject.DoesNotExist:
      return HttpResponse("Такого предмету не існує!")

  def update_teacher(self, form):
      old_name = self.request.POST.get("old_name")
      old_surname = self.request.POST.get("old_surname")
      old_age = self.request.POST.get("old_age")
      old_subject_name = self.request.POST.get("old_subject")

      try:
          old_subject = Subject.objects.get(name=old_subject_name)
          teacher = Teacher.objects.get(
              name=old_name,
              surname=old_surname,
              age=old_age,
              subject=old_subject
              )

          teacher.name = form.cleaned_data['name']
          teacher.surname = form.cleaned_data['surname']
          teacher.age = form.cleaned_data['age']
          teacher.subject = form.cleaned_data['subject']

          teacher.save()
          return super().form_valid(form)

      except (Subject.DoesNotExist, Teacher.DoesNotExist):
        return HttpResponse("Помилка: вчитель або предмет не знайдені")

#Subject

class Subject_form_work(FormView):
    template_name = 'Subject.html'
    form_class = SubjectForm
    success_url = "/members/subjects/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subjects"] = Subject.objects.all()
        return context

    def form_valid(self, form):
        action = self.request.POST.get("action")

        if action == "add":
            return self.add_subject(form)
        elif action == "update":
            return self.update_subject(form)
        elif action == "delete":
            return self.delete_subject(form)
        else:
            return HttpResponse("Невідома дія")

    def add_subject(self, form):
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']

        Subject.objects.create(name=name, description=description)
        return super().form_valid(form)

    def delete_subject(self, form):
        name = form.cleaned_data['name']

        try:
            subject = Subject.objects.get(name=name)
            subject.delete()
            return super().form_valid(form)
        except Subject.DoesNotExist:
            return HttpResponse("Такого предмету не існує!")

    def update_subject(self, form):
        old_name = self.request.POST.get("old_name")
        new_name = form.cleaned_data['name']
        new_description = form.cleaned_data['description']

        try:
            subject = Subject.objects.get(name=old_name)

            subject.name = new_name
            subject.description = new_description
            subject.save()

            return super().form_valid(form)
        except Subject.DoesNotExist:
            return HttpResponse("Такого предмету не існує!")

class Subject_work(TemplateView):
  template_name = 'Subject.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["subjects"] = Subject.objects.all()
    return context
  
  def post(self, request):
    action = request.POST.get("action")

    if action == "add":
      return self.add_subject(request)
    elif action == "delete":
      return self.delete_subject(request)
    elif action == "update":
      return self.update_subject(request)

  def add_subject(self, request):

    name = request.POST.get("name")
    description = request.POST.get("description")

    Subject.objects.create(name=name, description=description)
    return HttpResponse("Предмет додано!")

  def delete_subject(self, request):

    name = request.POST.get("name")

    try:
      subject = Subject.objects.get(name=name)
      subject.delete()
      return HttpResponse("Предмет видалено!")
    except Subject.DoesNotExist:
      return HttpResponse("Такого предмету не існує!")

  def update_subject(self, request):

    old_name = request.POST.get("old_name")

    new_name = request.POST.get("new_name")
    new_description = request.POST.get("new_description")

    try:
      subject = Subject.objects.get(name=old_name)
                
      if new_name:
        subject.name = new_name
                
      if new_description:
        subject.description = new_description

                
      subject.save()
      return HttpResponse("Дані предмету оновлено!")
    except Subject.DoesNotExist:
      return HttpResponse("Такого предмету не існує!")

#Grade

class Grade_Create_View(LoginRequiredMixin, FormView):
    template_name = 'Grade.html'
    form_class = GradeForm
    success_url = '/members/grades/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grades"] = Grade.objects.all()
        return context

    def form_valid(self, form):
        
        Grade.objects.create(
          student = form.cleaned_data["student"],
          subject = form.cleaned_data["subject"],
          score = form.cleaned_data["score"],
          date = form.cleaned_data["date"]
        )
        return super().form_valid(form)

class Grade_Update_View(LoginRequiredMixin, FormView):
    template_name = 'Grade_Update.html'
    form_class = GradeForm
    success_url = '/members/grades/'

    def form_valid(self, form):
        subject_id = self.kwargs.get('pk')

        try:
            subject = Subject.objects.get(pk=subject_id)
            subject.name = form.cleaned_data['name'],
            subject.description = form.cleaned_data['description']
            subject.save()
            return super().form_valid(form)
        
        except Subject.DoesNotExist:
            form.add_error(None, "Предмета не знайдено.")
            return self.form_invalid(form)

class Grade_Delete_View(LoginRequiredMixin, DeleteView):
    model = Grade
    template_name = 'Grade_Delete.html'
    success_url = '/members/grades/'

class Grade_form_work(FormView):
    template_name = 'Grade.html'
    form_class = GradeForm 
    success_url = "/members/grades/"

    def form_valid(self, form):
        action = self.request.POST.get("action")

        if action == "add":
            return self.add_grade(form)
        elif action == "update":
            return self.update_grade(form)
        elif action == "delete":
            return self.delete_grade(form)
        else:
            return HttpResponse("Невідома дія")

    def add_grade(self, form):
        student = form.cleaned_data["student"]
        subject = form.cleaned_data["subject"]
        score = form.cleaned_data["score"]
        date = form.cleaned_data["date"]

        Grade.objects.create(student=student, subject=subject, score=score, date=date)
        return super().form_valid(form)

    def delete_grade(self, form):
        student = form.cleaned_data["student"]
        subject = form.cleaned_data["subject"]
        score = form.cleaned_data["score"]
        date = form.cleaned_data["date"]

        try:
            grade = Grade.objects.get(student=student, subject=subject, score=score, date=date)
            grade.delete()
            return super().form_valid(form)
        except Grade.DoesNotExist:
            return HttpResponse("Такої оцінки не існує!")

    def update_grade(self, form):
        student = form.cleaned_data["student"]
        subject = form.cleaned_data["subject"]
        old_score = self.request.POST.get("old_score")  # still from POST because not in form
        date = form.cleaned_data["date"]
        new_score = form.cleaned_data["score"]

        try:
            grade = Grade.objects.get(student=student, subject=subject, score=old_score, date=date)
            grade.score = new_score
            grade.save()
            return super().form_valid(form)
        except Grade.DoesNotExist:
            return HttpResponse("Такої оцінки не існує!")

class Grade_work(TemplateView):
  template_name = 'Grade.html'

  def post(self, request):
    action = request.POST.get("action")

    if action == "add":
      return self.add_grade(request)
    elif action == "delete":
      return self.delete_grade(request)
    elif action == "update":
      return self.update_grade(request)

  def add_grade(self, request):

    student_name = request.POST.get("student")
    subject_name = request.POST.get("subject")
    score = request.POST.get("score")
    date = request.POST.get("date")
      
    try:
      grade_subject = Subject.objects.get(name=subject_name)
      grade_student = Student.objects.get(name=student_name)
      Grade.objects.create(student=grade_student, subject=grade_subject, score=score, date=date)
      return HttpResponse("Оцінку додано!")
    except (Subject.DoesNotExist, Student.DoesNotExist):
      return HttpResponse("Такого студента або предмета не існує!")

  def delete_grade(self, request):
    student_name = request.POST.get("student")
    subject_name = request.POST.get("subject")
    score = request.POST.get("score")
    date = request.POST.get("date")
      
    try:
      grade_student = Student.objects.get(name=student_name)
      grade_subject = Subject.objects.get(name=subject_name)
      grade = Grade.objects.get(student=grade_student, subject=grade_subject, score=score, date=date)
      grade.delete()
      return HttpResponse("Оцінку видалено!")
    except (Grade.DoesNotExist, Student.DoesNotExist, Subject.DoesNotExist):
      return HttpResponse("Такої оцінки, учня або предмета не існує!")

  def update_grade(self, request):
    student_name = request.POST.get("student")
    subject_name = request.POST.get("subject")
    old_score = request.POST.get("old_score")
    date = request.POST.get("date")

    new_score = request.POST.get("new_score")

    try:
      student = Student.objects.get(name = student_name)
      subject = Subject.objects.get(name = subject_name)
      grade = Grade.objects.get(student= student, subject= subject, score= old_score, date=date)

      if new_score:
        grade.score = new_score

        grade.save()
        return HttpResponse("Оцінку оновлено!")
    except (Grade.DoesNotExist, Student.DoesNotExist, Subject.DoesNotExist):
        return HttpResponse("Такої оцінки, учня або предмета не існує!")

#Class

class Class_form_work(FormView):
    template_name = 'Class.html'
    form_class = ClassForm
    success_url = "/members/classes/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["classes"] = Class.objects.all()
        return context

    def form_valid(self, form):
        action = self.request.POST.get("action")

        if action == "add":
            return self.add_class(form)
        elif action == "update":
            return self.update_class(form)
        elif action == "delete":
            return self.delete_class(form)
        else:
            return HttpResponse("Невідома дія")

    def add_class(self, form):
        name = form.cleaned_data["name"]
        year = form.cleaned_data["year"]
        Class.objects.create(name=name, year=year)
        return super().form_valid(form)

    def delete_class(self, form):
        name = form.cleaned_data["name"]
        try:
            class_obj = Class.objects.get(name=name)
            class_obj.delete()
            return super().form_valid(form)
        except Class.DoesNotExist:
            return HttpResponse("Такого класу не існує!")

    def update_class(self, form):
        name = self.request.POST.get("name")  # Old name to find class
        new_name = form.cleaned_data["name"]  # New name from form
        new_year = form.cleaned_data["year"]

        try:
            class_obj = Class.objects.get(name=name)
            if new_name:
                class_obj.name = new_name
            if new_year:
                class_obj.year = new_year
            class_obj.save()
            return super().form_valid(form)
        except Class.DoesNotExist:
            return HttpResponse("Такого класу не існує!")

class Class_work(TemplateView):
  template_name = 'Class.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["classes"] = Class.objects.all()
    return context
  
  def post(self, request):
    action = request.POST.get("action")

    if action == "add":
      return self.add_class(request)
    elif action == "delete":
      return self.delete_class(request)
    elif action == "update":
      return self.update_class(request)

  def add_class(self, request):
    name = request.POST.get("name")
    year = request.POST.get("year")


    Class.objects.create(name=name, year=year)
    return HttpResponse("Клас додано!")


  def delete_class(self, request):
    name = request.POST.get("name")

    try:
      class_d = Class.objects.get(name=name)
      class_d.delete()
      return HttpResponse("Клас видалено!")
    except (Class.DoesNotExist):
      return HttpResponse("Такого класу не існує!")

  def update_class(self, request):
    name = request.POST.get("name")

    new_name = request.POST.get("new_name")

    try:
      class_u = Class.objects.get(name=name)

      if new_name:
        class_u.name = new_name

      class_u.save()
      return HttpResponse("Дані класу оновлено!")
    except (Class.DoesNotExist, Student.DoesNotExist):
      return HttpResponse("Такого учня або класу не існує!")

#Schedule

class Schedule_work(FormView):
    template_name = 'Schedule.html'
    form_class = ScheduleForm
    success_url = '/schedule/'  # redirect or update this as needed

    def form_valid(self, form):
        action = self.request.POST.get("action")

        if action == "add":
            return self.add_schedule(form)
        elif action == "delete":
            return self.delete_schedule(form)
        elif action == "update":
            return self.update_schedule(form)

        return HttpResponse("Невідома дія!")

    def add_schedule(self, form):
        Schedule.objects.create(
            day=form.cleaned_data["day"],
            time=form.cleaned_data["time"],
            subject=form.cleaned_data["subject"],
            class_assigned=form.cleaned_data["class_assigned"],
            teacher=form.cleaned_data["teacher"]
        )
        return HttpResponse("Урок додано!")

    def delete_schedule(self, form):
        try:
            schedule = Schedule.objects.get(
                day=form.cleaned_data["day"],
                time=form.cleaned_data["time"],
                subject=form.cleaned_data["subject"],
                class_assigned=form.cleaned_data["class_assigned"],
                teacher=form.cleaned_data["teacher"]
            )
            schedule.delete()
            return HttpResponse("Урок видалено!")
        except Schedule.DoesNotExist:
            return HttpResponse("Такий урок не знайдено!")

    def update_schedule(self, form):
        old_day = self.request.POST.get("old_day")
        old_time = self.request.POST.get("old_time")
        old_teacher_name = self.request.POST.get("old_teacher")

        try:
            old_teacher = Teacher.objects.get(name=old_teacher_name)
            schedule = Schedule.objects.get(
                day=old_day,
                time=old_time,
                subject=form.cleaned_data["subject"],
                class_assigned=form.cleaned_data["class_assigned"],
                teacher=old_teacher
            )

            # Update only if fields are filled
            new_day = form.cleaned_data.get("day")
            new_time = form.cleaned_data.get("time")
            new_teacher = form.cleaned_data.get("teacher")

            if new_day:
                schedule.day = new_day
            if new_time:
                schedule.time = new_time
            if new_teacher:
                schedule.teacher = new_teacher

            schedule.save()
            return HttpResponse("Дані уроку оновлено!")

        except (Teacher.DoesNotExist, Schedule.DoesNotExist):
            return HttpResponse("Старий запис уроку не знайдено!")

class Schedule_work(TemplateView):
  template_name = 'Schedule.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["schedules"] = Schedule.objects.all()
    return context
  
  def post(self, request):
    action = request.POST.get("action")

    if action == "add":
      return self.add_schedule(request)
    elif action == "delete":
      return self.delete_schedule(request)
    elif action == "update":
      return self.update_schedule(request)

  def add_schedule(self, request):

    day = request.POST.get("day")
    time = request.POST.get("time")
    subject = request.POST.get("subject")
    class_assigned = request.POST.get("class_assigned")
    teacher = request.POST.get("teacher")

    try:
      class_assigned_ = Class.objects.get(name=class_assigned)
      subject_ = Subject.objects.get(name=subject)
      teacher_ = Teacher.objects.get(name=teacher)
      Schedule.objects.create(day=day, time=time, subject=subject_, class_assigned=class_assigned_, teacher=teacher_)
      return HttpResponse("Урок додано!")

    except (Class.DoesNotExist, Subject.DoesNotExist, Teacher.DoesNotExist):
      return HttpResponse("Такого класу, предмету, вчителя не існує!")


  def delete_schedule(self, request):
      day = request.POST.get("day")
      time = request.POST.get("time")
      subject = request.POST.get("subject")
      class_assigned = request.POST.get("class_assigned")
      teacher = request.POST.get("teacher")

      try:
        class_assigned_d = Class.objects.get(name=class_assigned)
        subject_d = Subject.objects.get(name=subject)
        teacher_d = Teacher.objects.get(name=teacher)
        schedule = Schedule.objects.get(day=day, time=time, subject=subject_d, class_assigned=class_assigned_d ,teacher=teacher_d, )
        schedule.delete()
        return HttpResponse("Урок видалено!")
      except (Class.DoesNotExist, Subject.DoesNotExist, Teacher.DoesNotExist, Schedule.DoesNotExist):
        return HttpResponse("Такого класу, предмету, вчителя, або уроку не існує!")

  def update_schedule(self, request):
    old_day = request.POST.get("old_day")
    old_time = request.POST.get("old_time")
    subject = request.POST.get("subject")
    class_assigned = request.POST.get("class_assigned")
    old_teacher = request.POST.get("old_teacher")

    new_day = request.POST.get("new_day")
    new_time = request.POST.get("new_time")
    new_teacher = request.POST.get("new_teacher")

    try:
      old_teacher = Teacher.objects.get(name=old_teacher)
      schedule = Schedule.objects.get(day=old_day, time=old_time, subject=subject, class_assigned=class_assigned, teacher=old_teacher)

      if new_teacher:
        new_teacher = Teacher.objects.get(name=new_teacher)
        schedule.teacher = new_teacher
                
      if new_day:
        schedule.day = new_day
                
      if new_time:
        schedule.time = new_time
                
      schedule.save()
      return HttpResponse("Дані уроку оновлено!")
    except (Teacher.DoesNotExist, Schedule.DoesNotExist):
      return HttpResponse("Такого вчителя або уроку не існує!")

#Login

class _LoginView(FormView):
    template_name = 'login.html'
    form_class = Teacher_Login_Form
    success_url = reverse_lazy('home')  # Після успішного входу переходимо на домашню сторінку

    def form_valid(self, form):
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']

        # age = form.cleaned_data["age"]
        # subject = form.cleaned_data["subject"]
        
        name = form.cleaned_data["name"]
        surname = form.cleaned_data["surname"]
        input_password = form.cleaned_data['password']

        try:
            teacher = Teacher.objects.get(name=name, surname=surname)

            if not check_password(input_password, teacher.password):
                form.add_error(None, "Неправильний пароль.")
                return self.form_invalid(form)

            if not teacher.user:
                user = User.objects.create_user(
                    username=f"{name}_{surname}",
                    password=input_password,
                    first_name=name,
                    last_name=surname
                )
                teacher.user = user
                teacher.save()

            login(self.request, teacher.user)
            return super().form_valid(form)

        except Teacher.DoesNotExist:
            form.add_error(None, "Викладача не знайдено.")
            return self.form_invalid(form)

#Home pages

class Home_Work_View(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

class Home_School_Page_View(TemplateView):
    template_name = 'School_Home_Page.html'




