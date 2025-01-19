from unfold import admin as uadmin
from django.contrib import admin

from .models import (
    Answer,
    Course,
    Lesson,
    Module,
    Question,
    Quiz,
    Subject,
)


class AnswerTabulrInline(uadmin.StackedInline):
    model = Answer
    extra = 0


class LessonTabularInline(uadmin.StackedInline):
    model = Lesson
    extra = 0


class ModuleTabularInline(uadmin.StackedInline):
    model = Module
    extra = 0


@admin.register(Course)
class CourseModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", "price", "count_students", "created", ]
    inlines = [ModuleTabularInline]


@admin.register(Module)
class ModuleModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", "course", "required", ]
    inlines = [LessonTabularInline]


@admin.register(Question)
class QuestionModelAdmin(uadmin.ModelAdmin):
    list_display = ["question", "type", ]
    inlines = [AnswerTabulrInline]


@admin.register(Subject)
class SubjectModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", ]

@admin.register(Quiz)
class QuizModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", ]


@admin.register(Lesson)
class LessonModelAdmin(uadmin.ModelAdmin):
    list_display = ["name", "type", ]
