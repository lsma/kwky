from django.http import HttpResponse


def staff_index(request):
    return HttpResponse('Staff Index Page')

def staff_detail(request, name):
    return HttpResponse('Staff Detail Page: {}'.format(name))


def program_index(request):
    return HttpResponse('Program Index Page')

def program_detail(request, prog_id):
    return HttpResponse('Program Detail Page: {}'.format(prog_id))

def program_archive(request, prog_id, archive_year):
    return HttpResponse('Program Archive Page: {} from {}'.format(prog_id,
    archive_year))
