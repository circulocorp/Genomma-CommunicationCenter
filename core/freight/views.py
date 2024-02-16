from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from core.freight.serializers import FreightSerializer
from rest_framework.pagination import PageNumberPagination
from core.freight.models import Freight
from core.freight.catalog import FreightStatus
from rabbit.rabbit_configuration import RabbitMQConfiguration
from django.core.serializers.json import DjangoJSONEncoder
import json


class FreightPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 1000


class FreightApiView(APIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = FreightPagination

    def post(self, request, format=None):
        freight_data = json.loads(request.body)
        freight_serializer = FreightSerializer(data=freight_data)

        if freight_serializer.is_valid():
            freight_instance = freight_serializer.save()

            freight_serializer.data['uuid'] = str(freight_instance.uuid)
            # Send message to RabbitMQ
            print('Sending message to RabbitMQ')
            rabbitmq_config = RabbitMQConfiguration()
            rabbitmq_config.send_message(json.dumps(freight_data, cls=DjangoJSONEncoder))
            rabbitmq_config.close_connection()

            return Response(data={
                'content': freight_serializer.data,
                'message': 'Freight created successfully',
                'status': 'success',
                'code': 201
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'content': freight_serializer.errors,
                'message': 'Freight not created: {}'.format(freight_serializer.errors),
                'status': 'error',
                'code': 400
            }, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request, format=None):
        freights = Freight.objects.filter(status=FreightStatus.ACTIVE.value)

        if not freights:
            return Response(data={
                'content': [],
                'message': 'No freight(s) found',
                'status': 'success',
                'code': 200
            }, status=status.HTTP_200_OK)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(freights, request)
        serializer = FreightSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            'content': serializer.data,
            'message': '{} Freight(s) found'.format(len(serializer.data)),
            'status': 'success',
            'code': 200
        })
    
    
    def put(self, request, format=None):
        freight_data = json.loads(request.body)
        freight_instance = Freight.objects.get(freight_order=freight_data['freight_order'])
        freight_serializer = FreightSerializer(freight_instance, data=freight_data)

        if freight_serializer.is_valid():
            freight_instance = freight_serializer.save()
            return Response(data={
                'content': freight_serializer.data,
                'message': 'Freight updated successfully',
                'status': 'success',
                'code': 200
            }, status=status.HTTP_200_OK)
        else:
            return Response(data={
                'content': freight_serializer.errors,
                'message': 'Freight not updated: {}'.format(freight_serializer.errors),
                'status': 'error',
                'code': 400
            }, status=status.HTTP_400_BAD_REQUEST)