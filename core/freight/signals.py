from django.db.models.signals import post_save
from django.dispatch import receiver
from core.freight.models import Freight, FreightTransaction


@receiver(post_save, sender=Freight)
def create_freight_transaction(sender, instance, created, **kwargs):
    if created:
        FreightTransaction.objects.create(freight=instance)