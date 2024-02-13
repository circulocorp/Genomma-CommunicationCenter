from rest_framework import serializers
from core.freight.models import Stage, Event, Freight, FreightTransaction

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['stage_id', 'origen', 'destino', 'plate_number']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['evento', 'location', 'sequence', 'planned_date', 'planned_hour']

class FreightTransactionSerializer(serializers.ModelSerializer):
    process_status_display = serializers.CharField(source='get_process_status_display', read_only=True)

    class Meta:
        model = FreightTransaction
        fields = ('__all__')


class FreightSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True)
    events = EventSerializer(many=True)
    transactions = FreightTransactionSerializer(many=True, required=False)

    class Meta:
        model = Freight
        fields = ['uuid', 'transaction_id', 'freight_order', 'status', 'planned_km', 'planned_time', 'vehicle_resource', 'plate_number', 'carrier', 'driver', 'stages', 'events', 'transactions']

    def create(self, validated_data):
        stages_data = validated_data.pop('stages')
        events_data = validated_data.pop('events')

        freight = Freight.objects.create(**validated_data)

        for stage_data in stages_data:
            Stage.objects.create(freight=freight, **stage_data)

        for event_data in events_data:
            Event.objects.create(freight=freight, **event_data)

        return freight
    
    def update(self, instance, validated_data):
        stages_data = validated_data.pop('stages')
        events_data = validated_data.pop('events')

        instance.transaction_id = validated_data.get('transaction_id', instance.transaction_id)
        instance.freight_order = validated_data.get('freight_order', instance.freight_order)
        instance.status = validated_data.get('status', instance.status)
        instance.planned_km = validated_data.get('planned_km', instance.planned_km)
        instance.planned_time = validated_data.get('planned_time', instance.planned_time)
        instance.vehicle_resource = validated_data.get('vehicle_resource', instance.vehicle_resource)
        instance.plate_number = validated_data.get('plate_number', instance.plate_number)
        instance.carrier = validated_data.get('carrier', instance.carrier)
        instance.driver = validated_data.get('driver', instance.driver)
        instance.save()

        for stage_data in stages_data:
            stage = instance.stages.get(stage_id=stage_data['stage_id'])
            stage.origen = stage_data.get('origen', stage.origen)
            stage.destino = stage_data.get('destino', stage.destino)
            stage.plate_number = stage_data.get('plate_number', stage.plate_number)
            stage.save()

        for event_data in events_data:
            event = instance.events.get(evento=event_data['evento'])
            event.location = event_data.get('location', event.location)
            event.sequence = event_data.get('sequence', event.sequence)
            event.planned_date = event_data.get('planned_date', event.planned_date)
            event.save()

        return instance