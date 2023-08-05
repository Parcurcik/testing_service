from django import forms
from .models import Answer


class QuestionForm(forms.Form):
    selected_answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None
    )

    def __init__(self, *args, question=None, **kwargs):
        super().__init__(*args, **kwargs)
        if question:
            self.fields['selected_answer'].queryset = question.answer_set.all()
