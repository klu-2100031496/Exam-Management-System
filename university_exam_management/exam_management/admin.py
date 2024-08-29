from django.contrib import admin
from .models import AnswerSheet, Evaluation, RevaluationRequest, TeacherProfile, StudentProfile

@admin.register(AnswerSheet)
class AnswerSheetAdmin(admin.ModelAdmin):
    list_display = ('student', 'file', 'is_evaluated', 'created_at')
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        """Custom action to delete selected answer sheets."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Deleted {count} answer sheets.")

    delete_selected.short_description = "Delete selected answer sheets"

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('answer_sheet', 'teacher', 'is_final')
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        """Custom action to delete selected evaluations."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Deleted {count} evaluations.")

    delete_selected.short_description = "Delete selected evaluations"

@admin.register(RevaluationRequest)
class RevaluationRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'answer_sheet', 'reason', 'is_processed')
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        """Custom action to delete selected revaluation requests."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Deleted {count} revaluation requests.")

    delete_selected.short_description = "Delete selected revaluation requests"

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'teacher_id')
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        """Custom action to delete selected teacher profiles."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Deleted {count} teacher profiles.")

    delete_selected.short_description = "Delete selected teacher profiles"

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id')
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        """Custom action to delete selected student profiles."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Deleted {count} student profiles.")

    delete_selected.short_description = "Delete selected student profiles"
