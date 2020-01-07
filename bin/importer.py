#!/usr/bin/env python3
""" Import data from sunnybeam """

import datetime
import glob
import os
import sqlite3
import sys


################################################################################
def Verbose(msg):
    """ Be verbose """
    sys.stderr.write("%s\n" % msg)


################################################################################
def getAvailableFiles(datapath):
    """ Get all the files """
    flist = glob.glob(os.path.join(datapath, '*-*-*.CSV'))
    return flist


################################################################################
def analyseFile(fname, conn):
    """ Pull details out of the file """
    # 11-12-20.CSV
    daystr = os.path.basename(fname).replace('.CSV', '')
    daybits = daystr.split('-')
    date = datetime.date(int(daybits[0])+2000, int(daybits[1]), int(daybits[2]))
    curs = conn.cursor()
    curs.execute(f"SELECT id FROM day WHERE date={date}")
    dayid = curs.fetchone()
    if not dayid:
        curs.execute(f"INSERT INTO day (date, today, total) VALUES ({date}, 0.0, 0.0)")
        curs.execute(f"SELECT id FROM day WHERE date={date}")
        dayid = curs.fetchone()

    with open(fname) as fh:
        for line in fh:
            analyse_line(conn, line, dayid[0])


################################################################################
def analyse_hour(conn, dayid, line):
    """ Hour """
    curs = conn.cursor()
    if line[0] not in '0123456789':
        return
    t, power = line.split(';')         # 07:30pm;0.366
    hour = int(t[0:2])
    minute = int(t[3:5])
    ampm = t[5:7]
    if ampm == 'pm' and hour != 12:
        hour += 12
    time = datetime.time(hour, minute, 00)
    curs.execute(f"SELECT id FROM hour WHERE day={dayid} AND hour={hour}")
    hourid = curs.fetchone()
    if not hourid:
        curs.execute(f"INSERT INTO hour (day, hour) VALUES ({dayid}, {hour})")
        curs.execute(f"SELECT id FROM hour WHERE day={dayid} AND hour={hour}")
        hourid = curs.fetchone()
    hourid = hourid[0]

    sql = f"UPDATE hour SET time='{time}', power={float(power)} WHERE day={dayid} AND hour={hour}"
    print(sql)
    curs.execute(sql)


################################################################################
def analyse_line(conn, line, dayid):
    """ Analyse a line of data """
    curs = conn.cursor()
    line = line.strip()
    if not line:
        return
    analyse_hour(conn, dayid, line)
    if line.startswith('E-Today'):
        pwr = line.split(';')[1]
        if pwr:
            today = float(pwr)
            curs.execute(f"UPDATE day SET (today) VAULES ({today}) WHERE id={dayid}")
    if line.startswith('E-Total'):
        pwr = line.split(';')[1]
        if pwr:
            total = float(pwr)
            curs.execute(f"UPDATE day SET (total) VAULES ({total}) WHERE id={dayid}")


################################################################################
def create_database(conn):
    """ Create the database schema """
    curs = conn.cursor()
    try:
        curs.execute("""CREATE TABLE day (
            id INTEGER PRIMARY KEY,
            date  TEXT,
            today REAL default 0,
            total REAL default 0
            )""")
    except sqlite3.OperationalError:
        print("day table already exists")
    try:
        curs.execute("""CREATE TABLE hour (
            id INTEGER PRIMARY KEY,
            time TEXT,
            hour INTEGER default 0,
            power REAL default 0,
            day INTEGER NOT NULL,
            FOREIGN KEY (day) REFERENCES day (id)
            )""")
    except sqlite3.OperationalError:
        print("hour table already exists")


################################################################################
def main():
    """ Main """
    # files = getAvailableFiles("/Volumes/NO NAME/SBEAM/")
    files = getAvailableFiles("/Users/dwagon/Dropbox/SBEAM")
    sqlite_file = "sqlite.sql"
    conn = sqlite3.connect(sqlite_file)
    create_database(conn)
    for f in files:
        Verbose("Analysing %s" % f)
        analyseFile(f, conn)
    conn.commit()
    conn.close()


################################################################################
if __name__ == "__main__":
    main()

# EOF
