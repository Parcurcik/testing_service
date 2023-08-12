from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import TestSet, UserTest
from .forms import QuestionForm


def index(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        if email:
            try:
                existing_user = User.objects.get(username=email)
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    return render(request, 'index.html', {'user': request.user})
                else:
                    error_message = "Неверный пароль"
                    messages.error(request, error_message)
            except User.DoesNotExist:
                new_user = User.objects.create_user(username=email, email=email, password=password)
                login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
                new_user.save()
        else:
            error_message = "Введите почту"
            messages.error(request, error_message)

    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def tests(request):
    test_sets = TestSet.objects.all()
    return render(request, 'test_pages.html', {'test_sets': test_sets})


@login_required
def test(request, test_id):
    test_set = get_object_or_404(TestSet, id=test_id)
    questions = list(test_set.question_set.all())
    user_test, created = UserTest.objects.get_or_create(user=request.user, test_set=test_set)
    user_answers = user_test.useranswer_set.all()
    correct_answers = sum(user_answer.selected_answer.is_correct for user_answer in user_answers)
    current_question_index = user_answers.count()
    find_percent = int(int(correct_answers) / len(questions) * 100)
    num_questions = len(questions)
    if current_question_index < num_questions:
        current_question = questions[current_question_index]
        if request.method == 'POST':
            form = QuestionForm(request.POST, question=current_question)
            if form.is_valid():
                user_answer = form.cleaned_data['selected_answer']
                user_test.useranswer_set.update_or_create(question=current_question,
                                                          defaults={'selected_answer': user_answer})
                return redirect('test', test_id=test_id)
        else:
            form = QuestionForm(question=current_question)
    else:
        return render(request, 'test_view.html', {'test_set': test_set, 'user_test': user_test, 'questions': questions,
                                                  'show_result': True, 'current_question': None,
                                                  'correct_answers': correct_answers, 'find_percent': find_percent})
    return render(request, 'test_view.html',
                  {'test_set': test_set, 'form': form, 'current_question_index': current_question_index,
                   'current_question': current_question, 'correct_answers': correct_answers})


@login_required
def delete_user_answers(request, test_id):
    test_set = get_object_or_404(TestSet, id=test_id)
    user_test = get_object_or_404(UserTest, user=request.user, test_set=test_set)
    user_test.useranswer_set.all().delete()
    return redirect('test', test_id=test_id)
