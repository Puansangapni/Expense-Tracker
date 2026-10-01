from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Transaction

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