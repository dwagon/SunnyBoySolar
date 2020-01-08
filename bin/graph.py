#!/usr/bin/env python3
""" Graph generation """

import sqlite3


################################################################################
def graphOverTime(conn):
    """ TODO """
    curs = conn.cursor()
    curs.execute("SELECT id FROM day WHERE today>0 ORDER BY date")
    all_days = curs.fetchall()
    daycount = 0
    with open('graphOverTime.csv', 'w') as fh:
        fh.write("day,time,power\n")
        for day in all_days:
            curs.execute(f"SELECT time, power FROM hour WHERE day={day[0]} ORDER BY hour")
            all_hours = curs.fetchall()
            for hour in all_hours:
                fh.write("%d,%s,%f\n" % (daycount, hour[0], hour[1]))
            daycount += 1


################################################################################
def powerGeneration(conn):
    """ TODO """
    curs = conn.cursor()
    curs.execute("SELECT date, total, today FROM day WHERE today>0 ORDER BY date")
    all_days = curs.fetchall()
    with open('powerGeneration.csv', 'w') as fh:
        fh.write("day,daily_power\n")
        for day in all_days:
            fh.write(f"%s,%f\n" % (day[0], day[2]))


################################################################################
def monthlyHistograph(conn):
    """ TODO """
    curs = conn.cursor()
    oldmonth = ""
    daycount = 0
    monthdata = {}
    alltime = {}
    buckets = {}
    curs.execute("SELECT id, date FROM day WHERE today>0 ORDER BY date")
    days = curs.fetchall()
    hourset = set()
    for day in days:
        month = "%d_%02d" % (int(day[1].split('-')[0]), int(day[1].split('-')[1]))
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
        curs.execute(f"SELECT time, power FROM hour WHERE day={day[0]} ORDER BY hour")
        hours = curs.fetchall()
        for hour in hours:
            if hour[0] not in buckets:
                buckets[hour[0]] = {'min': 999, 'max': 0, 'sum': 0}
                hourset.add(hour[0])
            if hour[0] not in alltime:
                alltime[hour[0]] = {'min': 999, 'max': 0}
            buckets[hour[0]]['sum'] += hour[1]
            if hour[1] < buckets[hour[0]]['min']:
                buckets[hour[0]]['min'] = hour[1]
            if hour[1] > buckets[hour[0]]['max']:
                buckets[hour[0]]['max'] = hour[1]
            if hour[1] < alltime[hour[0]]['min']:
                alltime[hour[0]]['min'] = hour[1]
            if hour[1] > alltime[hour[0]]['max']:
                alltime[hour[0]]['max'] = hour[1]
    monthdata[oldmonth] = buckets
    for b in buckets:
        monthdata[oldmonth][b]['avg'] = buckets[b]['sum'] / daycount

    months = sorted(monthdata.keys())
    with open('graphMonthHistogram.csv', 'w') as fh:
        string = "Time,Min,Max,"
        for m in months:
            string += "%s_min,%s_avg,%s_max," % (m, m, m)
        fh.write("%s\n" % string[:-1])
        for t in sorted(list(hourset)):
            string = "%s,%f,%f," % (t, alltime[t]['min'], alltime[t]['max'])
            for m in months:
                string += "%f,%f,%f," % (monthdata[m][t]['min'], monthdata[m][t]['avg'], monthdata[m][t]['max'])
            fh.write("%s\n" % string[:-1])


################################################################################
def histograph(conn):
    """ TODO """
    curs = conn.cursor()
    buckets = {}
    curs.execute("SELECT id FROM day WHERE today>0 ORDER BY date")
    all_days = curs.fetchall()
    for day in all_days:
        sql = f"SELECT time, power FROM hour WHERE day={day[0]}"
        curs.execute(sql)
        for hour in curs.fetchall():
            if hour[0] not in buckets:
                buckets[hour[0]] = {'min': 999, 'max': 0, 'sum': 0}
            buckets[hour[0]]['sum'] += hour[1]
            if hour[1] < buckets[hour[0]]['min']:
                buckets[hour[0]]['min'] = hour[1]
            if hour[1] > buckets[hour[0]]['max']:
                buckets[hour[0]]['max'] = hour[1]

    with open('graphHistogram.csv', 'w') as fh:
        fh.write("Time,Avg,Min,Max\n")
        for k, v in sorted(buckets.items()):
            fh.write("%s,%f,%f,%f\n" % (k, v['sum']/len(all_days), v['min'], v['max']))


################################################################################
def main():
    """ TODO """
    sqlite_file = "sqlite.sql"
    conn = sqlite3.connect(sqlite_file)

    # firstday = Day.objects.filter(today__gt=0).order_by('date')[0]
    # lastday = Day.objects.filter(today__gt=0).order_by('-date')[0]
    # sys.stderr.write("%s to %s\n" % (firstday, lastday))
    graphOverTime(conn)
    powerGeneration(conn)
    histograph(conn)
    monthlyHistograph(conn)


################################################################################
if __name__ == "__main__":
    main()

# EOF
