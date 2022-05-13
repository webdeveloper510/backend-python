from abc import abstractclassmethod
import pytest
from faker import Faker
from superadmin.subapps.media_and_groupings.models import HeaderDetails

fake =Faker()
def test_createHeaderDetails(HeaderMarketing):
    texts = fake.text()
    HeaderDetails.objects.create(
        marketing = HeaderMarketing,
        # platform_type = models.CharField(choices=PLATFORM_TYPE, max_length=20, null=True, blank=True)
        page_visits = 100,
        text = texts
    )

    all_header = HeaderDetails.objects.all()
    assert len(all_header) == 1

    firstHeader = all_header.first()
    assert firstHeader.marketing == HeaderMarketing
    assert firstHeader.text ==  texts


def test_updateHeaderDetails(HeaderMarketing):
    texts = fake.text()
    HeaderDetails.objects.create(
        marketing = HeaderMarketing,
        # platform_type = models.CharField(choices=PLATFORM_TYPE, max_length=20, null=True, blank=True)
        page_visits = 100,
        text = texts
    )

    all_header = HeaderDetails.objects.all()
    assert len(all_header) == 1
    new_marketing = HeaderMarketing
    new_marketing.id = None
    new_marketing.save()
    firstHeader = all_header.first()
    new_text = fake.text()
    firstHeader.marketing = new_marketing
    firstHeader.text =  new_text
    firstHeader.save()


    first_header = HeaderDetails.objects.all().first()
    assert first_header.marketing == new_marketing
    assert first_header.text == new_text


def test_deleteHeaderDetails(HeaderMarketing):
    texts = fake.text()
    HeaderDetails.objects.create(
        marketing = HeaderMarketing,
        # platform_type = models.CharField(choices=PLATFORM_TYPE, max_length=20, null=True, blank=True)
        page_visits = 100,
        text = texts
    )

    all_header = HeaderDetails.objects.all()
    assert len(all_header) == 1

    all_header[0].delete()
    all_header = HeaderDetails.objects.all()
    assert len(all_header) == 0