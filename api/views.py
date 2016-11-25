from django.shortcuts import render

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.models import MailItem
from api.serializers import MailItemSerializer

import lob


# Test Key
lob.api_key = 'test_0dc8d51e0acffcb1880e0f19c79b2f5b0cc'

# Temporary message template 
template_url = 'https://github.com/lob/lob-templates/raw/master/letters/outstanding-balance/outstanding-balance.pdf'


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def mail_item_list(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        mailItem = MailItem.objects.all()
        serializer = MailItemSerializer(mailItem, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MailItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            mailItem = serializer.validated_data
            senderName = 'test' # mailItem['senderName']
            letter = lob.Letter.create(
                to_address = {
                    'name': 'name', #mailItem['recipientName'],
                    'address_line1': 'blah', # mailItem['recipientAddress'],
                    'address_city': mailItem['recipientCity'],
                    'address_state': mailItem['recipientState'],
                    'address_zip': mailItem['recipientZip'],
                    'address_country': 'US' #mailItem['recipientCountry']
                },
                from_address = {
                    'name': senderName,
                    'address_line1': mailItem['senderAddress'],
                    'address_city': mailItem['senderCity'],
                    'address_state': mailItem['senderState'],
                    'address_zip': mailItem['senderZip'],
                    'address_country': 'US' # mailItem['senderCountry']
                },
                file = template_url,
                data = {
                    'name': senderName
                },
                color = False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def mail_item_detail(request, pk):
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        mailItem = MailItem.objects.get(pk=pk)
    except MailItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MailItemSerializer(mailItem)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MailItemSerializer(mailItem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        mailItem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)