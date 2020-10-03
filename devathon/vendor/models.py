from django.db import models

# Create your models here.

from django.db import models

from django.urls import reverse
from datetime import datetime
# Create your models here.
from student.models import Student


class ExtraItems(models.Model):
    item_name = models.CharField(max_length=100, primary_key=True)
    item_cost = models.CharField(max_length=10)

    def __str__(self):
        return self.item_name


class Token(models.Model):
    reg_id = models.ForeignKey(
        Student, related_name='token', null=True, blank=True, on_delete=models.CASCADE)
    item_name = models.ForeignKey(
        ExtraItems, max_length=30, on_delete=models.CASCADE)
  #  item_cost = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField(default=datetime.now, blank=True)

    def get_absolute_url(self):
        return reverse('vendor:order')

    def __str__(self):
        return self.reg_id.user.username+" "+self.item_name.item_name
    
    
    class Meta:
        ordering = ['-date']
