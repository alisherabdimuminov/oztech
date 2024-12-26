from rest_framework import serializers

from users.models import User
from .models import (
    Answer,
    Course,
    Lesson,
    Question,
    Quiz,
    Subject,
)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("name", )


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", )

class AnswerGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("value_1", "value_2", "is_correct", )


class QuestionGETSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField("answers_func")

    def answers_func(self, obj):
        answers_obj = Answer.objects.filter(question=obj)
        answers = AnswerGETSerializer(answers_obj, many=True)
        return answers.data

    class Meta:
        model = Question
        fields = ("question", "type", "answers", )


class QuizGETSerializer(serializers.ModelSerializer):
    questions = QuestionGETSerializer(Question, many=True)

    class Meta:
        model = Quiz
        fields = ("id", "name", "questions", )


class CoursesGETSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(User, many=False)
    subject = SubjectSerializer(Subject, many=False)
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = Course
        fields = ("id", "name", "user", "subject", "description", "image", "price", "count_students", "created", )


class LessonGETLittleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "name", "type", )


class CourseGETSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(User, many=False)
    subject = SubjectSerializer(Subject, many=False)
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    lessons = serializers.SerializerMethodField("lessons_func")

    def lessons_func(self, obj):
        lessons_obj = Lesson.objects.filter(course=obj)
        lessons = LessonGETLittleSerializer(lessons_obj, many=True)
        return lessons.data

    class Meta:
        model = Course
        fields = ("id", "name", "user", "subject", "description", "image", "price", "count_students", "lessons", "created", )


class LessonGETSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    quiz = QuizGETSerializer(Quiz, many=False)
    class Meta:
        model = Lesson
        fields = ("id", "name", "course", "type", "quiz", "duration", "video", "source", "previous", "next", "created", )
