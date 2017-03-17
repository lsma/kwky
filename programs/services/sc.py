import soundcloud, re, datetime

from django.conf import settings

from django.http import Http404,HttpResponseServerError
from requests import ConnectionError, HTTPError

PROPER_PLAYLIST = re.compile(
        "http://soundcloud.com/{}/sets/(\w\w\w)-(\d\d)".format(
            settings.SOUNDCLOUD_UNAME))

ALL_PLAYLISTS = "http://soundcloud.com/{}/sets".format(settings.SOUNDCLOUD_UNAME)

class InvalidSoundCloudURLFormat(Exception): pass

def initialize_soundcloud():
    try:
        return soundcloud.Client(client_id=settings.SOUNDCLOUD_ID)

    except:
        raise HttpResponseServerError('We could not connect to our ' + \
            'podcasting service.\nPlease visit ' + \
            'http://soundcloud.com/{} '.format(settings.SOUNDCLOUD_UNAME) + \
            'to listen.')

def get_all_playlists(client):
    try:
        return client.get('/resolve', url=ALL_PLAYLISTS)

    except:
        raise HttpResponseServerError('We could not connect to our ' + \
            'podcasting service.\nPlease visit ' + \
            'http://soundcloud.com/{} '.format(settings.SOUNDCLOUD_UNAME) + \
            'to listen.')

def is_valid_playlist(p):
    """Takes a SoundCloud playlist and returns a bool as to wether it is valid"""
    return PROPER_PLAYLIST.match(p.permalink_url) != None

def get_playlist_year(p):
    """Takes a SoundCloud playlist for a podcast archive and returns the year"""
    if not PROPER_PLAYLIST.match(p.permalink_url):
        raise InvalidSoundCloudURLFormat("Invalid url ('{}')".format(p.permalink_url))
    return p.permalink_url.split('/')[-1].split('-')[-1]

def get_playlist_program(p):
    """Takes a SoundCloud playlist for a podcast archive and returns the program id"""
    if not PROPER_PLAYLIST.match(p.permalink_url):
        raise InvalidSoundCloudURLFormat("Invalid url ('{}')".format(p.permalink_url))
    return p.permalink_url.split('/')[-1].split('-')[0]

def get_prog_playlists(prog_id):
    """Returns a list of playlists for a given program"""
    client = initialize_soundcloud()

    prog_playlists = [] # this will hold all the playlists that are this
                        # program's archives

    for playlist in get_all_playlists(client):
        if is_valid_playlist(playlist):
            playlist_prog_id = get_playlist_program(playlist)

            if playlist_prog_id == prog_id:      # if the program IDs match, add it
                prog_playlists.append(playlist)

    prog_playlists.sort(key=lambda x: get_playlist_year(x), reverse=True)

    return prog_playlists

def newest_track(playlist):
    """Returns the newest track from a playlist"""
    def _key(x):
        # Turn the y/m/d values into number of days since 01/01/0001 for sorting
        #raise Exception("{}/{}/{}".format(x['release_year'],x['release_month'],x['release_day']))

        return datetime.date(x['release_year'] if x['release_year'] else 1,
                             x['release_month'] if x['release_month'] else 1,
                             x['release_day'] if x['release_day'] else 1).toordinal()

    return sorted(playlist.tracks, key=_key)[-1]

def get_playlist(prog_id, year):
    """Returns a playlist for a given program and year"""
    client = initialize_soundcloud()

    # Construct soundcloud url
    sc_url = 'http://soundcloud.com/{}/sets/{}-{}'.format(
        settings.SOUNDCLOUD_UNAME,
        prog_id,
        year
    )

    try:
        return client.get('/resolve', url=sc_url)

    except HTTPError as err:
        raise Http404('The requested year cannot be found.' + \
                      '\nMost likely, you requested an year ' + \
                      'in which this program was never aired.')

    except ConnectionError:
        raise HttpResponseServerError('We could not connect to our ' + \
                                      'podcasting service.\nPlease ' + \
                                      'visit {} to listen.'.format(sc_url))


def get_track(prog_id, date):
    """Returns a track for a given program and date"""
    client = initialize_soundcloud()

    # Construct soundcloud urls to try
    url = 'http://soundcloud.com/{}/{}-{}'.format(
        settings.SOUNDCLOUD_UNAME,
        prog_id,
        date.strftime('%m%d%y'),
    )

    # Get the track from soundcloud
    try:
        return client.get('/resolve', url=url)

    except HTTPError as err:
        raise Http404('The requested episode cannot be found.' + \
                      '\nMost likely, you requested a date ' + \
                      'in which this program was never aired.')

    except ConnectionError:
        raise HttpResponseServerError('We could not connect to our ' + \
                                      'podcasting service.\nPlease ' + \
                                      'visit {} to listen.'.format(url))

