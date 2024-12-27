from datetime import datetime, timedelta
from django.http import HttpRequest
from rest_framework import decorators
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response

from users.models import User

from .models import (
    Answer,
    Course,
    Lesson,
    Question,
    Quiz,
    Subject,
    Module,
    Rating,
    CourseRating,
)
from .serializers import (
    CourseRatingSerializer,
    CoursesGETSerializer,
    CourseGETSerializer,
    LessonGETSerializer,
    SubjectSerializer,
    ModuleGETSerializer,
    RatingSerializer,
)


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def get_courses_list(request: HttpRequest):
    subject_pk = request.GET.get("subject", 0)
    courses_obj = Course.objects.all()
    if subject_pk != 0:
        courses_obj = courses_obj.filter(subject_id=subject_pk)
    courses = CoursesGETSerializer(courses_obj, many=True, context={ "request": request })
    return Response({
        "status": "success",
        "code": "200",
        "data": courses.data
    })


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def get_course(request: HttpRequest, pk: int):
    course_obj = Course.objects.get(pk=pk)
    course = CourseGETSerializer(course_obj, many=False, context={ "request": request })
    return Response({
        "status": "success",
        "code": "200",
        "data": course.data
    })


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def my_courses(request: HttpRequest):
    user = request.user
    courses_obj = Course.objects.filter(students=user)
    courses = CoursesGETSerializer(courses_obj, many=True, context={ "request": request })
    print(courses_obj)
    return Response({
        "status": "success",
        "code": "200",
        "data": courses.data
    })


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def get_module(request: HttpRequest, pk1: int, pk2: int):
    module_obj = Module.objects.filter(id=pk2)
    if not module_obj:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    module_obj = module_obj.first()
    module = ModuleGETSerializer(module_obj, many=False)
    return Response({
        "status": "success",
        "code": "200",
        "data": module.data
    })


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def get_lesson(request: HttpRequest, pk1: int, pk2: int, pk3: int):
    lesson_obj = Lesson.objects.get(pk=pk3)
    lesson = LessonGETSerializer(lesson_obj, many=False)
    return Response({
        "status": "success",
        "code": "200",
        "data": lesson.data
    })


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def get_subjects(self):
    subjects_obj = Subject.objects.all()
    subjects = SubjectSerializer(subjects_obj, many=True)
    return Response({
        "status": "success",
        "code": "200",
        "data": subjects.data
    })


@decorators.api_view(http_method_names=["POST"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def get_rate(request: HttpRequest):
    course_pk = request.data.get("course")
    module_pk = request.data.get("module")
    lesson_pk = request.data.get("lesson")
    score = request.data.get("score")
    percent = request.data.get("percent")

    course = Course.objects.get(pk=course_pk)
    module = Module.objects.get(pk=module_pk)
    lesson = Lesson.objects.get(pk=lesson_pk)

    course_rating = CourseRating.objects.filter(user=request.user, course=course).first()
    course_rating.score += score
    course_rating.save()

    rating = Rating.objects.create(
        user=request.user,
        course=course,
        module=module,
        lesson=lesson,
        score=score,
        percent=percent,
    )

    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })


@decorators.api_view(http_method_names=["GET"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def get_rates(request: HttpRequest):
    ratings_obj = Rating.objects.filter(user=request.user)
    ratings = RatingSerializer(ratings_obj, many=True)

    return Response({
        "status": "success",
        "code": "200",
        "data": ratings.data,
    })


@decorators.api_view(http_method_names=["POST"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def get_ratings(request: HttpRequest):
    course_id = request.data.get("course")
    type = request.data.get("type") or "monthly"
    course = Course.objects.get(pk=course_id)
    now = datetime.now()
    now_as_str = now.strftime("%Y-%m-%d")
    ratings_obj = CourseRating.objects.filter(course=course, created=now)
    if type == "monthly":
        one_month_ago = now - timedelta(days=30)
        one_month_ago_as_str = one_month_ago.strftime("%Y-%m-%d")
        ratings_obj = CourseRating.objects.filter(course=course, created__range=[one_month_ago_as_str, now_as_str])
    elif type == "weekly":
        one_week_ago = now - timedelta(days=7)
        one_week_ago_as_str = one_week_ago.strftime("%Y-%m-%d")
        ratings_obj = CourseRating.objects.filter(course=course, created__range=[one_week_ago_as_str, now_as_str])
    else:
        ratings_obj = CourseRating.objects.filter(course=course, created__day=now.day)
    ratings = CourseRatingSerializer(ratings_obj, many=True)
    return Response({
        "status": "success",
        "errors": {},
        "data": {
            "ratings": ratings.data
        },
    })


@decorators.api_view(http_method_names=["POST"])
@decorators.permission_classes(permission_classes=[permissions.IsAuthenticated])
@decorators.authentication_classes(authentication_classes=[authentication.TokenAuthentication])
def end_lesson(request: HttpRequest):
    lesson_id = request.data.get("lesson")
    lesson = Lesson.objects.get(pk=lesson_id)
    is_last_lesson = Lesson.objects.filter(module=lesson.module).last()
    print(is_last_lesson)
    if lesson.pk == is_last_lesson.pk:
        modules = Module.objects.filter(course=lesson.module.course)
        print(modules)
        finded = False
        for i in modules:
            print(i, lesson.module)
            if i.pk == lesson.module.pk:
                finded = True
                print("set", finded)
            elif finded:
                print("topildi")
                try:
                    i.students.add(request.user)
                    i.save()
                    finded = False
                    print(i, "saved")
                    break
                except Exception as e:
                    print(e)
                    pass
    lesson.finishers.add(request.user)
    return Response({
        "status": "success",
        "errors": {},
        "data": {}
    })
