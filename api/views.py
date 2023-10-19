from rest_framework.response import Response
from rest_framework import status, generics
from api.models import PhoneBook as PhoneBookModel
from api.serializers import PhoneBookSerializer
from datetime import datetime

class PhoneBook(generics.GenericAPIView):
    serializer_class = PhoneBookSerializer
    queryset = PhoneBookModel.objects.all()
    lookup_field = 'number'

    def get(self, request):
        entries = PhoneBookModel.objects.all()
        serializer = self.serializer_class(entries)
        return Response({
            "status_code": "1",
            "data": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PhoneBookDetail(generics.GenericAPIView):
    queryset = PhoneBookModel.objects.all()
    serializer_class = PhoneBookSerializer
    lookup_field = 'number'

    def get_phonebook_entry(self, number):
        try:
            return PhoneBookModel.objects.get(number=number)
        except:
            return None 

    def get(self, request, number):
        phonebook_entry = self.get_phonebook_entry(number=number)
        if phonebook_entry == None:
            return Response({"status_code": 0, "message": f"phone number requested for not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(phonebook_entry)
        if serializer.data["is_blacklisted"]:
            return Response({"status_code":1, "message": "blocked", "data":{"number": serializer.data["number"]}})
        else:
            return Response({"status_code":1, "message": "active", "data":{"number": serializer.data["number"]}})

    def patch(self, request, number):
        phonebook_entry = self.get_phonebook_entry(number)
        if phonebook_entry == None:
            return Response({"status_code": 0, "message": f"phone number requested for not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            phonebook_entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updated_at'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, number):
        phonebook_entry = self.get_phonebook_entry(number)
        if phonebook_entry == None:
            return Response({"status_code": 0, "message": f"phone number requested for not found"}, status=status.HTTP_404_NOT_FOUND)
        phonebook_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)