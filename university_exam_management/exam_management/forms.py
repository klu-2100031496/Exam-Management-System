from django import forms
from .models import AnswerSheet

class EvaluationForm(forms.Form):
    # Create a form with individual fields for marks per question
    marks_1 = forms.FloatField(min_value=0, required=True, label="Marks for Question 1")
    marks_2 = forms.FloatField(min_value=0, required=True, label="Marks for Question 2")
    marks_3 = forms.FloatField(min_value=0, required=True, label="Marks for Question 3")
    marks_4 = forms.FloatField(min_value=0, required=True, label="Marks for Question 4")
    marks_5 = forms.FloatField(min_value=0, required=True, label="Marks for Question 5")
    marks_6 = forms.FloatField(min_value=0, required=True, label="Marks for Question 6")
    marks_7 = forms.FloatField(min_value=0, required=True, label="Marks for Question 7")
    marks_8 = forms.FloatField(min_value=0, required=True, label="Marks for Question 8")
    marks_9 = forms.FloatField(min_value=0, required=True, label="Marks for Question 9")
    marks_10 = forms.FloatField(min_value=0, required=True, label="Marks for Question 10")

    def clean(self):
        cleaned_data = super().clean()
        marks = {f'marks_{i}': cleaned_data.get(f'marks_{i}', 0) for i in range(1, 11)}
        return marks

class AnswerSheetUploadForm(forms.ModelForm):
    class Meta:
        model = AnswerSheet
        fields = ['student', 'file']

class RevaluationRequestForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, label="Reason for Re-evaluation", required=True)
