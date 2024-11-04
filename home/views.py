from django.shortcuts import render, HttpResponse

def home(request):
   # return HttpResponse ("This is my homepage (/)") #
    context = {'name': 'Megan', 'job': 'Dressage Rider'}
    return render(request, 'home/home.html', context)

def about(request):
   # return HttpResponse ("This is my about page (/about)") #
    return render(request, 'home/about.html')

def services(request):
   # return HttpResponse ("This is my services page (/services)") #
    return render(request, 'home/services.html')

def contact(request):
  #  return HttpResponse ("This is my contact page (/contact)")  #
    return render(request, 'home/contact.html')