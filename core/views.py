from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LostItemForm, FoundItemForm
from .models import LostItem, FoundItem
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

@login_required
def report_lost(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST)
        if form.is_valid():
            lost_item = form.save(commit=False)
            lost_item.user = request.user
            lost_item.save()
            return redirect('item_list')
    else:
        form = LostItemForm()
    return render(request, 'lost_form.html', {'form': form})

@login_required
def report_found(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            found_item = form.save(commit=False)
            found_item.user = request.user
            found_item.save()
            return redirect('item_list')
    else:
        form = FoundItemForm()
    return render(request, 'found_form.html', {'form': form})

@login_required
def item_list(request):
    query = request.GET.get('q', '')
    lost_items = LostItem.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    found_items = FoundItem.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'item_list.html', {
        'lost_items': lost_items,
        'found_items': found_items,
        'query': query,
    })

@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return redirect('home')
    lost_items = LostItem.objects.all()
    found_items = FoundItem.objects.all()
    return render(request, 'admin_panel.html', {
        'lost_items': lost_items,
        'found_items': found_items,
    })
