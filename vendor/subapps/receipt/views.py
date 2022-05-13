from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from common.CustomLimitOffsetPaginator import CustomLimitOffsetPaginator

from .models import Receipt
from .serializer import ReceptSerializer

#PDF Genration
from django.template.loader import get_template
from io import BytesIO
import pdfkit

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    return pdfkit.from_string(html,False)


class ReceptsViews(APIView):
    permission_class = [permissions.IsAuthenticated]

    def get(self, request):
        all_recepts = Receipt.objects.all()
        paginator = CustomLimitOffsetPaginator()

        page = paginator.paginate_queryset(all_recepts, request, view=self)
        serializer = serializer = ReceptSerializer(page, many=True)
        if page is not None:
            return paginator.get_paginated_response(serializer.data)

        return Response(serializer.data)

def receipt(request):
    pdf = render_to_pdf('receipts/receipt.html', {"firstName":"zaakir"})
    return HttpResponse(pdf, content_type='application/pdf')
