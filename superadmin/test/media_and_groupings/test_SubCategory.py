from os import name
import pytest
from faker import Faker
from django.db.utils import  IntegrityError
from superadmin.subapps.media_and_groupings.models import SubCategory

fake=Faker()


def test_subCategory(category):
    name = fake.name()
    subcat = SubCategory.objects.create(
        name=name,
        category=category,
        status="ACTIVE"
    )
    # subcat.save()
    allSubCat = SubCategory.objects.all()
    assert len(allSubCat) == 1
    assert subcat.status == 'ACTIVE'
    assert subcat.name == name

@pytest.mark.django_db
def test_subCategoryWithoutCategory():
    with pytest.raises(IntegrityError):
        SubCategory.objects.create(name='subCat')
    