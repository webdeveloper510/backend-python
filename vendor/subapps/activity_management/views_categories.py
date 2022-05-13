from unicodedata import category
from rest_framework import serializers, status, generics , views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Category, SubCategory
from .serializers_categories import CategorySerializer,SubCategorySerializer,UpdateWeightageSerializer


class CategoryListView(generics.ListCreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UpdateCategoryWeightageView(views.APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer = UpdateWeightageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"weightage":"Updated Successfully"})
        else :
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SubCategoriesView(views.APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,pk):
        subCategories = SubCategory.objects.filter(category__id=pk)
        return Response(SubCategorySerializer(subCategories,many=True).data)