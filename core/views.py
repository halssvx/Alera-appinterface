from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import BloodGlucose, PatternAlert

@login_required
def dashboard(request):
    alerts = PatternAlert.objects.filter(user=request.user).order_by("-created_at")[:5]
    return render(request, "dashboard.html", {"alerts": alerts})

@login_required
def log_glucose(request):
    if request.method == "POST":
        BloodGlucose.objects.create(
            user=request.user,
            value_mgdl=request.POST.get("value"),
            meal_tag=request.POST.get("meal_tag"),
            note=request.POST.get("note")
        )
        return redirect("/")
    return render(request, "log.html")

@login_required
def glucose_series(request):
    qs = BloodGlucose.objects.filter(user=request.user).order_by("timestamp")
    data = [{"x": g.timestamp.isoformat(), "y": float(g.value_mgdl)} for g in qs]
    return JsonResponse({"data": data})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})
