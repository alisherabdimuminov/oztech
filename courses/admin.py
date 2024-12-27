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


class AnswerTabulrInline(uadmin.TabularInline):
    model = Answer


class LessonTabularInline(uadmin.TabularInline):
    model = Lesson
    max_num = 1


class ModuleTabularInline(uadmin.TabularInline):
    model = Module
    max_num = 1


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
