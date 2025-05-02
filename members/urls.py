from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('students/', views.Student_form_work.as_view(), name='student'),
    path('students_2/', views.Student_Create_View.as_view(), name='student2'),
    path('students_update/<str:pk>', views.Student_Update_View.as_view(), name='students_update'),
    path('students_delete/<str:pk>', views.Student_Delete_View.as_view(), name='students_delete'),

    path('teachers/', views.Teacher_form_work.as_view(), name='teacher'),

    path('subjects/', views.Subject_form_work.as_view(), name='subject'),
    path('subjects_update/<str:pk>', views.Student_Update_View.as_view(), name='subjects_update'),
    path('subjects_delete/<str:pk>', views.Student_Delete_View.as_view(), name='subjects_delete'),

    path('grades/', views.Grade_form_work.as_view(), name='grade'),
    path('grades_update/<str:pk>', views.Student_Update_View.as_view(), name='grades_update'),
    path('grades_delete/<str:pk>', views.Student_Delete_View.as_view(), name='grades_delete'),

    path('classes/', views.Class_form_work.as_view(), name='class'),
    path('classes_update/<str:pk>', views.Student_Update_View.as_view(), name='classes_update'),
    path('classes_delete/<str:pk>', views.Student_Delete_View.as_view(), name='classes_delete'),

    path('schedules/', views.Subject_form_work.as_view(), name='schedule'),
    path('schedules_update/<str:pk>', views.Student_Update_View.as_view(), name='schedules_update'),
    path('schedules_delete/<str:pk>', views.Student_Delete_View.as_view(), name='schedules_delete'),

    path('login/', views._LoginView.as_view(), name='login'),
    path('home_work', views.Home_Work_View.as_view(), name='home'),
    path('', views.Home_School_Page_View.as_view(), name='main'),
]