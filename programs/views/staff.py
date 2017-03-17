from django.shortcuts import render, get_object_or_404

from programs.models import StaffProfile, StaffLink


def staff_index(request):
    staff_members = StaffProfile.objects.order_by('org_rank')
    context = {'staff_members': staff_members}
    return render(request, 'programs/staff_index.html', context)

def staff_detail(request, ln, fn):
    member = get_object_or_404(StaffProfile,
        first_name__iexact=fn,
        last_name__iexact=ln)
    context = {'member': member}
    return render(request, 'programs/staff_detail.html', context)
