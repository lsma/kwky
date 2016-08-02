from django.shortcuts import render

from .models import StaffProfile, Program


def staff_index(request):
    staff_members = StaffProfile.objects.order_by('-org_rank')
    context = {'staff_members': staff_members}
    return render(request, 'programs/staff_index.html', context)

def staff_detail(request, name):
    return HttpResponse('Staff Detail Page: {}'.format(name))


def program_index(request):
    return HttpResponse('Program Index Page')

def program_detail(request, prog_id):
    return HttpResponse('Program Detail Page: {}'.format(prog_id))

def program_archive(request, prog_id, archive_year):
    return HttpResponse('Program Archive Page: {} from {}'.format(prog_id,
    archive_year))
