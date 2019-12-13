from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import BankParser

bank = BankParser.BankParser()

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(self.request.query_params)

class FetchByIFSC(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
    	ifsc = self.request.query_params.get('ifsc')

    	if(ifsc is not None):
    		return Response(bank.fetchByIFSC(ifsc))
    	else:
    		return Response({'message':'Invalid Parameters'})

class FetchByName(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request,*args, **kwargs):
        name = self.request.query_params.get('name')
        city = self.request.query_params.get('city')
        limit = self.request.query_params.get('limit')
        offset = self.request.query_params.get('offset')

        if(name is not None and city is not None):
            if(limit is not None and offset is not None):
                return Response(bank.fetchByName(name,city,limit,offset))
            elif(limit is None and offset is not None):
                return Response(bank.fetchByName(name,city,offset = offset))
            elif(limit is not None and offset is None):
                return Response(bank.fetchByName(name,city,limit = limit))
            else:
                return Response(bank.fetchByName(name,city))
        else:
            return Response({'message':'Invalid Parameters'})