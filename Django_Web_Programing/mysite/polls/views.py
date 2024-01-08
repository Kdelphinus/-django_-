from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    # return HttpResponseRedirect("1")

    # return HttpResponseRedirect(reverse("detail", args=[1]))
    # return HttpResponseRedirect(reverse("detail", kwargs={"question_id": 1}))

    ctx = {
        "greetings": "Hello there!",
        "location": {"city": "Seoul", "country": "South Korea"},
        "languages": ["Korean", "English"],
    }
    # 나중에 템플릿을 합치기 편하기 위해 templates/appName 으로 폴더 구조를 만든다.
    return render(request, "polls/main.html", context=ctx)


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s." % question_id
    return HttpResponse(response)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
