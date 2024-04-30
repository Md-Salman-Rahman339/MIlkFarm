from django.shortcuts import render
from django.views.generic import CreateView, DetailView,ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404,redirect
from django.urls import reverse_lazy
from . import models
from .forms import ProductForm,ReviewForm
from . import forms
from author.models import UserAccount
from .models import BuyProduct,Category,Product,Review
from django. contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_list_or_404 
from django.views import View

from django.template.loader import render_to_string



def product_view(request,category_slug=None):
    categories=Category.objects.all()

    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        data=Product.objects.filter(category=category)

    else:
        data=Product.objects.all()

    return render(request,'product_list.html',{'data':data,'categories':categories})


@method_decorator(login_required, name='dispatch')
class DetailsPost(DetailView):
    model = models.Product
    pk_url_kwarg = 'pk'
    template_name = 'product_details.html'

        
    def post(self, request, *args, **kwargs):
        comment_form = forms.ReviewForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object 
        comments = post.comments.all()
        comment_form = forms.ReviewForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context
    

@login_required
def buy_product(request,product_id):
    product=get_object_or_404(Product,pk=product_id)
    if request.method=='GET':
        return render(request,'buy_book.html',{'book':product})

    elif request.method=='POST':
        if request.user.account.balance>=product.buying_price:
            request.user.account.balance-=product.buying_price
            request.user.account.save()
            BuyProduct.objects.create(user=request.user,product=product)
            messages.success(request, f"You have successfully bought {product.title}.")
        else:
            messages.error(request, "Insufficient funds to buy the book.")
        return redirect('product_list')




class MyProductListView(ListView):
    template_name = 'myproduct_list.html'
    context_object_name = 'data'   

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            user_products = BuyProduct.objects.filter(user=self.request.user, product__category=category).select_related('product')
        else:
            user_products = BuyProduct.objects.filter(user=self.request.user).select_related('product')

        return [user_product.product for user_product in user_products]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['user_books'] = BuyProduct.objects.filter(user=self.request.user).select_related('product')
        return context


