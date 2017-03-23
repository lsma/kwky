"""
showtimes.py
LSMA

Services related to formatting Showtime entries.  These functions accept
showtimes in one of the following formats:

[(bool,bool,bool,bool,bool,bool,bool), datetime.time, datetime.timedelta]

"""

import datetime, calendar

WEEKDAYS = 0
START_TIME = 1
DURATION = 2


def flatten(container):
    """Flattens a list.  Thank you, Stack Overflow user hexparrot!"""
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i

def group(items, key):
    """Takes a list, and returns a dict where keys are unique values returned by
    the 'key' parameter and values are lists of indicies of the 'items'
    parameter.

    Example:

    >>> import datetime
    >>> a = datetime.date(1999, 12, 17)
    >>> b = datetime.date(2005, 8, 4)
    >>> c = datetime.date(2011, 12, 25)
    >>> d = datetime.date(2015, 12, 24)
    >>> group_consecutive([a,b,c,d], key=lambda x: x.month)
    {8: [1], 12: [0, 2,3]}
    """
    groups = {}
    for item,index in zip(items,range(len(items))):
        value = key(item)
        if value in groups:
            groups[value].append(item)
        else:
            groups[value] = [item]
    return groups

def group_consecutive(items, key=lambda x: x):
    """Like 'group', but maintains consecutive groups by nesting lists.

    Example:

    >>> import datetime
    >>> a = datetime.date(1999, 12, 17)
    >>> b = datetime.date(2005, 8, 4)
    >>> c = datetime.date(2011, 12, 25)
    >>> d = datetime.date(2015, 12, 24)
    >>> group_consecutive([a,b,c,d], key=lambda x: x.month)
    {8: [[1]], 12: [[0],[2,3]]}

    Notice that the lists are nested into consecutive groups.  'c' and 'd' are
    consecutive items who's month is 12, so they reside in the same sub-list.
    """
    groups = {}
    last_value = None
    for item,index in zip(items,range(len(items))):
        value = key(item)
        if value in groups:
            if value == last_value:
                groups[value][-1].append(index)
            else:
                groups[value].append([index])
        else:
            groups[value] = [[index]]
        last_value = value
    return groups

def format_weekdays(weekdays, weekday_names=calendar.day_name, through='-'):
    """Formats a 7-tuple into a list of weekday names"""
    groups = group_consecutive(weekdays, key=lambda x: bool(x)).get(True, [])
    print(weekdays, groups)
    items = []
    for g in groups:
        if len(g) > 2:
            items.append(weekday_names[g[0]] + through + weekday_names[g[-1]])
        else:
            for i in g: items.append(weekday_names[i])

    return render_list(items)

def render_list(l):
    """Renders a list of strings into human readable form"""
    if len(l) > 2: return ', '.join(l[:-1])+' and '+str(l[-1])
    elif len(l) == 2: return ' and '.join(l)
    elif len(l) == 1: return str(l[0])
    else: return ''


def merge_showtimes(showtimes):
    """Merges showtimes with the same weekdays and time ranges"""
    # merge showtimes with the same time range
    groups = group(showtimes, lambda x: (x[1],x[2]))
    showtimes = []
    for g in groups:
        new_weekdays = tuple(any(x) for x in zip(  *[y[0] for y in groups[g]]   ))
        showtimes.append(  (new_weekdays, (g[0], g[1]) )  )

    # merge showtimes with the same day range
    groups = group(showtimes, lambda x: x[0])
    showtimes = []
    for g in groups:
        showtimes.append(  (g, tuple(sorted( [i[1] for i in groups[g]], key=lambda x: x[0].isoformat()  )) )  )

    return showtimes

def render_showtimes(showtimes,
                     timeformat='{0:%-I}:{0:%M}{0:%p} to {1:%-I}:{1:%M}{1:%p}',
                     entryformat='{days} from {times}',
                     weekday_names=calendar.day_name):
    """Renders showtime tuples into human-readable form"""
    l = []
    for s in showtimes:
        times = []
        for time in s[1]:
            times.append(timeformat.format(time[0],
                datetime.datetime.combine(datetime.date.min, time[0])+time[1]))

        l.append(entryformat.format(days=format_weekdays(s[0],weekday_names=weekday_names),times=render_list(times)))

    return l


if __name__ == "__main__":
    print('Showtime renderer tester\n')
    while True:
        print('************************')
        print('***** New Session ******')
        print('************************')
        print('Ctr+C to exit')
        showtimes = []
        while True:
            print('------------------------')
            print('Enter 7 1s or 0s for each weekday (mon-sun)')
            days = tuple(int(x) for x in input('>'))
            print(format_weekdays(days))
            print('Enter start time hour')
            h = int(input('>'))
            print('Enter duration hour')
            dh = int(input('>'))

            showtimes.append( [days, datetime.time(hour=h), datetime.timedelta(hours=dh)] )

            print('Added: {}'.format(showtimes[-1]))

            print('Add another showtime?')
            if 'y' not in input('>').lower(): break
        print('------------------------')
        print('Result:')
        for f in format_showtime(showtimes): print(f)





