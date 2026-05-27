from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DataSource, EmissionRecord
from .serializers import DataSourceSerializer, EmissionRecordSerializer
from django.utils import timezone
import csv
import io

from django.shortcuts import render
def index(request):
    return render(request,'index.html')

class DataSourceViewSet(viewsets.ModelViewSet):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer

    @action(detail=False, methods=['post'])
    def upload(self, request):
        file = request.FILES.get('file')
        source_type = request.data.get('source_type')
        name = request.data.get('name')

        if not file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        source = DataSource.objects.create(
            name=name,
            source_type=source_type,
            uploaded_by=request.data.get('uploaded_by', 'analyst')
        )

        decoded_file = file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded_file))
        records_created = 0

        for row in reader:
            EmissionRecord.objects.create(
                source=source,
                category=row.get('category', 'Unknown'),
                quantity=float(row.get('quantity', 0) or 0),
                unit=row.get('unit', 'unknown'),
                raw_data=dict(row),
                status='PENDING'
            )
            records_created += 1

        return Response({
            'message': f'Successfully uploaded {records_created} records',
            'source_id': source.id
        })

class EmissionRecordViewSet(viewsets.ModelViewSet):
    queryset = EmissionRecord.objects.all()
    serializer_class = EmissionRecordSerializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        record = self.get_object()
        record.status = 'APPROVED'
        record.reviewed_at = timezone.now()
        record.reviewed_by = request.data.get('reviewed_by', 'analyst')
        record.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        record = self.get_object()
        record.status = 'REJECTED'
        record.reviewed_at = timezone.now()
        record.reviewed_by = request.data.get('reviewed_by', 'analyst')
        record.save()
        return Response({'status': 'rejected'})