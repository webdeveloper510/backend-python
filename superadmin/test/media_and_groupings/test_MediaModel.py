import pytest
from faker import Faker

from superadmin.subapps.media_and_groupings.models import Media

fake = Faker()

# @pytest.mark.django_db
def test_MediaModels(superAdmin):
    name = fake.name()
    Media.objects.create(
        name = name,
        status="ACTIVE",
        type="4",
        used_for="CATEGORY_IMAGE"
    )

    all_media = Media.objects.all()

    assert len(all_media) == 1
    assert all_media[0].name == name
    assert all_media[0].type == '4'
    assert all_media[0].used_for == "CATEGORY_IMAGE"


def test_updateMedia(superAdmin):
    name = fake.name()
    Media.objects.create(
        name = name,
        status="ACTIVE",
        type="4",
        used_for="CATEGORY_IMAGE"
    )

    all_media = Media.objects.all()

    assert len(all_media) == 1
    assert all_media[0].name == name
    assert all_media[0].type == '4'
    assert all_media[0].used_for == "CATEGORY_IMAGE"

    new_name = fake.name()
    firstMedia = all_media[0]
    firstMedia.name = new_name
    firstMedia.type = '1'
    firstMedia.used_for = "CATEGORY_ICON"
    firstMedia.save()

    alln_media = Media.objects.all()
    assert alln_media[0].name == new_name
    assert alln_media[0].type == '1'
    assert alln_media[0].used_for == "CATEGORY_ICON"

@pytest.mark.django_db
def test_delete():
    name = fake.name()
    media = Media.objects.create(
        name = name,
        status="ACTIVE",
        type="4",
        used_for="CATEGORY_IMAGE"
    )

    all_media = Media.objects.all()
    assert len(all_media) == 1
    
    media.delete()
    all_media.delete()
    