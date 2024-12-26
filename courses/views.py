from django.http import HttpRequest
from rest_framework import decorators
from rest_framework.response import Response

from .models import (
    Answer,
    Course,
    Lesson,
    Question,
    Quiz,
    Subject,
)
from .serializers import (
    CoursesGETSerializer,
    CourseGETSerializer,
    LessonGETSerializer,
    SubjectSerializer,
)


@decorators.api_view(http_method_names=["GET"])
def get_courses_list(request: HttpRequest):
    courses_obj = Course.objects.all()
    courses = CoursesGETSerializer(courses_obj, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": courses.data
    })

@decorators.api_view(http_method_names=["GET"])
def get_course(request: HttpRequest, pk: int):
    course_obj = Course.objects.get(pk=pk)
    course = CourseGETSerializer(course_obj, many=False)
    return Response({
        "status": "success",
        "code": "200",
        "data": course.data
    })


@decorators.api_view(http_method_names=["GET"])
def get_lesson(request: HttpRequest, pk1: int, pk2: int):
    lesson_obj = Lesson.objects.get(pk=pk2)
    lesson = LessonGETSerializer(lesson_obj, many=False)
    return Response({
        "status": "success",
        "code": "200",
        "data": lesson.data
    })


@decorators.api_view(http_method_names=["GET"])
def get_subjects(self):
    subjects_obj = Subject.objects.all()
    subjects = SubjectSerializer(subjects_obj, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": subjects.data
    })

