#!/usr/bin/env python3
""" Graph generation """

import os
import sys
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'sunny.sunny.settings'
django.setup()
from sunny.beam.models import Day, Hour    # noqa


################################################################################
def graphOverTime():
    """ TODO """
    days = Day.objects.filter(today__gt=0)
    daycount = 0
    f = open('graphOverTime.csv', 'w')
    f.write("day,time,power\n")
    for day in days:
        hours = Hour.objects.filter(day=day).order_by('time')
        for hour in hours:
            f.write("%d,%s,%f\n" % (daycount, hour.time, hour.power))
        daycount += 1
    f.close()


################################################################################
def powerGeneration():
    """ TODO """
    days = Day.objects.filter(total__gt=0).order_by('date')
    f = open('powerGeneration.csv', 'w')
    f.write("day,total_power,daily_power\n")
    for day in days:
        f.write("%s,%f,%f\n" % (day.date, day.total, day.today))
    f.close()


################################################################################
def monthlyHistograph():
    """ TODO """
    oldmonth = ""
    daycount = 0
    monthdata = {}
    alltime = {}
    buckets = {}
    days = Day.objects.filter(today__gt=0).order_by('date')
    hourset = set()
    for day in days:
        month = "%d_%02d" % (day.date.year, day.date.month)
        if month != oldmonth:
            if oldmonth:
                monthdata[oldmonth] = {}
                monthdata[oldmonth] = buckets
                for b in buckets:
                    monthdata[oldmonth][b]['avg'] = buckets[b]['sum']/daycount
            oldmonth = month
            daycount = 0
            buckets = {}
        daycount += 1
        hours = Hour.objects.filter(day=day)
        for hour in hours:
            if hour.time not in buckets:
                buckets[hour.time] = {'min': 999, 'max': 0, 'sum': 0}
                hourset.add(hour.time)
            if hour.time not in alltime:
                alltime[hour.time] = {'min': 999, 'max': 0}
            buckets[hour.time]['sum'] += hour.power
            if hour.power < buckets[hour.time]['min']:
                buckets[hour.time]['min'] = hour.power
            if hour.power > buckets[hour.time]['max']:
                buckets[hour.time]['max'] = hour.power
            if hour.power < alltime[hour.time]['min']:
                alltime[hour.time]['min'] = hour.power
            if hour.power > alltime[hour.time]['max']:
                alltime[hour.time]['max'] = hour.power
    monthdata[oldmonth] = buckets
    for b in buckets:
        monthdata[oldmonth][b]['avg'] = buckets[b]['sum'] / daycount

    months = sorted(monthdata.keys())
    f = open('graphMonthHistogram.csv', 'w')
    string = "Time,Min,Max,"
    for m in months:
        string += "%s_min,%s_avg,%s_max," % (m, m, m)
    f.write("%s\n" % string[:-1])
    for t in sorted(list(hourset)):
        string = "%s,%f,%f," % (t, alltime[t]['min'], alltime[t]['max'])
        for m in months:
            string += "%f,%f,%f," % (monthdata[m][t]['min'], monthdata[m][t]['avg'], monthdata[m][t]['max'])
        f.write("%s\n" % string[:-1])
    f.close()


################################################################################
def histograph():
    """ TODO """
    buckets = {}
    days = Day.objects.filter(today__gt=0)
    for day in days:
        hours = Hour.objects.filter(day=day)
        for hour in hours:
            if hour.time not in buckets:
                buckets[hour.time] = {'min': 999, 'max': 0, 'sum': 0}
            buckets[hour.time]['sum'] += hour.power
            if hour.power < buckets[hour.time]['min']:
                buckets[hour.time]['min'] = hour.power
            if hour.power > buckets[hour.time]['max']:
                buckets[hour.time]['max'] = hour.power

    f = open('graphHistogram.csv', 'w')
    f.write("Time,Avg,Min,Max\n")
    for k, v in sorted(buckets.items()):
        f.write("%s,%f,%f,%f\n" % (k, v['sum']/len(days), v['min'], v['max']))
    f.close()


################################################################################
def main():
    """ TODO """
    firstday = Day.objects.filter(today__gt=0).order_by('date')[0]
    lastday = Day.objects.filter(today__gt=0).order_by('-date')[0]
    sys.stderr.write("%s to %s\n" % (firstday, lastday))
    graphOverTime()
    powerGeneration()
    histograph()
    monthlyHistograph()


################################################################################
if __name__ == "__main__":
    main()

# EOF
