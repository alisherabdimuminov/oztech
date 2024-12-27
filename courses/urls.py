from django.urls import path

from .views import (
    get_courses_list,
    get_course,
    my_courses,
    get_module,
    get_lesson,
    get_subjects,
    get_rate,
    get_rates,
    get_ratings,
    end_lesson,
)

urlpatterns = [
    path("", get_courses_list, name="courses"),
    path("my/", my_courses, name="my_courses"),
    path("subjects/", get_subjects, name="subjects"),
    path("<int:pk>/", get_course, name="course"),
    path("<int:pk1>/modules/<int:pk2>/", get_module, name="lesson"),
    path("<int:pk1>/modules/<int:pk2>/lessons/<int:pk3>/", get_lesson, name="lesson"),

    path("rate/", get_rate, name="get_rate"),
    path("rates/", get_rates, name="get_rates"),
    path("ratings/", get_ratings, name="get_ratings"),

    path("end/", end_lesson, name="end_lesson"),
]
