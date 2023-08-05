from django.contrib import admin
from .models import TestSet, Question, Answer, UserTest, UserAnswer

admin.site.register(TestSet)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserTest)
admin.site.register(UserAnswer)
