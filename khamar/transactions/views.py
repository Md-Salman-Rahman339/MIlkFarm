from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic import CreateView
from transactions.constants import DEPOSIT
from transactions.forms import DepositForm
from transactions.models import Transaction
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.http import require_http_methods

def send_transaction_email(user,amount,subject,template):
    message=render_to_string(template,{
        'user':user,
        'amount':amount,
    })



class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name='transaction_form.html'
    model=Transaction
    title=''
    success_url=reverse_lazy('deposit_money')

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        user=self.request.user
        if hasattr(user,'account'):
            kwargs.update({'account':user.account})

        else:
            raise Http404("User has no account.")
        return kwargs

    def get_context_data(self, **kwargs: Any):
        context= super().get_context_data(**kwargs)    
        context.update({
            'title':self.title
        })
        return context
    

class DepositMoneyView(TransactionCreateMixin):
    form_class=DepositForm
    title='Deposit'

    def get_initial(self):
        initial={'transaction_type': DEPOSIT}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields=[
                'balance'
            ]
        )

        
        return super().form_valid(form)

