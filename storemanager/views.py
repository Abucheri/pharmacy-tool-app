from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponse
import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    title = "Welcome"
    context = {
        "title": title,
    }
    # return render(request, 'home.html', context)
    return redirect('/list_items')


@login_required
def list_items(request):
    header = 'List of Drugs in Stock'
    form = DrugsSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        'header': header,
        'queryset': queryset,
        'form': form
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(  # category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value())

        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of Drugs in Stock.csv" '
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, 'list_items.html', context)


@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'The item has been added to Stock')
        return redirect('/list_items')
    context = {
        'form': form,
        'title': 'Add Drugs',
    }
    return render(request, 'add_items.html', context)


def update_drugs(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid:
            form.save()
            messages.success(request, 'The item has been updated')
            return redirect('/list_items')
    context = {
        'form': form
    }
    return render(request, 'update_items.html', context)


def delete_drugs(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'The item has been removed from Stock')
        return redirect('/list_items')
    return render(request, 'delete_items.html')


def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset
    }
    return render(request, 'item_detail.html', context)


def issue_drugs(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.received_quantity = 0
        instance.quantity -= instance.issued_quantity
        # instance.issued_by = str(request.user)
        instance.issued_by = str(request.user)
        messages.success(request, 'The drug has been issued successfully. ' + str(instance.quantity) + ' ' + str(
            instance.item_name) + 's left in stock.')
        instance.save()

        return redirect('/item_detail/' + str(instance.id))

    context = {
        'title': 'Issue ' + str(queryset.item_name),
        'queryset': queryset,
        'form': form,
        'username': 'Issued by ' + str(request.user),
    }
    return render(request, 'add_items.html', context)


def receive_drugs(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issued_quantity = 0
        instance.quantity += instance.received_quantity
        instance.received_by = str(request.user)
        instance.save()
        messages.success(request, 'The drug has been received successfully. ' + str(instance.quantity) + ' ' + str(
            instance.item_name) + 's now in stock.')

        return redirect('/item_detail/' + str(instance.id))

    context = {
        'title': 'Receive ' + str(queryset.item_name),
        'instance': queryset,
        'form': form,
        'username': 'Received by ' + str(request.user),
    }
    return render(request, 'add_items.html', context)


def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'The reorder level for ' + str(instance.item_name) + ' has been updated to ' + str(
            instance.reorder_level))

        return redirect('/list_items')

    context = {
        'instance': queryset,
        'form': form
    }
    return render(request, 'add_items.html', context)


@login_required
def stock_list_history(request):
    header = 'Transaction History'
    queryset = StockHistory.objects.all()
    form = DrugsHistorySearchForm(request.POST or None)
    context = {
        "header": header,
        "queryset": queryset,
        "form": form,
    }
    if request.method == 'POST':
        category = form['category'].value()
        queryset = StockHistory.objects.filter(
            item_name__icontains=form['item_name'].value(),
            last_updated__range=[
                form['start_date'].value(),
                form['end_date'].value()
            ]
        )
        if category != '':
            queryset = queryset.filter(category_id=category)

        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Transaction History.csv"'
            writer = csv.writer(response)
            writer.writerow(
                ['CATEGORY',
                 'ITEM NAME',
                 'QUANTITY',
                 'ISSUED QUANTITY',
                 'RECEIVED QUANTITY',
                 'RECEIVED BY',
                 'ISSUED BY',
                 'LAST UPDATED']
            )
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [stock.category,
                     stock.item_name,
                     stock.quantity,
                     stock.issued_quantity,
                     stock.received_quantity,
                     stock.received_by,
                     stock.issued_by,
                     stock.last_updated]
                )
            return response

        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }
    return render(request, 'stock_list_history.html', context)
