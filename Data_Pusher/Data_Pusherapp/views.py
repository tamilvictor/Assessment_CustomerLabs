from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests

class AccountListCreate(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationListCreate(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_queryset(self):
        account_id = self.kwargs['account_id']
        return Destination.objects.filter(account__account_id=account_id)

class DestinationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class IncomingData(APIView):
    def post(self, request):
        app_secret_token = request.headers.get('CL-X-TOKEN')
        if not app_secret_token:
            return Response({"detail": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            account = Account.objects.get(app_secret_token=app_secret_token)
        except Account.DoesNotExist:
            return Response({"detail": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        destinations = account.destinations.all()

        for destination in destinations:
            headers = destination.headers
            if destination.http_method.lower() == 'get':
                response = requests.get(destination.url, params=data, headers=headers)
            elif destination.http_method.lower() == 'post':
                response = requests.post(destination.url, json=data, headers=headers)
            elif destination.http_method.lower() == 'put':
                response = requests.put(destination.url, json=data, headers=headers)
            else:
                continue  # Handle other methods if necessary

            if response.status_code not in range(200, 300):
                return Response({"detail": "Failed to send data to one or more destinations"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Data sent successfully"}, status=status.HTTP_200_OK)
