from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LostItemForm, FoundItemForm
from .models import LostItem, FoundItem
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse  # ✅ for reverse('item_list')
from .models import Match
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def home(request):
    return render(request, 'home.html')


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin_panel')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

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

            # Matching logic — find LostItems with similar keywords
            matches = LostItem.objects.filter(
                title__icontains=found_item.title
            ) | LostItem.objects.filter(
                description__icontains=found_item.title
            )

            match_count = 0
            for lost in matches:
                Match.objects.create(lost_item=lost, found_item=found_item)
                match_count += 1

            if match_count > 0:
                # 👇 create dynamic link to only show matched items
                match_url = reverse('item_list') + f"?match_title={found_item.title}"
                messages.success(
                    request,
                    f"""
                    ✅ <strong>Match Found!</strong> We found {match_count} lost item(s) that may match.
                    <a href='{match_url}' class='alert-link'>Click here to view them</a> 🔍
                    """
                )
            else:
                messages.info(request, "Item reported successfully. No matches found yet.")

            return redirect('item_list')
    else:
        form = FoundItemForm()
    return render(request, 'found_form.html', {'form': form})


@login_required
def item_list(request):
    query = request.GET.get('q', '')
    match_title = request.GET.get('match_title', '')

    if match_title:
        # Only show matching LostItems based on match title
        lost_items = LostItem.objects.filter(title__icontains=match_title)
        found_items = FoundItem.objects.none()
    else:
        # Normal search view
        lost_items = LostItem.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        found_items = FoundItem.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'item_list.html', {
        'lost_items': lost_items,
        'found_items': found_items,
        'query': query,
    })


@user_passes_test(lambda u: u.is_superuser)
@login_required
def admin_panel(request):
    if request.method == 'POST':
        if 'delete_lost' in request.POST:
            LostItem.objects.filter(id=request.POST['delete_lost']).delete()
        elif 'delete_found' in request.POST:
            FoundItem.objects.filter(id=request.POST['delete_found']).delete()

    lost_items = LostItem.objects.all()
    found_items = FoundItem.objects.all()
    return render(request, 'admin_panel.html', {
        'lost_items': lost_items,
        'found_items': found_items,
    })