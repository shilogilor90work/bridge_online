from django.shortcuts import redirect
from django.shortcuts import render

def home(request):
    return redirect('/home')


def home_page(request):
    return render(request, 'manage_hands/home.html')