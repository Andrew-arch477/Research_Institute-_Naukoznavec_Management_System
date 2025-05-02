from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model): 
    name = models.CharField(max_length = 30, unique=True)
    description = models.CharField(max_length = 100)


    def __str__(self): 
        return self.name 

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length = 30)
    surname = models.CharField(max_length = 30)
    age = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete = models.SET_NULL, null=True, blank=True)
    password = models.CharField(max_length = 300)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(age__gte=20), name="age_gte_20"),
            models.CheckConstraint(condition=models.Q(age__lte=80), name="age_lte_80"), 
        ]
  
    def __str__(self):
        return f"{self.name} {self.surname}"


class Class(models.Model): 
    name = models.CharField(max_length = 30, unique=True)
    year = models.IntegerField()
  
    def __str__(self):
        return f"{self.name}"

class Student(models.Model): 
    name = models.CharField(max_length = 100) 
    class_hi_visits = models.ForeignKey(Class, on_delete = models.SET_NULL, null=True, blank=True) 
    surname = models.CharField(max_length = 100)
  
    def __str__(self): 
        return f"{self.name} {self.surname}"
    
class Schedule(models.Model): 
    day = models.CharField(max_length=30)
    time = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True) 
    class_assigned = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True) 
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
  
    def __str__(self): 
        return f"{self.class_assigned} - {self.subject} on {self.day} at {self.time}"
    

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.PositiveIntegerField()
    date = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(score__gte=0), name="score_gte_0"),
            models.CheckConstraint(condition=models.Q(score__lte=12), name="score_lte_12"), 
        ]

    def __str__(self):
        return f"Name: {self.student}, Subject: {self.subject}, Grade: {self.score}"

# DISALLOWED_CHARACTERS_REGEX = r'[^@]+'  # Це дозволяє лише символи, які не є @

# class MyModel(models.Model):
#     name = models.CharField(max_length=100)

#     class Meta:
#         constraints = [
#             models.CheckConstraint(
#                 check=~models.F('name').regex(DISALLOWED_CHARACTERS_REGEX),
#                 name='no_at_symbol_in_name'
#             ),
#         ]







