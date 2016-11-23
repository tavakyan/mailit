from django.shortcuts import render

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.models import MailItem
from api.serializers import MailItemSerializer

import lob

# Test Key
lob.api_key = 'test_0dc8d51e0acffcb1880e0f19c79b2f5b0cc'


html_file = """
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css">
<title>Lob.com Sample Letter</title>
<style>
  *, *:before, *:after {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
  }

  body {
    width: 8.5in;
    height: 11in;
    margin: 0;
    padding: 0;
  }

  .page {
    page-break-after: always;
  }

  .page-content {
    position: relative;
    width: 8.125in;
    height: 10.625in;
    left: 0.1875in;
    top: 0.1875in;
    background-color: rgba(0,0,0,0.2);
  }

  .text {
    position: relative;
    left: 20px;
    top: 20px;
    width: 6in;
    font-family: 'Open Sans';
    font-size: 30px;
  }

  #return-address-window {
    position: absolute;
    left: .625in;
    top: .5in;
    width: 3.25in;
    height: .875in;
    background-color: rgba(255,0,0,0.5);
  }

  #return-address-text {
    position: absolute;
    left: .07in;
    top: .34in;
    width: 2.05in;
    height: .44in;
    background-color: white;
    font-size: .11in;
  }

  #return-logo {
    position: absolute;
    left: .07in;
    top: .02in;
    width: 2.05in;
    height: .3in;
    background-color: white;
  }

  #recipient-address-window {
    position: absolute;
    left: .625in;
    top: 1.75in;
    width: 4in;
    height: 1in;
    background-color: rgba(255,0,0,0.5);
  }

  #recipient-address-text {
    position: absolute;
    left: .07in;
    top: .05in;
    width: 2.92in;
    height: .9in;
    background-color: white;
  }

</style>
</head>

<body>
  <div class="page">
    <div class="page-content">
      <div class="text" style="top: 3in">
        The grey box is the safe area. Do not put text outside this box. If you are using the data argument, you can add variables like this: {{variable_name}}.
      </div>
    </div>
    <div id="return-address-window">
      <div id="return-logo">
        Room for company logo.
      </div>
      <div id="return-address-text">
        The Return Address will be printed here. The red area will be visible through the envelope window.
      </div>
    </div>
    <div id="recipient-address-window">
      <div id="recipient-address-text">
        The Recipient's Address will be printed here. The red area will be visible through the envelope window.
      </div>
    </div>
  </div>
  <div class="page">
    <div class="page-content">
      <div class="text">
        This is a second page.
      </div>
    </div>
  </div>
</body>

</html>
"""


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

            letter = lob.Letter.create(
                to_address = {
                    'name': 'Harry Zhang',
                    'address_line1': '123 Test Street',
                    'address_city': 'Mountain View',
                    'address_state': 'CA',
                    'address_zip': '94041',
                    'address_country': 'US'
                },
                from_address = {
                    'name': 'Ami Wang',
                    'address_line1': '123 Test Avenue',
                    'address_city': 'Mountain View',
                    'address_state': 'CA',
                    'address_zip': '94041',
                    'address_country': 'US'
                },
                file = html_file,
                data = {
                    'name': 'Harry'
                },
                color = False)
            print(letter)
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