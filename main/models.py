from django.db import models
from django.contrib.auth.models import User


class TestSet(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=60)

    def __str__(self):
        return self.title


class Question(models.Model):
    test_set = models.ForeignKey(TestSet, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_set = models.ForeignKey(TestSet, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)


class UserAnswer(models.Model):
    user_test = models.ForeignKey(UserTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def is_correct(self):
        return self.selected_answer.is_correct
