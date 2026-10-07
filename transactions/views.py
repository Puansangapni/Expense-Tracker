from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Transaction
from .forms import TransactionForm

@login_required
def dashboard_view(request):

    # Mengambil semua transaksi milik user yang sedang login
    transactions = Transaction.objects.filter(
        user=request.user
    )

    # Total income
    total_income = transactions.filter(
        type="income"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    # Total expense
    total_expense = transactions.filter(
        type="expense"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    # Balance
    balance = total_income - total_expense

    # 5 transaksi terbaru
    recent_transactions = transactions.order_by(
        "-date",
        "-created_at"
    )[:5]

    context = {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "recent_transactions": recent_transactions,
    }

    return render(
        request,
        "dashboard.html",
        context
    )


@login_required
def transaction_list(request):

    transactions = Transaction.objects.filter(
        user=request.user  
    ).order_by(
        "-date",
        "-created_at"
    )

    context = {
        "transactions": transactions
    }

    return render(
        request,
        "transactions/transaction_list.html",
        context
    )


@login_required
def transaction_create(request):

    if request.method == "POST":

        form = TransactionForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            transaction = form.save(commit=False)

            transaction.user = request.user

            transaction.save()

            return redirect("transaction_list")

    else:
        form = TransactionForm(
            user=request.user
        )

    context = {
        "form": form,
        "title": "Add Transaction",
        "button_text": "Add Transaction",
    }

    return render(
        request,
        "transactions/transaction_form.html",
        context
    )

@login_required
def transaction_update(request, pk):

    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        form = TransactionForm(
            request.POST,
            instance=transaction,
            user=request.user
        )

        if form.is_valid():
            form.save()
            return redirect("transaction_list")

    else:
        form = TransactionForm(
            instance=transaction,
            user=request.user
        )

    context = {
        "form": form,
        "title": "Edit Transaction",
        "button_text": "Update Transaction",
    }

    return render(
        request,
        "transactions/transaction_form.html",
        context
    )

@login_required
def transaction_delete (request, pk):

    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        transaction.delete()
        return redirect("transaction_list")

    context = {
        "transaction": transaction,
    }
    
    return render(
        request,
        "transactions/transaction_confirm_delete.html",
        context
    )
    