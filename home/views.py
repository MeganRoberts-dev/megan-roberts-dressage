from django.shortcuts import render, HttpResponse

def home(request):
   # return HttpResponse ("This is my homepage (/)") #
    context = {'name': 'Megan', 'job': 'Dressage Rider'}
    return render(request, 'home/home.html', context)

def about(request):
   # return HttpResponse ("This is my about page (/about)") #
    return render(request, 'home/about.html')
