from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ...models_profile import ParentProfile, Child, Medal, Discount
from ...forms_profile import ParentProfileForm, ChildForm

@login_required
def profile(request):
    """Valideyn profil səhifəsi"""
    from django.utils import timezone
    
    profile, created = ParentProfile.objects.get_or_create(user=request.user)
    children = profile.children.all()
    
    # Aktiv kampaniyalar (hamıya göstərilir)
    today = timezone.now().date()
    campaigns = Discount.objects.filter(
        is_active=True,
        valid_from__lte=today,
        valid_until__gte=today
    ).order_by('-valid_from')
    
    # Hər uşaq üçün medalları əldə et
    children_with_medals = []
    for child in children:
        medals = child.medals.select_related('medal_type').all()
        children_with_medals.append({
            'child': child,
            'medals': medals,
            'medal_count': medals.count()
        })
    
    context = {
        'profile': profile,
        'children_with_medals': children_with_medals,
        'campaigns': campaigns,
        'status': profile.get_status(),
        'total_medals': profile.get_medal_count(),
    }
    return render(request, 'profile/profile.html', context)


@login_required
def edit_profile(request):
    """Profil redaktə"""
    profile, created = ParentProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ParentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil uğurla yeniləndi!')
            return redirect('profile')
    else:
        form = ParentProfileForm(instance=profile)
    
    return render(request, 'profile/edit_profile.html', {'form': form})


@login_required
def add_child(request):
    """Uşaq əlavə et"""
    profile, created = ParentProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = profile
            child.save()
            messages.success(request, f'{child.name} uğurla əlavə edildi!')
            return redirect('profile')
    else:
        form = ChildForm()
    
    return render(request, 'profile/add_child.html', {'form': form})


@login_required
def edit_child(request, child_id):
    """Uşaq məlumatını redaktə et"""
    profile, created = ParentProfile.objects.get_or_create(user=request.user)
    child = get_object_or_404(Child, id=child_id, parent=profile)
    
    if request.method == 'POST':
        form = ChildForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            messages.success(request, f'{child.name} məlumatı yeniləndi!')
            return redirect('profile')
    else:
        form = ChildForm(instance=child)
    
    return render(request, 'profile/edit_child.html', {'form': form, 'child': child})


@login_required
def delete_child(request, child_id):
    """Uşaq məlumatını sil"""
    profile, created = ParentProfile.objects.get_or_create(user=request.user)
    child = get_object_or_404(Child, id=child_id, parent=profile)
    
    if request.method == 'POST':
        child_name = child.name
        child.delete()
        messages.success(request, f'{child_name} məlumatı silindi!')
        return redirect('profile')
    
    return render(request, 'profile/delete_child.html', {'child': child})
