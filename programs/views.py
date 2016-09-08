import re, soundcloud, datetime

from requests import ConnectionError, HTTPError

from django.http import Http404,HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from .models import StaffProfile, Program

# Soundcloud client option for retrieving soundcloud track IDs for embeded
# player in /programs/[abbr]/[mmddyy]
client = soundcloud.Client(client_id=settings.SOUNDCLOUD_ID)

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
    programs = Program.objects.order_by('title')
    context = {'program_list': programs}
    return render(request, 'programs/program_index.html', context)

def program_detail(request, prog_id):
    prog = get_object_or_404(Program, abbr__iexact=prog_id)
    hosts = StaffProfile.objects.filter(program=prog).order_by('org_rank')
    context = {'prog': prog,
               'sc_embed_src': 'http://www.reddit.com',
               'hosts': hosts,}
    return render(request, 'programs/program_detail.html', context)

def program_archive(request, prog_id, month, day, year):
    # Extract date object from the date string
    #   it will be in the form 'mmddyy'
    date = datetime.date(month=int(month),
                         day=int(day),
                         year=int(year))

    # Construct soundcloud urls to try
    base_url = 'http://soundcloud.com/{}/{}-'.format(
        settings.SOUNDCLOUD_UNAME,
        prog_id,
    )
    sc_urls = [base_url+date.strftime('%m%d%y'),
               base_url+date.strftime('%m%d%Y'),]

    for url in sc_urls:
        try:
            track = client.get('/resolve', url=url)
        except HTTPError:
            error_content = 'The requested episode cannot be found.' + \
                            '\nMost likely, you requested an episode ' + \
                            'from a date where no episode was aired.'
            if settings.DEBUG:
                error_content += '\n{}'.format(sc_url)

            raise Http404(error_content)
        except ConnectionError:
            raise HttpResponseServerError('We could not connect to our ' + \
                                          'podcasting service.\nPlease ' + \
                                          'visit {} to listen'.format(sc_url))
    # Get the track from soundcloud
    try:
        track = client.get('/resolve', url=sc_url)
    except HTTPError:
        error_content = 'The requested episode cannot be found.' + \
                        '\nMost likely, you requested an episode ' + \
                        'from a date where no episode was aired.'
        if settings.DEBUG:
            error_content += '\n{}'.format(sc_url)

        raise Http404(error_content)
    except ConnectionError:
        raise HttpResponseServerError('We could not connect to our ' + \
                                      'podcasting service.\nPlease ' + \
                                      'visit {} to listen'.format(sc_url))
    
    # Construct the context, includes track data and date
    context = {'track':   track,
               'date':    date,}

    # Render it
    return render(request, 'programs/program_archive.html', context)
