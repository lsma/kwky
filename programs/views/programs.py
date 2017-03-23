import datetime

from django.shortcuts import render, get_object_or_404
from django.conf import settings

from programs.models import Program, ProgramLink, Showtime, StaffProfile
from programs import services

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

    # Get playlist stuff
    prog_playlists = services.get_prog_playlists(prog_id)

    newest_track = None
    if prog_playlists:
        newest_track = services.newest_track(prog_playlists[0])

    playlists = [(services.get_playlist_year(p), p.track_count) for p in prog_playlists]

    # Assemble the context
    context = {'prog': prog,
               'sc_embed_src': 'http://www.reddit.com',
               'hosts': hosts,
               'links': links,
               'showtimes': showtimes,
               'playlists': playlists,
               'newest_track': newest_track,}
    return render(request, 'programs/program_detail.html', context)


def program_archive_year(request, prog_id, year):
    prog = get_object_or_404(Program, abbr__iexact=prog_id)

    playlist = services.get_playlist(prog_id, year)

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

    track = services.get_track(prog_id, date)


    # Construct the context, includes track data and date
    context = {'track':   track,
               'date':    date,
               'program': prog,}

    # Render it
    return render(request, 'programs/program_archive_single.html', context)
