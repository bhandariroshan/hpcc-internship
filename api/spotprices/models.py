from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.contrib.postgres.fields import JSONField

 
class SpotPrices(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.CharField(max_length=200)

    api_price =  models.FloatField()
    cli_price =  models.FloatField(max_length=10)
    region =  models.CharField(max_length=200)
    time =  models.CharField(max_length=200)

    pay_as_you_go_price =  models.FloatField()
    one_year_reserved_price =  models.FloatField()
    three_year_reserved_price =  models.FloatField()

    per_saving_paygo =  models.CharField(max_length=200)
    per_saving_one =   models.CharField(max_length=200)
    per_saving_three =  models.CharField(max_length=200)


    # Meta and Strings = 
    class Meta:
        """ Meta data for Exam Evaluation Criteria model"""
        verbose_name = _('SpotPrice')
        verbose_name_plural = _('SpotPrices')

    def __str__(self):
        return self.region + ' - ' + self.size
 