#!/usr/bin/python3

from datetime import date,timedelta

def month_length(any_day):
    """Thanks Augusto Men!"""
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return (next_month - timedelta(days=next_month.day)).day

_months = ['january','february','march','april','may','june','july',
           'august','september','october','november','december']
def month_sort(x): return _months.index(x.lower())

validator = lambda d: d.strftime("%w") == "2"
day_link = "http://soundcloud.com/iowacatholicradio/fot-%m%d%y"
startdate = date(2013,10,21)
enddate = date.today()

dd = {}
aday = timedelta(days=1)
cur = date(*startdate.timetuple()[:3])
while cur <= enddate:
    year = cur.strftime('%Y')
    month = cur.strftime('%B')
    if year not in dd:
        dd[year] = {}
    if month not in dd[year]:
        dd[year][month] = []
        month_len = month_length(cur)
        for x in ('S','M','T','W','T','F','S'):
            dd[year][month].append(("span", "weekday-header", None, x))
        for x in range(cur.weekday()+1, 0, -1):
            dd[year][month].append(("span", "last-month", None, month_len-x))
    tag,clss = ("a","daylink") if validator(cur) else ("span","daybox")
    href = cur.strftime(day_link)
    dd[year][month].append((tag, clss, href, cur.day))
    cur += aday

print('<html>\n  <head>\n    <link rel="stylesheet" type="text/css" href="./theme.css"></link>  </head>\n  <body>\n    <div class="datetime">\n      <div class="datetime-relbox">')

print('      <div id="archives" class="years dateframe">')
print('        <p class="dateframe-title"><a href="#archives">Archives</a></p>')
print('        <div class="dateframe-content">')
for year in sorted(dd.keys()):
    print('          <a class="dateframe-item" href="#{0}">{0}</a>'.format(year))
print('        </div>')
print('      </div>')

for year in sorted(dd.keys()):
    print('      <div id="{}" class="months dateframe">'.format(year))
    print('        <p class="dateframe-title"><a href="#archives">{}</a></p>'.format(year))
    print('        <div class="dateframe-content">')
    for month in sorted(dd[year].keys(), key=month_sort):
        print('          <a class="dateframe-item" href="#{}-{}">{}</a>'.format(month[:3],year,month))
    print('        </div>')
    print('      </div>')
        
for year in sorted(dd.keys()):
    for month in sorted(dd[year].keys(), key=month_sort):
        print('      <div id="{}-{}" class="days dateframe">'.format(month[:3],year))
        print('        <p class="dateframe-title"><a href="#{0}">{1}, {0}</a></p>'.format(year, month))
        print('        <div class="dateframe-content">')
        for tag,clss,href,day in dd[year][month]:
            print('          <{0} class="dateframe-item {1}" href="{2}">{3}</{0}>'.format(tag,clss,href,day))
        print('        </div>')
        print('      </div>')
        

print('    </div>\n    </div>\n  </body>\n</html>')

