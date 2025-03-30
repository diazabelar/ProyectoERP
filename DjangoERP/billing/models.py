from django.db import models
from core.models import Company

class Customer(models.Model):
    name = models.CharField(max_length=100)
    vat_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('company', 'vat_id')