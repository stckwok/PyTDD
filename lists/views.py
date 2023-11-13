from django.shortcuts import render, redirect
from lists.models import Item

# Create your views here.
# render search folders called templates inside any of your apps’ directories. 
# Then it builds an HttpResponse based on the content of the template.

def home_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/")

    items = Item.objects.all()
    return render(request, "home.html", {"items": items})