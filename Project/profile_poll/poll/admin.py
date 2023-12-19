from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(CustomUser)


class User(admin.ModelAdmin):
    list_display = 'name'
    model = CustomUser


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)

