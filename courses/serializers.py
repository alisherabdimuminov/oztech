from rest_framework import serializers

from users.models import User
from users.serializers import UserSerializer
from .models import (
    Answer,
    Course,
    CourseRating,
    Lesson,
    Module,
    Question,
    Quiz,
    Rating,
    Subject,
)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "name", )


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


class LessonGETLittleSerializer(serializers.ModelSerializer):
    requires_context = True

    is_open = serializers.SerializerMethodField("check_open")

    def check_open(self, obj):
        request = self.context.get("request")
        print(request)
        if request:
            if (obj.has_previous()):
                if request.user in obj.previous.finishers.all():
                    return True
                else:
                    return False
            else:
                return True
        return True

    class Meta:
        model = Lesson
        fields = ("id", "name", "type", "duration", "is_open", )


class ModuleRequiredSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField("is_open_func")
    lessons = serializers.SerializerMethodField("get_lessons")

    def get_lessons(self, obj):
        return LessonGETLittleSerializer(obj.lessons(), many=True, context=self.context).data
    

    def is_open_func(self, obj):
        request = self.context.get("request")
        print(request)
        if request:
            if request.user in obj.students.all():
                return True
            return False
        return False
    class Meta:
        model = Module
        fields = ("id", "name", "is_open", "lessons", )


class LessonGETSerializer(serializers.ModelSerializer):
    requires_context = True

    is_open = serializers.SerializerMethodField("check_open")
    quiz = QuizGETSerializer(Quiz.objects.all(), many=False)
    previous = LessonGETLittleSerializer(Lesson.objects.all(), many=False)
    next = LessonGETLittleSerializer(Lesson.objects.all(), many=False)
    
    def check_open(self, obj):
        request = self.context.get("request")
        if request:
            if (obj.has_previous()):
                if request.user in obj.previous.finishers.all():
                    return True
                else:
                    return False
            else:
                return True
        return True
    
    class Meta:
        model = Lesson
        fields = ("id", "name", "type", "video", "duration", "resource", "quiz", "previous", "next", "is_open", "created",)


class ModuleGETSerializer(serializers.ModelSerializer):
    requires_context = True

    is_open = serializers.SerializerMethodField("is_open_func")
    required = ModuleRequiredSerializer(Module.objects.all(), many=False)
    lessons = LessonGETLittleSerializer(Lesson.objects.all(), many=True)

    def is_open_func(self, obj):
        request = self.context.get("request")
        if request:
            if request.user in obj.students.all():
                return True
            return False
        return False
    

    class Meta:
        model = Module
        fields = ("id", "name", "required", "video_length", "count_students", "count_finishers", "count_lessons", "students", "lessons", "is_open")


class CoursesGETSerializer(serializers.ModelSerializer):
    requires_context = True

    is_open = serializers.SerializerMethodField("is_open_func")
    percentage = serializers.SerializerMethodField("percentage_func")
    user = AuthorSerializer(User, many=False)
    subject = SubjectSerializer(Subject, many=False)
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    def is_open_func(self, obj):
        request = self.context.get("request")
        if request:
            if request.user in obj.students.all():
                return True
            return False
        return False

    def percentage_func(self, obj):
        request = self.context.get("request")
        user = request.user
        count = 0
        for module in obj.modules():
            count += module.finished_lessons(user=user)
        if obj.count_lessons() == 0:
            return 0
        return count * 100 / obj.count_lessons()

    class Meta:
        model = Course
        fields = ("id", "name", "user", "subject", "description", "image", "price", "percentage", "length", "count_modules", "count_lessons", "count_students", "is_open", "created", )


class CourseGETSerializer(serializers.ModelSerializer):
    requires_context = True

    is_open = serializers.SerializerMethodField("is_open_func")
    user = AuthorSerializer(User, many=False)
    subject = SubjectSerializer(Subject, many=False)
    percentage = serializers.SerializerMethodField("percentage_func")
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    modules = serializers.SerializerMethodField("modules_func")

    def is_open_func(self, obj):
        request = self.context.get("request")
        if request:
            if request.user in obj.students.all():
                return True
            return False
        return False

    def modules_func(self, obj):
        modules_obj = Module.objects.filter(course=obj)
        modules = ModuleRequiredSerializer(modules_obj, many=True, context=self.context)
        return modules.data
    
    def percentage_func(self, obj):
        request = self.context.get("request")
        user = request.user
        count = 0
        for module in obj.modules():
            count += module.finished_lessons(user=user)
        if obj.count_lessons() == 0:
            return 0
        return count * 100 / obj.count_lessons()


    class Meta:
        model = Course
        fields = ("id", "name", "user", "subject", "description", "image", "price", "percentage", "length", "count_modules", "count_lessons", "count_students",  "modules", "is_open", "created", )


class RatingSerializer(serializers.ModelSerializer):
    course = CourseGETSerializer(Course, many=False)
    class Meta:
        model = Rating
        fields = ("course", "module", "lesson", "score",)


class CourseRatingSerializer(serializers.ModelSerializer):
    course = CourseGETSerializer(Course, many=False)
    author = UserSerializer(User, many=False)
    class Meta:
        model = CourseRating
        fields = ("author", "course", "score", )