from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    return render(request, 'lists/home.html')


def list_view(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})


def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/universal-list/')
