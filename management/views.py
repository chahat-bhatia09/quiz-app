from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from quiz.models import Mark, Question
from os.path import join
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.sessions.models import Session



# Create your views here.

@method_decorator(staff_member_required, name="dispatch")
class Controls(View):
    def get(self, request): #render the controls html
        return render(request, template_name="management/controls.html", context={"question_limit": settings.GLOBAL_SETTINGS["questions"]})

@method_decorator(staff_member_required, name="dispatch")
class Results(View):
    def get(self, request):
        results = Mark.objects.all().order_by('-attempt_date')[:7] #render first 7 results
        return render(request, template_name="management/results.html", context={"results": results})


# @method_decorator(staff_member_required, name="dispatch")
# class VerifyQuestion(View):
#     def get(self, request):
#         qs = Question.objects.filter(verified=False)
#         return render(request, template_name="management/verify_question.html", context={"questions": qs})
# #assume the naming convention to be q1,q2 etc
#     def post(self, request):
#         count = 0
#         for q, v in request.POST.items():
#             if q.startswith("q") and v == "on":
#                 id = q[1:] #extracting "id" part
#                 q = Question.objects.filter(id=id).first()
#                 if q is not None:
#                     q.verified = True
#                     q.save()
#                     count += 1
#                 else:
#                     messages.warning(request, message=f"No question exists with the id : {id}")
#         messages.success(request, message=f"{count} questions added")
#         return redirect("controls")
@method_decorator(staff_member_required, name="dispatch")
class VerifyQuestion(View):
    def get(self, request):
        qs = Question.objects.filter(verified=False)
        return render(request, template_name="management/verify_question.html", context={"questions": qs})

    def post(self, request):
        verify_count = 0
        reject_count = 0
        for q, v in request.POST.items():
            if q.startswith("q"):
                id = q[1:]  # extracting "id" part
                question = Question.objects.filter(id=id).first()
                if question is not None:
                    if v == "verify":
                        question.verified = True
                        question.save()
                        verify_count += 1
                    elif v == "reject":
                        question.delete()
                        reject_count += 1
                else:
                    messages.warning(request, message=f"No question exists with the id: {id}")
        messages.success(request, message=f"{verify_count} question(s) verified and {reject_count} question(s) rejected.")
        return redirect("controls")



@method_decorator(staff_member_required, name="dispatch")
class Setting(View): #set question limit
    def get(self, request):
        info = {
            "question_limit": settings.GLOBAL_SETTINGS["questions"]
        }
        return render(request, template_name="management/setting.html", context={"info": info})
    def post(self, request):
        qlimit = int(request.POST.get("qlimit", 2))
        if qlimit > 0:
            settings.GLOBAL_SETTINGS["questions"] = qlimit
            messages.success(request, message="Your preference was saved")
        else:
            messages.warning(request, message="Please choose a number greater than 0")
        return redirect("controls")


@method_decorator(login_required, name="dispatch")
class AddQuestion(View):
    def get(self, request):
        return render(request,template_name="management/add_questions.html",context={"questions": range(1, settings.GLOBAL_SETTINGS["questions"] + 1)})

    def post(self, request):
        count, already_exists = 0, 0
        for i in range(1, settings.GLOBAL_SETTINGS["questions"] + 1):
            data = request.POST
            q = data.get(f"q{i}", "")
            o1 = data.get(f"q{i}o1", "")
            o2 = data.get(f"q{i}o2", "")
            o3 = data.get(f"q{i}o3", "")
            o4 = data.get(f"q{i}o4", "")
            co = data.get(f"q{i}c", "")
            if Question.objects.filter(question=q).first():
                already_exists += 1
                continue
            question = Question(question=q, option1=o1, option2=o2, option3=o3, option4=o4, correct_option=co, creator=request.user)
            question.save()
            count += 1
        if already_exists:
            messages.warning(request, message=f"{already_exists} question already exists")
        messages.success(request, message=f"{count} question/s successfully added. Wait for verification.")
        return redirect("add_question")



class Scoresheet(View):
    def get(self, request):
        results = Mark.objects.all().order_by("-got")[:7] #Only render the first 7 results
        return render(request, template_name="management/scoresheet.html", context={"results": results})
