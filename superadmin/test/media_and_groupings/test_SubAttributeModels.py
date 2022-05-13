import pytest
from faker import Faker
from django.db.utils import IntegrityError
from django.db.transaction import atomic

from superadmin.subapps.media_and_groupings.models import SubAttribute

fake = Faker()

def test_subAttributeModel(attribute):
    name = fake.name()
    SubAttribute.objects.create(
        name= name,
        attribute=attribute
    )
    subAttrs = SubAttribute.objects.all()

    assert len(subAttrs) == 1
    assert subAttrs[0].name == name
    assert subAttrs[0].status == 'INACTIVE'

@pytest.mark.django_db
def test_creatingSubCatWithoutAttribute():
    name = fake.name()
    with pytest.raises(IntegrityError):
        SubAttribute.objects.create(
            name= name
        )

