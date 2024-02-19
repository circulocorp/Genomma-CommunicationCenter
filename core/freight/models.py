from django.db import models
import uuid
from django.utils.translation import gettext as _
from core.freight.catalog import FreightStatus


FREIGHT_STATUS = (
    ('Activo', _('Activo')),
    ('Cancelado', _('Cancelado'))
)

PROCESS_STATUS = (
    (0, _('Pendiente de procesar')),
    (1, _('Procesado')),
    (2, _('Procesado correctamente')),
    (3, _('Procesado con errores')),
    (4, _('En error'))
)

class Freight(models.Model):
    uuid = models.UUIDField(_('Uuid'),primary_key=True, editable=False, default=uuid.uuid4, unique=True, blank=False, null=False)
    freight_order = models.CharField(_('Freight order'), max_length=50, blank=False, null=False, unique=True)
    status = models.CharField(_('Status'), max_length=50, choices=FREIGHT_STATUS, default=FreightStatus.ACTIVE, blank=False, null=False)
    planned_km = models.FloatField(_('Planned km'), blank=False, null=False)
    planned_time = models.BigIntegerField(_('Planned time'), blank=False, null=False)
    vehicle_resource = models.CharField(_('Vehicle resource'), max_length=50, blank=False, null=False)
    plate_number = models.CharField(_('Plate number'), max_length=50, blank=False, null=False)
    carrier = models.CharField(_('Carrier'), max_length=50, blank=False, null=False)
    driver = models.CharField(_('Driver'), max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Freight')
        verbose_name_plural = _('Freights')
        db_table = 'freight'
        ordering = ['-created_at']

    def __str__(self):
        return self.freight_order
    
    def get_status(self):
        return self.status
    
    def get_planned_km(self):
        return self.planned_km
    
    def get_planned_time(self):
        return self.planned_time
    
    def get_vehicle_resource(self):
        return self.vehicle_resource
    
    def get_plate_number(self):
        return self.plate_number
    
    def get_carrier(self):
        return self.carrier
    
    def get_driver(self):   
        return self.driver
    

class Stage(models.Model):
    uuid = models.UUIDField(_('Uuid'),primary_key=True, editable=False, default=uuid.uuid4, unique=True, blank=False, null=False)
    freight = models.ForeignKey(Freight, on_delete=models.CASCADE, related_name='stages')
    stage_id = models.CharField(_('Stage id'), max_length=50, blank=False, null=False)
    origen = models.CharField(_('Origin'), max_length=50, blank=False, null=False)
    destino = models.CharField(_('Destination'), max_length=50, blank=False, null=False)
    plate_number = models.CharField(_('Plate number'), max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Stage')
        verbose_name_plural = _('Stages')
        db_table = 'stage'
        ordering = ['created_at']

    def __str__(self):
        return self.stage_id
    
    def get_origin(self):
        return self.origin
    
    def get_destination(self):
        return self.destination
    
    def get_plate_number(self):
        return self.plate_number
    
    def get_freight(self):
        return self.freight.freight_order
    

class Event(models.Model):
    uuid = models.UUIDField(_('Uuid'),primary_key=True, editable=False, default=uuid.uuid4, unique=True, blank=False, null=False)
    freight = models.ForeignKey(Freight, on_delete=models.CASCADE, related_name='events')
    evento = models.CharField(_('Event'), max_length=50, blank=False, null=False)
    location = models.CharField(_('Location'), max_length=50, blank=False, null=False)
    sequence = models.CharField(_('Sequence'), max_length=10, blank=False, null=False)
    planned_date = models.CharField(_('Planned date'), max_length=150, blank=False, null=False)
    planned_hour = models.CharField(_('Planned hour'), max_length=150, blank=False, null=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        db_table = 'event'
        ordering = ['created_at']

    def __str__(self):
        return self.event
    
    def get_location(self):
        return self.location
    
    def get_sequence(self):
        return self.sequence
    
    def get_planned_date(self):
        return self.planned_date
    
    def get_planned_hour(self):
        return self.planned_hour
    
class FreightTransaction(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, blank=False, null=False)
    freight = models.ForeignKey(Freight, on_delete=models.CASCADE, related_name='transactions')
    process_status = models.IntegerField(_('Process status'), choices=PROCESS_STATUS, default=0, blank=False, null=False)
    mzone_code = models.CharField(_('Mzone code'), max_length=50, blank=True, null=True)
    mzone_message = models.CharField(_('Mzone message'), max_length=150, blank=True, null=True)
    broker_message = models.CharField(_('Broker message'), max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Freight transaction')
        verbose_name_plural = _('Freight transactions')
        db_table = 'freight_transaction'
        ordering = ['created_at']

    def __str__(self):
        return self.mzone_code
    
    def get_process_status(self):
        return self.process_status
    
    def get_mzone_code(self):
        return self.mzone_code
    
    def get_mzone_message(self):
        return self.mzone_message
    
    def get_broker_message(self):
        return self.broker_message