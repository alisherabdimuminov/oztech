from django.urls import path

from .views import (
    get_courses_list,
    get_course,
    get_lesson,
    get_subjects,
)

urlpatterns = [
    path("", get_courses_list, name="courses"),
    path("subjects/", get_subjects, name="subjects"),
    path("course/<int:pk>/", get_course, name="course"),
    path("course/<int:pk1>/lessons/lesson/<int:pk2>/", get_lesson, name="lesson"),
]
