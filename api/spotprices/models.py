from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.contrib.postgres.fields import JSONField

 
class SpotPrices(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.CharField(max_length=200)

    region =  models.CharField(max_length=100)
    time =  models.CharField(max_length=200)

    api_price =  models.FloatField(default=float('-inf'))
    cli_price =  models.FloatField(default=float('-inf'))

    pay_as_you_go_price = models.FloatField(default=float('-inf'))
    one_year_reserved_price = models.FloatField(default=float('-inf'))
    three_year_reserved_price = models.FloatField(default=float('-inf'))

    per_saving_paygo = models.FloatField(default=float('-inf'))
    per_saving_one = models.FloatField(default=float('-inf'))
    per_saving_three = models.FloatField(default=float('-inf'))

    # Meta and Strings
    class Meta:
        """ Meta data for Exam Evaluation Criteria model"""
        verbose_name = _('SpotPrice')
        verbose_name_plural = _('SpotPrices')

    def __str__(self):
        return self.region + ' - ' + self.size
 