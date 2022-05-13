from django.core.exceptions import ValidationError
import pytest
from superadmin.subapps.media_and_groupings.models import AgeGroup

# @pytest.mark.django_db
def test_ageGroups(country):
    ageGroup = AgeGroup(
        name = "Baby Groups",
        min_age = 1,
        max_age = 3,
        status = 'INACTIVE',
        country = country
    )
    ageGroup.save()
    assert ageGroup.id == 1
    allGroup = AgeGroup.objects.all()
    firstGroup = allGroup.first()

    assert len(allGroup) ==1
    assert firstGroup.name == "Baby Groups"
    assert firstGroup.country.name == "India"

@pytest.mark.django_db
def test_ageGroupWithoutCountry():
    ageGroup = AgeGroup(
        name = "Adult",
        min_age = 18,
        max_age = 21,
        status = 'INACTIVE'
    )
    ageGroup.save()
    assert ageGroup.id == 1
    allGroup = AgeGroup.objects.all()
    firstGroup = allGroup.first()

    assert len(allGroup) ==1
    assert firstGroup.name == "Adult"
    assert firstGroup.country == None


    
# @pytest.mark.django_db
def test_ageGroupdifferentStatus(country):
    ageGroup = AgeGroup(
        name = "Adult",
        min_age = 18,
        max_age = 21,
        country=country,
        status = 'abcd'
    )
    with pytest.raises(ValidationError):
        ageGroup.save()

    # allGroup = AgeGroup.objects.all()
    
