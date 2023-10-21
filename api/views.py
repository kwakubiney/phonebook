from rest_framework.response import Response
from rest_framework import status, generics
from api.models import PhoneBook as PhoneBookModel
from api.serializers import PhoneBookSerializer
from datetime import datetime
from api.permissions import IsAdminOrReadOnly, IsDeleteAllowed

class PhoneBook(generics.GenericAPIView):
    serializer_class = PhoneBookSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_phonebook_entry(self, pk):
        try:
            return PhoneBookModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request):
        entries = PhoneBookModel.objects.all()
        serializer = self.serializer_class(entries, many=True)
        return Response({
            "status": "success",
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
    permission_classes = [IsDeleteAllowed]

    def get_phonebook_entry(self, pk):
        try:
            return PhoneBookModel.objects.get(pk=pk)
        except:
            return None 

    def get(self, request, pk):
        phonebook_entry = self.get_phonebook_entry(pk=pk)
        if phonebook_entry == None:
            return Response({"status_code": 0, "message": f"phone number specified does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(phonebook_entry)
        if serializer.data["is_blacklisted"]:
            return Response({"status_code":1, "message": "blocked", "data":{"number": serializer.data["number"]}})
        else:
            return Response({"status_code":1, "message": "active", "data":{"number": serializer.data["number"]}})

    def delete(self, request, pk):
        phonebook_entry = self.get_phonebook_entry(pk)
        if phonebook_entry == None:
            return Response({"status_code": 0, "message": f"phone number specified does not exist"}, status=status.HTTP_404_NOT_FOUND)
        phonebook_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        phonebook_entry = self.get_phonebook_entry(pk)
        if phonebook_entry == None:
            return Response({"status_code": 0, "message": f"phone number specified does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            phonebook_entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)