from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, timedelta

from users.models import User


LESSON_TYPE = (
    ("lesson", "Dars"),
    ("quiz", "Test"),
)

QUESTION_TYPE = (
    ("one_select", "Bitta javob tanlash"),
    ("many_select", "Ko'p javob tanlash"),
    ("writable", "Yoziladigan"),
    ("matchable", "Mos keladigan"),
)

PERMISSION_TYPE = (
    ("monthly", "6 oylik"),
    ("yearly", "1 yillik"),
)


class Question(models.Model):
    question = models.TextField(verbose_name="Savol matni")
    type = models.CharField(max_length=100, choices=QUESTION_TYPE, verbose_name="Savol turi")
    created = models.DateTimeField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Savol")
    value_1 = models.TextField(null=True, blank=True, verbose_name="Qiymat 1")
    value_2 = models.TextField(null=True, blank=True, verbose_name="Qiymat 2")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.value_1
    
    class Meta:
        verbose_name = "Javob"
        verbose_name_plural = "Javoblar"


class Quiz(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    questions = models.ManyToManyField(Question, related_name="quiz_questions", verbose_name="Savollar")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"
    

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    image = models.ImageField(upload_to="images/subjects", verbose_name="Rasmi")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def courses(self):
        return Course.objects.filter(subject=self).count()
    
    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
    

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="O'qituvchi")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
    description = models.TextField(verbose_name="Kurs haqida qisqacha")
    image = models.ImageField(upload_to="images/courses", verbose_name="Rasmi")
    price = models.IntegerField(verbose_name="Narxi")
    students = models.ManyToManyField(User, related_name="course_students", null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def modules(self):
        return Module.objects.filter(course=self)
    
    def count_students(self):
        return self.students.count()
    
    def count_modules(self):
        return Module.objects.filter(course=self).count()
    
    def count_lessons(self):
        return Lesson.objects.filter(module__course=self).count()
    
    def count_quizzes(self) -> int:
        return Lesson.objects.filter(module__course=self, type="quiz").count()

    def length(self):
        return Lesson.objects.filter(module__course=self).aggregate(models.Sum("duration")).get("duration__sum") or 0

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"


class Module(models.Model):
    name = models.CharField(max_length=500, verbose_name='Nomi')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    required = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Talab qilinadi")
    students = models.ManyToManyField(User, related_name="module_students", null=True, blank=True, verbose_name="Talabalar")
    finishers = models.ManyToManyField(User, related_name="module_finishers", null=True, blank=True, verbose_name="Bitirganlar")

    def __str__(self) -> str:
        return self.name
    
    def finished_lessons(self, user: User):
        lessons = Lesson.objects.filter(module=self)
        count = 0
        for lesson in lessons:
            if user in lesson.finishers.all():
                count += 1
        return count
    
    def count_students(self) -> int:
        return self.students.count()
    
    def count_finishers(self) -> int:
        return self.finishers.count()
    
    def count_lessons(self) -> int:
        return Lesson.objects.filter(module=self).count()
    
    def count_quizzes(self) -> int:
        return Lesson.objects.filter(module=self, type="quiz").count()
    
    def lessons(self):
        return Lesson.objects.filter(module=self)
    
    def count_quizzes(self):
        return Lesson.objects.filter(type="quiz").count()
    
    def video_length(self) -> int:
        return Lesson.objects.filter(module=self).aggregate(duration=models.Sum("duration")).get("duration") or 0

    class Meta:
        verbose_name = "Modul"
        verbose_name_plural = "Modullar"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name="Modul")
    type = models.CharField(max_length=100, choices=LESSON_TYPE, verbose_name="Turi")
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Test")
    duration = models.IntegerField(default=60, verbose_name="Davomiyligi")
    video = models.URLField(null=True, blank=True, verbose_name="Video link (YouTubue)")
    resource = models.FileField(upload_to="files/lessons", null=True, blank=True, verbose_name="Manbaa")
    previous = models.ForeignKey("self", related_name="previous_lesson", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Oldingi dars")
    next = models.ForeignKey("self", related_name="next_lesson", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Keyingi dars")
    finishers = models.ManyToManyField(User, related_name="lesson_finishers", null=True, blank=True, verbose_name="Tugatganlar")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def is_quiz(self):
        return True if self.quiz else False
    
    def has_previous(self):
        return True if self.previous else False
    
    def has_next(self):
        return True if self.next else False
    
    def count_finishers(self):
        return self.finishers.count()
    
    def finishers_list(self):
        return self.finishers.all()
    
    def end_lesson(self, user: User):
        self.finishers.add(user)

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    score = models.IntegerField()
    percent = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.score)


class CourseRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.score)
    

class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.CharField(max_length=1000, choices=PERMISSION_TYPE)
    created = models.DateField(auto_now_add=True)
    ended = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.type
    
    def save(self, *args, **kwargs):
        if self.type == "monthly":
            self.ended = date.today() + timedelta(days=182)
        else:
            self.ended = date.today() + timedelta(days=365)
        super(Permission, self).save(*args, **kwargs)


@receiver(post_save, sender=Lesson)
def notify_model_saved(sender, instance: Lesson, created, **kwargs):
    if instance.previous:
        instance.previous.next = instance
        instance.previous.save()
