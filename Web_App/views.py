from django.shortcuts import render

# Create your views here.
# https://www.geeksforgeeks.org/django-templates/
def main_page(request):
    context = {

    }
    return render(request, 'mainPage/mainPage.html', context)
