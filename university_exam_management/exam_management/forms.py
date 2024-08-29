# exam_management/forms.py

from django import forms
from .models import AnswerSheet

class EvaluationForm(forms.Form):
    marks = forms.JSONField(widget=forms.Textarea, help_text="Enter marks for each question in JSON format.")

class AnswerSheetUploadForm(forms.ModelForm):
    class Meta:
        model = AnswerSheet
        fields = ['student', 'file']


class RevaluationRequestForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, label="Reason for Re-evaluation", required=True)