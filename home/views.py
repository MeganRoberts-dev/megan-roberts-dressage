from django.shortcuts import render, HttpResponse

def home(request):
    context = {'name': 'Megan', 'job': 'Dressage Rider'}
    return render(request, 'home/home.html', context)

def about(request):
    return render(request, 'home/about.html')

def show_map(request):
    map_embed_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d4776.852632755679!2d-3.8154586016487375!3d53.228133839020664!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x486519445e1dc32b%3A0x8125cfa40a3f67fe!2sPenrhyd%20Rd%2C%20Tal-y-cafn%2C%20Colwyn%20Bay%20LL28%205RW!5e0!3m2!1sen!2suk!4v1734372022097!5m2!1sen!2suk" 
    return render(request, 'home/home.html', {'map_embed_url': map_embed_url})
