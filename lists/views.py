from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# render search folders called templates inside any of your apps’ directories. 
# Then it builds an HttpResponse based on the content of the template.
def home_page(request):
    return render(request, "home.html")
