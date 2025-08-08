from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page...",
            "author": "Developed by: Gabriela Martinez",
        })
        return context
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'
    
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price":200},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price":800},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price":500},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price":100}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product = Product.products[int(id) - 1]
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse('home'))
        
        viewData = {
            "title": product["name"] + " - Online Store",
            "subtitle": product["name"] + " - Product information",
            "product": product
        }

        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form,
            "success": False
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            viewData = {
                "title": "Create product",
                "form": ProductForm(),  # formulario vacío después de crear
                "success": True,
                "product_name": form.cleaned_data['name']
            }
            return render(request, self.template_name, viewData)
        else:
            viewData = {
                "title": "Create product",
                "form": form,
                "success": False
            }
            return render(request, self.template_name, viewData)