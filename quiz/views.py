from django.shortcuts import render, redirect
from django.views import View
from .models import Question, Mark
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.core.paginator import Paginator

@method_decorator(login_required, name="dispatch")
class Quiz(View):
    def get(self, request):
        questions = Question.objects.filter(verified=True)
        return render(request, template_name="quiz/quiz.html",context={"questions": questions})

    def post(self, request):
        mark = Mark(user=request.user, total=Question.objects.filter(verified=True).count())
        for i in range(1, Question.objects.filter(verified=True).count()+1):
            q = Question.objects.filter(pk=request.POST.get(f"q{i}", 0), verified=True).first()
            if request.POST.get(f"q{i}o", "") == q.correct_option:
                mark.got += 1
        mark.save()
        messages.success(request, message="New attempt recorded")
        return redirect("attempts")



@method_decorator(login_required, name="dispatch")
class Attempts(View):
    def get(self, request):
        results = Mark.objects.filter(user=request.user)
        return render(request, template_name="quiz/attempts.html", context={"results": results})


