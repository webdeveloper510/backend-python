import pytest
from faker import Faker
from superadmin.subapps.media_and_groupings.models import Attribute

fake = Faker()

@pytest.mark.django_db
def test_attributemodel():
    name = fake.name()
    Attribute.objects.create(
        name = name,
        index = 1
    )
    all_attr = Attribute.objects.all()
    assert len(all_attr) == 1
    assert all_attr[0].name == name
    assert all_attr[0].status == "INACTIVE"


def test_attributeWithCreatedBy(superAdmin):
    name = fake.name()
    Attribute.objects.create(
        name = name,
        index = 1,
    )
    all_attr = Attribute.objects.all()
    assert len(all_attr) == 1
    assert all_attr[0].name == name
    assert all_attr[0].index == 1
    
