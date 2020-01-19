from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from .serializers import QrCodeSerializer, QrStatsSerializer, QrScanSerializer
from .models import QrCode, QrStats


class QrCodeViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    queryset = QrCode.objects.all()
    serializer_class = QrCodeSerializer


class QrCodeScanViewSet(GenericViewSet):
    queryset = QrCode.objects.all()
    stats_queryset = QrStats.objects.all()
    serializer_class = QrScanSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        self.count_in(request)
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        total_scans, unique_scans = self.get_stats()

        serializer.update(
            instance,
            {
                'total_scans': total_scans,
                'unique_scans': unique_scans,
            },
        )
        return Response(serializer.data)

    def count_in(self, request):
        ip = request.META.get('HTTP_USER_AGENT')
        browser = request.META.get('REMOTE_ADDR')

        if ip:
            stats = QrStats(ip=ip, browser=browser, qr_code=self.get_object())
            stats.save()

    def get_stats(self):
        qr_scans = QrStats.objects.filter(qr_code=self.get_object()).all()
        return (
            len(qr_scans),
            len({(scan.ip, scan.browser) for scan in qr_scans}),
        )


class QeCodeStatsViewSet(GenericViewSet, RetrieveModelMixin):
    queryset = QrStats.objects.all()
    serializer_class = QrStatsSerializer
