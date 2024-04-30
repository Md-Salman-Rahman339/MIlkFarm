from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'get_balance_after_transaction', 'transaction_type']

    def get_balance_after_transaction(self, obj):
        return obj.account.balance + obj.amount

    get_balance_after_transaction.short_description = 'Balance After Transaction'

    def save_model(self, request, obj, form, change):
        obj.account.balance += obj.amount
        obj.account.save()
        super().save_model(request, obj, form, change)
