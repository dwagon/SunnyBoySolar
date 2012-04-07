#!/opt/local/bin/python2.7

import os, sys, glob, datetime
os.environ['DJANGO_SETTINGS_MODULE']='solar.settings'
from solar.sunrecord.models import Day, Hour
from django.core.exceptions import ObjectDoesNotExist

datapath="/Volumes/NO NAME/SBEAM/"

################################################################################
def Verbose(msg):
    sys.stderr.write("%s\n" % msg)

################################################################################
def getAvailableFiles():
    flist=glob.glob(os.path.join(datapath,'*-*-*.CSV'))
    return flist

################################################################################
def analyseFile(fname):
    # 11-12-20.CSV
    daystr=os.path.basename(fname).replace('.CSV','')
    daybits=daystr.split('-')
    date=datetime.date(int(daybits[0])+2000, int(daybits[1]), int(daybits[2]))
    try:
        dayobj=Day.objects.get(date=date)
    except ObjectDoesNotExist:
        dayobj=Day(date=date)
        dayobj.save()

    f=open(fname)
    for line in f:
        line=line.strip()
        if not line:
            continue
        if line[0] in '0123456789':
            t,power=line.split(';')         # 07:30pm;0.366
            hour=int(t[0:2])
            minute=int(t[3:5])
            ampm=t[5:7]
            if ampm=='pm' and hour!=12:
                hour+=12
            time=datetime.time(hour, minute, 00)
            try:
                hourobj=Hour.objects.get(day=dayobj, time=time)
            except ObjectDoesNotExist:
                hourobj=Hour(day=dayobj, time=time, hour=hour)
            hourobj.power=float(power)
            hourobj.save()
        if line.startswith('E-Today'):
            pwr=line.split(';')[1]
            if pwr:
                dayobj.today=float(pwr)
        if line.startswith('E-Total'):
            pwr=line.split(';')[1]
            if pwr:
                dayobj.total=float(pwr)
    f.close()
    dayobj.save()

################################################################################
def main():
    files=getAvailableFiles()
    for f in files:
        Verbose("Analysing %s" % f)
        analyseFile(f)

################################################################################
if __name__=="__main__":
        main()

#EOF
