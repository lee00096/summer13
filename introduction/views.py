from django.shortcuts import render

def profile(request):
    return render(request, 'introduction/profile.html')