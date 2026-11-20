import json
import pandas as pd
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm


def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    cat_labels, cat_values, month_labels, month_values = [], [], [], []
    total = 0

    if expenses.exists():
        df = pd.DataFrame(list(expenses.values('amount', 'category', 'date')))
        df['amount'] = df['amount'].astype(float)
        df['date'] = pd.to_datetime(df['date'])
        total = round(df['amount'].sum(), 2)

        by_cat = df.groupby('category')['amount'].sum().round(2)
        cat_labels, cat_values = list(by_cat.index), list(by_cat.values)

        by_month = df.groupby(df['date'].dt.strftime('%Y-%m'))['amount'].sum().round(2).sort_index()
        month_labels, month_values = list(by_month.index), list(by_month.values)

    context = {
        'expenses': expenses,
        'total': total,
        'cat_labels': json.dumps(cat_labels),
        'cat_values': json.dumps(cat_values),
        'month_labels': json.dumps(month_labels),
        'month_values': json.dumps(month_values),
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def add_expense(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        return redirect('dashboard')
    return render(request, 'tracker/expense_form.html', {'form': form, 'heading': 'Add Expense'})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'tracker/expense_form.html', {'form': form, 'heading': 'Edit Expense'})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return render(request, 'tracker/confirm_delete.html', {'expense': expense})


@login_required
def export_csv(request):
    expenses = Expense.objects.filter(user=request.user).values('title', 'amount', 'category', 'date')
    df = pd.DataFrame(list(expenses))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    df.to_csv(response, index=False)
    return response
