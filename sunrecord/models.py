from django.db import models

# Create your models here.

class Day(models.Model):
    date=models.DateField()
    today=models.FloatField(null=True)
    total=models.FloatField(null=True)

    def __unicode__(self):
        return "%s" % self.date

class Hour(models.Model):
    day=models.ForeignKey('Day')
    time=models.TimeField()
    hour=models.IntegerField()
    power=models.FloatField()

    def __unicode__(self):
        return "%s %0.3f" % (self.time, power)

#EOF
