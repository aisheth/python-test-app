from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from clients.models import Client
from clients.serializers import ClientSerializer, \
    ClientDetailSerializer


class ClientListCreateAPIView(ListCreateAPIView):
    '''
    ListCreateAPIView helps us process POST and GET requests.

    Endpoints: 
    1. POST 
        - htpp://127.0.0.1:8000/api/clients/ 
        - This endpoint is used to add new client
    2. GET 
        - htpp://127.0.0.1:8000/api/clients/
        - This endpoint is used to retrieve list of clients
    '''
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_queryset(self):
        '''
        This is optimized queryset to avoid n+1 problem. To undestand better, 
        Try this API endpoint after commenting this function. Once this function
        is commented above queryset will be used. Observe number of database queries
        before and after commenting this function.
        But there's still a problem with following queryset which is solved in 
        project's list API. 
        '''
        queryset = Client.objects.select_related('created_by')
        return queryset


class ClientRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    '''
    ListCreateAPIView helps us process POST and GET requests.

    Endpoints: 
    1. PUT/PATCH 
        - htpp://127.0.0.1:8000/api/clients/:id/
        - This endpoint is used to update client information
    2. GET 
        - htpp://127.0.0.1:8000/api/clients/:id/
        - This endpoint is used to retrieve details of a client
    '''
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_serializer_class(self):
        '''
        Using two different serializers according to method
        '''
        if self.request.method == 'GET':
            return ClientDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = Client.objects.select_related('created_by') \
            .prefetch_related('projects')
        return queryset
