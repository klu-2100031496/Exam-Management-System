from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from .models import AnswerSheet, Evaluation, RevaluationRequest
from .forms import EvaluationForm, AnswerSheetUploadForm, RevaluationRequestForm
from django.contrib import messages

@login_required
def student_home(request):
    # Fetch answer sheets for the logged-in student
    answer_sheets = AnswerSheet.objects.filter(student=request.user)
    return render(request, 'exam_management/student_home.html', {'answer_sheets': answer_sheets})

@login_required
def teacher_home(request):
    return render(request, 'exam_management/teacher_home.html')


@login_required
def home(request):
    if request.user.groups.filter(name='Teachers').exists():
        return redirect('teacher_home')
    elif request.user.groups.filter(name='Students').exists():
        return redirect('student_home')
    else:
        return redirect('login')

class CustomLoginView(LoginView):
    template_name = 'exam_management/login.html'

    def get_success_url(self):
        if self.request.user.groups.filter(name='Teachers').exists():
            return '/teacher/home/'
        elif self.request.user.groups.filter(name='Students').exists():
            return '/student/home/'
        else:
            return '/'

@login_required
def evaluate_answer_sheet(request, answer_sheet_id):
    answer_sheet = get_object_or_404(AnswerSheet, id=answer_sheet_id)
    teacher_id = request.user.id 
    evaluation, created = Evaluation.objects.get_or_create(answer_sheet=answer_sheet ,  teacher_id=teacher_id)

    if evaluation.is_final and not RevaluationRequest.objects.filter(answer_sheet=answer_sheet).exists():
        messages.warning(request, "This answer sheet has already been evaluated and cannot be re-evaluated unless a revaluation request is made.")
        return redirect('teacher_home')

    if request.method == 'POST':
        # Process the evaluation form
        marks = {}
        for i in range(1, 11):
            mark = request.POST.get(f'marks_{i}', 0)
            marks[i] = float(mark)
        
        print("Logged-in user:", request.user)
        evaluation.teacher = request.user
        evaluation.marks = marks
        evaluation.is_final = True
        evaluation.save()

        messages.success(request, "Evaluation submitted successfully.")
        return redirect('teacher_home')

    context = {
        'answer_sheet': answer_sheet,
        'marks': evaluation.marks if evaluation else {},
        'can_evaluate': not evaluation.is_final or RevaluationRequest.objects.filter(answer_sheet=answer_sheet).exists(),
    }
    return render(request, 'evaluate_answer_sheet.html', context)




def revaluate_answer_sheet(request, answer_sheet_id):
    answer_sheet = get_object_or_404(AnswerSheet, id=answer_sheet_id)

    # Check if revaluation is allowed
    can_evaluate = answer_sheet.is_evaluated and request.user.has_perm('can_revaluate')

    # Handle form submission
    if request.method == "POST" and can_evaluate:
        for i in range(1, 11):
            marks = request.POST.get(f'marks_{i}', 0)
            # Save the updated marks to your model
            answer_sheet.marks[i-1] = marks  # Assuming a list or similar structure
        answer_sheet.is_evaluated = True  # Re-mark as evaluated
        answer_sheet.save()
        return redirect('revaluation_success')  # Redirect after successful revaluation

    # Get the current marks (if any)
    marks = {i: answer_sheet.marks.get(i-1, 0) for i in range(1, 11)}

    return render(request, 'exam_management/evaluate_answer_sheet.html', {
        'answer_sheet': answer_sheet,
        'can_evaluate': can_evaluate,
        'marks': marks,
    })







@login_required
def view_marks(request, sheet_id):
    answer_sheet = get_object_or_404(AnswerSheet, id=sheet_id, student=request.user)
    evaluation = Evaluation.objects.filter(answer_sheet=answer_sheet).first()
    revaluation_requested = RevaluationRequest.objects.filter(answer_sheet=answer_sheet, student=request.user).exists()
    return render(request, 'exam_management/view_marks.html', {
        'answer_sheet': answer_sheet,
        'evaluation': evaluation,
        'can_request_revaluation': not revaluation_requested and answer_sheet.is_evaluated
    })

@login_required
def revaluation_request(request, sheet_id):
    answer_sheet = get_object_or_404(AnswerSheet, id=sheet_id, student=request.user)
    
    # Prevent revaluation request if it already exists or the paper is not evaluated
    if answer_sheet.revaluation_requested:
        return redirect('student_home')

    if request.method == 'POST':
        reason = request.POST.get('reason')
        RevaluationRequest.objects.create(student=request.user, answer_sheet=answer_sheet, reason=reason)
        answer_sheet.revaluation_requested = True
        answer_sheet.save()
        return redirect('student_home')

    return render(request, 'exam_management/revaluation_request.html', {'answer_sheet': answer_sheet})



# @login_required
# def revaluation_request(request, sheet_id):
#     answer_sheet = get_object_or_404(AnswerSheet, id=sheet_id, student=request.user)

#     # Check if revaluation is already requested or paper not evaluated
#     if answer_sheet.revaluation_requested:
#         return redirect('student_home')  # Redirect if already requested
#     elif not answer_sheet.is_evaluated:
#         return redirect('student_home')  # Redirect if not evaluated

#     if request.method == 'POST':
#         reason = request.POST.get('reason')

#         # If form is valid, create request and save changes
#         if form.is_valid():  # Assuming you have a form (see point 2 above)
#             RevaluationRequest.objects.create(student=request.user, answer_sheet=answer_sheet, reason=reason)
#             answer_sheet.revaluation_requested = True
#             answer_sheet.save()
#             return redirect('student_home')  # Redirect after successful request

#     form = RevaluationRequestForm(request.POST or None)  # Assuming you have a RevaluationRequestForm
#     return render(request, 'exam_management/revaluation_request.html', {'answer_sheet': answer_sheet, 'form': form})







def logout_view(request):
    logout(request)
    return redirect('login')

@user_passes_test(lambda u: u.is_superuser)
def upload_answer_sheet(request):
    if request.method == 'POST':
        form = AnswerSheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            answer_sheet = form.save(commit=False)
            answer_sheet.student = request.user  # Assuming the student is the logged-in user
            answer_sheet.save()
            return redirect('admin_home')  # Redirect to a success page or another page
    else:
        form = AnswerSheetUploadForm()
    return render(request, 'exam_management/upload_answer_sheet.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_home(request):
    return render(request, 'exam_management/admin_home.html')

@login_required
def list_answer_sheets_for_teacher(request):
    if not request.user.is_superuser and not request.user.groups.filter(name='Teachers').exists():
        return redirect('login')
    
    answer_sheets = AnswerSheet.objects.all()  # or filter as needed
    return render(request, 'exam_management/list_answer_sheets_for_teacher.html', {'answer_sheets': answer_sheets})

@login_required
def list_answer_sheets_for_student(request):
    if not request.user.groups.filter(name='Students').exists():
        return redirect('login')

    # Retrieve answer sheets for the logged-in student
    answer_sheets = AnswerSheet.objects.filter(student=request.user).select_related('evaluation')

    # Pass the answer sheets to the template
    context = {
        'answer_sheets': answer_sheets,
    }
    return render(request, 'exam_management/list_answer_sheets_for_student.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Teachers').exists())
def view_revaluation_requests(request):
    if not request.user.is_superuser and not request.user.groups.filter(name='Teachers').exists():
        return redirect('login')

    revaluation_requests = RevaluationRequest.objects.all()
    return render(request, 'exam_management/view_revaluation_requests.html', {'revaluation_requests': revaluation_requests})
