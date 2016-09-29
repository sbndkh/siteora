from django.db import models

class Filing(models.Model):
    fil_id = models.BigIntegerField(primary_key=True)
    apptype = models.CharField(max_length=64)
    jobtype = models.CharField(max_length=64)
    jobtext = models.CharField(max_length=4000)
    ObjName = models.CharField(max_length=4000)
    eqpName = models.CharField(max_length=4000)
    DateReqStart = models.DateField()
    DateReqFinish = models.DateField()
    dep_id = models.BigIntegerField()
    dep_name = models.CharField(max_length=1000)
    #redytime = models.FloatField()
    #senddatetime = models.DateField()

    class Meta:
        db_table = 'allrequest'

