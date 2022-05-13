import pytest
from faker import Faker
from superadmin.subapps.media_and_groupings.models import Category


fake = Faker()


@pytest.mark.django_db
def test_categoryWithPureData():
    category = Category(
        name = fake.name(),
        index = 1,

    )
    category.save()
    assert category.id == 1
    first_category = Category.objects.all().first()
    assert first_category.name == category.name
    assert first_category.index == 1


def test_updateFunctionality(category):
    category.status = 'INACTIVE'
    category.is_being_used = True
    category.save()

    first_category = Category.objects.all().first()
    assert first_category.name == category.name
    assert first_category.index == 1
    assert first_category.status == 'INACTIVE' 

@pytest.mark.django_db
def test_orderAccordingName():
    category1 = Category(
        name = 'ASDFG',
        index = 1,
    )
    category2 = Category(
        name = 'BABY',
        index = 1,
    )
    category1.save()
    category2.save()
    all_category = Category.objects.all()
    assert all_category[0] == category1
    assert all_category[1] == category2

