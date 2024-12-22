from django.shortcuts import render, HttpResponse

def home(request):
    context = {'name': 'Megan', 'job': 'Dressage Rider'}
    return render(request, 'home/home.html', context)

def about(request):
    return render(request, 'home/about.html')

