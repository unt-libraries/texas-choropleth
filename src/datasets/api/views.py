from rest_framework.generics import RetrieveAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .serializers import DatasetSerializer
from core.api.permissions import IsOwnerOrSafeMethods
from datasets.models import Dataset


class DatasetAPIView(RetrieveAPIView):
    model = Dataset
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.prefetch_related('records__cartogram_entity')
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsOwnerOrSafeMethods,)
