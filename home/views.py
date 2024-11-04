from django.shortcuts import render, HttpResponse

def home(request):
   # return HttpResponse ("This is my homepage (/)") #
   return render(request, 'home.html')

def about(request):
   # return HttpResponse ("This is my about page (/about)") #
    return render(request, 'about.html')

def services(request):
   # return HttpResponse ("This is my services page (/services)") #
    return render(request, 'services.html')
    
def contact(request):
  #  return HttpResponse ("This is my contact page (/contact)")  #
    return render(request, 'contact.html')