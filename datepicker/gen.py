#!/usr/bin/python3

from datetime import date,timedelta

_months = ['january','february','march','april','may','june','july',
           'august','september','october','november','december']
def month_sort(x): return _months.index(x.lower())

startdate = date(2012,1,1)
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
    dd[year][month].append(cur.day)
    cur += aday

print('<html>\n  <head>\n    <link rel="stylesheet" type="text/css" href="./theme.css"></link>  </head>\n  <body>\n    <div class="datetime">\n      <div>')

print('      <p>Archives</p>')
print('      <div id="archives" class="years dateframe">')
for year in sorted(dd.keys()):
    print('        <div><a href="#{0}">{0}</a></div>'.format(year))
print('      </div>')

for year in sorted(dd.keys()):
    print('      <p><a href="#archives">&lt;&lt; {}</a></p>'.format(year))
    print('      <div id="{}" class="months dateframe">'.format(year))
    for month in sorted(dd[year].keys(), key=month_sort):
        print('        <div><a href="#{}-{}">{}</a></div>'.format(month[:3],year,month))
    print('      </div>')
        
for year in sorted(dd.keys()):
    for month in sorted(dd[year].keys(), key=month_sort):
        print('      <p><a href="#{0}">&lt;&lt; {1}, {0}</a></p>'.format(year, month))
        print('      <div id="{}-{}" class="days dateframe">'.format(month[:3],year))
        for day in dd[year][month]:
            print('        <div><a href="#">{}</a></div>'.format(day))
        print('      </div>')
        

print('    </div>\n    </div>\n  </body>\n</html>')

