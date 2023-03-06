from django.shortcuts import render

# Create your views here.
# https://www.geeksforgeeks.org/django-templates/
def landing_page(request):
    context = {
        "data": "Gfg is the best",
        "list": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    return render(request, 'mainPage/mainPage.html', context)