import re, soundcloud

from django.shortcuts import render, get_object_or_404

from .models import StaffProfile, Program


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


def program_index(request):
    return HttpResponse('Program Index Page')

def program_detail(request, prog_id):
    return HttpResponse('Program Detail Page: {}'.format(prog_id))

def program_archive(request, prog_id, archive_date):
    ID = "341f473cd62b009a2a8ea8b037d8af49"
    client = soundcloud.Client(client_id=ID)
    track = client.get('/resolve', 
        url='http://soundcloud.com/iowacatholicradio/cwn-080416')
    context = {'title':   track.title,
               'trackid': track.id,}
    return render(request, 'programs/program_archive.html', context)
