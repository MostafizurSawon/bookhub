from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from book.models import Book, Category

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['books'] = Book.objects.all()
        context['categories'] = Category.objects.all()
        return context
    

def home(request, category):
    categories = Category.objects.all()
    category = get_object_or_404(Category, name=category)
    books = Book.objects.filter(categories=category)
    
    return render(request, "home.html", {"books":books, "categories":categories})