from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Home page redirection based on user group
    path('student/home/', views.student_home, name='student_home'),  # Student home page
    path('teacher/home/', views.teacher_home, name='teacher_home'),  # Teacher home page
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout view

    # Evaluation and viewing marks paths
    path('evaluate/<int:answer_sheet_id>/', views.evaluate_answer_sheet, name='evaluate_answer_sheet'),
    path('view_marks/<int:sheet_id>/', views.view_marks, name='view_marks'),

    # Revaluation request path
    path('revaluation/<int:sheet_id>/', views.revaluation_request, name='revaluation_request'),

    # Admin and upload paths
    path('upload/', views.upload_answer_sheet, name='upload_answer_sheet'),
    path('adhome/', views.admin_home, name='admin_home'),

    # Teacher and student answer sheets paths
    path('teacher/answer_sheets/', views.list_answer_sheets_for_teacher, name='list_answer_sheets_for_teacher'),
    path('student/answer_sheets/', views.list_answer_sheets_for_student, name='list_answer_sheets_for_student'),

    path('revaluate/<int:answer_sheet_id>/', views.revaluate_answer_sheet, name='revaluate_answer_sheet'),


    # Revaluation requests for teachers
    path('teacher/revaluation_requests/', views.view_revaluation_requests, name='view_revaluation_requests'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
