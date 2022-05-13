import pytest
from superadmin.subapps.media_and_groupings.models import Avatar


# pytest -s test_avatarModels.py

@pytest.mark.django_db
def test_AvatarModel():
    all_avatar = Avatar.objects.all()
    assert len(all_avatar) == 0

    boy_avatar = Avatar(
        name = 'Avatar1',
        type = 'BOY',
        status = 'ACTIVE'
    )

    boy_avatar.save()

    all_avatar = Avatar.objects.all()
    assert len(all_avatar) == 1


    girl_avatar = Avatar(
            name = 'Avatar2',
            type = 'GIRL',
            status = 'ACTIVE'
        )
    girl_avatar.save()

    all_avatar = Avatar.objects.all()
    assert len(all_avatar) == 2
    assert girl_avatar.name == all_avatar[1].name
    assert girl_avatar.type == all_avatar[1].type
    assert girl_avatar.status == all_avatar[1].status
    
    girl_avatar.name == 'Avatar23'
    girl_avatar.status == 'DEACTIVE'
    girl_avatar.save()
    avatarOfGirl = Avatar.objects.get(id=girl_avatar.id)
    assert girl_avatar.name == avatarOfGirl.name
    assert girl_avatar.status == avatarOfGirl.status
    
    girl_avatar.delete()
    
    all_avatar = Avatar.objects.all()   
    assert len(all_avatar) == 1

