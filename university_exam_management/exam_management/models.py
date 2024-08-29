from django.db import models
from django.contrib.auth.models import User

# Model for storing answer sheets
class AnswerSheet(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_sheets')
    file = models.FileField(upload_to='answer_sheets/')
    is_evaluated = models.BooleanField(default=False)  # Indicates if the paper has been evaluated
    revaluation_requested = models.BooleanField(default=False)  # Indicates if a revaluation request has been made
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer Sheet of {self.student.username}"


# Model for storing evaluations
class Evaluation(models.Model):
    answer_sheet = models.OneToOneField(AnswerSheet, on_delete=models.CASCADE, related_name='evaluation')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations', null=True)
    marks = models.JSONField(default=dict)  # Store marks for each question as a JSON object, default to empty dict
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  # Record creation timestamp
    modified_at = models.DateTimeField(auto_now=True) 
    is_final = models.BooleanField(default=False)  # To mark if the evaluation is final or not

    def __str__(self):
        return f"Evaluation of {self.answer_sheet.student.username} by {self.teacher.username}"

    def get_marks(self):
        return self.marks or {}  # Return empty dict if marks is None

# Model for handling revaluation requests
class RevaluationRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revaluation_requests')
    answer_sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE, related_name='revaluation_requests')
    reason = models.TextField()  # Reason for re-evaluation
    is_processed = models.BooleanField(default=False)  # Indicates if the request has been processed

    class Meta:
        unique_together = ('student', 'answer_sheet')  # Ensure only one request per student and answer sheet

    def __str__(self):
        return f"Revaluation Request by {self.student.username} for {self.answer_sheet}"


# Extend User model with additional fields for teachers
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(max_length=20, unique=True)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Teacher Profile of {self.user.username}"

# Extend User model with additional fields for students
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Student Profile of {self.user.username}"
