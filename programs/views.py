import re, soundcloud, datetime

from requests import ConnectionError, HTTPError

from django.http import Http404,HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from .models import StaffProfile, Program, StaffLink, ProgramLink, Showtime

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
    # Get the program's entry from the database
    prog = get_object_or_404(Program, abbr__iexact=prog_id)

    # Get the host's entry from the database
    hosts = StaffProfile.objects.filter(program=prog).order_by('org_rank')
    links = ProgramLink.objects.filter(program=prog)
    showtimes = Showtime.objects.filter(program=prog)

    ## Get all soundcloud playlists for this program
    ## (there is a playlist for each year)

    # Grab all playlists
    all_playlists = client.get('/resolve',
        url='http://soundcloud.com/{}/sets'.format(settings.SOUNDCLOUD_UNAME))

    # all_playlists now holds all the playlists of the user.  We will have to
    # sort out the ones which are not for this particular program

    prog_playlists = [] # this will hold all the playlists containing this program's archives
    for playlist in all_playlists:

        # this will extract the program id from the url
        # eg: http://soundcloud.com/iowacatholicradio/prg-17
        #                                             ^^^
        playlist_prog_id = playlist.permalink_url.split('/')[-1].split('-')[0]

        if playlist_prog_id == prog_id:      # if the program IDs match, add it

            # It will make the template unreadable if we pass through this raw
            # soundcloud api data, so let's pull out only the data we need before
            # rendering the template.  We just need year and track count.
            year = playlist.permalink_url.split('/')[-1].split('-')[-1] # see comment @ playlist_prog_id = ...
            prog_playlists.append((year,playlist.track_count))

    prog_playlists.sort(key=lambda x: x[0], reverse=True)

    # Great!  Now we have a list of all the years and urls of all the playlists
    # pertaining to this program in 'prog_playlists'

    # Now we just have to get the latest track from the latest playlist.
    newest_track = None
    if prog_playlists:
        newest_playlist_url = 'http://soundcloud.com/{}/sets/{}-{}'.format(
            settings.SOUNDCLOUD_UNAME,
            prog_id,
            prog_playlists[0][0],
        )


        try:
            newest_playlist = client.get('/resolve', url=newest_playlist_url)
        except HTTPError as err:
            error_content = 'The requested year cannot be found.' + \
                            '\nMost likely, you requested an year ' + \
                            'in which this program was never aired.'

            if settings.DEBUG:
                error_content += '\n{}'.format(sc_url)
                raise Http404(error_content)
        except ConnectionError:
            raise HttpResponseServerError('We could not connect to our ' + \
                                          'podcasting service.\nPlease ' + \
                                          'visit {} to listen.'.format(url))

        newest_track = sorted(newest_playlist.tracks, key=lambda x: x['created_at'])[-1]

    context = {'prog': prog,
               'sc_embed_src': 'http://www.reddit.com',
               'hosts': hosts,
               'links': links,
               'showtimes': showtimes,
               'playlists': prog_playlists,
               'newest_track': newest_track,}
    return render(request, 'programs/program_detail.html', context)

def program_archive_year(request, prog_id, year):
    prog = get_object_or_404(Program, abbr__iexact=prog_id)

    # Construct soundcloud urls to try
    sc_url = 'http://soundcloud.com/{}/sets/{}-{}'.format(
        settings.SOUNDCLOUD_UNAME,
        prog_id,
        year
    )

    # Get the playlist from soundcloud
    try:
        playlist = client.get('/resolve', url=sc_url)
    except HTTPError as err:
        error_content = 'The requested year cannot be found.' + \
                        '\nMost likely, you requested an year ' + \
                        'in which this program was never aired.'
        if settings.DEBUG:
            error_content += '\n{}'.format(sc_url)

        raise Http404(error_content)

    except ConnectionError:
        raise HttpResponseServerError('We could not connect to our ' + \
                                      'podcasting service.\nPlease ' + \
                                      'visit {} to listen.'.format(sc_url))


    # Construct the context, includes track data and date
    context = {'playlist':   playlist,
               'year':    '20{}'.format(year),
               'program': prog,}

    # Render it
    return render(request, 'programs/program_archive_year.html', context)

def program_archive_single(request, prog_id, month, day, year):
    prog = get_object_or_404(Program, abbr__iexact=prog_id)

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

    # Get the track from soundcloud
    for url in sc_urls:
        try:
            track = client.get('/resolve', url=url)
        except HTTPError:
            error_content = 'The requested episode cannot be found.' + \
                            '\nMost likely, you requested an episode ' + \
                            'from a date where no episode was aired.'
            if settings.DEBUG:
                error_content += '\n{}'.format(sc_urls)

            raise Http404(error_content)
        except ConnectionError:
            raise HttpResponseServerError('We could not connect to our ' + \
                                          'podcasting service.\nPlease ' + \
                                          'visit {} to listen.'.format(url))


    # Construct the context, includes track data and date
    context = {'track':   track,
               'date':    date,
               'program': prog,}

    # Render it
    return render(request, 'programs/program_archive_single.html', context)
