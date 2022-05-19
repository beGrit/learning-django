from chat.models import OfficialAccount
from medical.models import Doctor


def get_avatar(user_id):
    avatar_path = '/media/avatar01.jpeg'
    # Check doctor table.
    doctor = Doctor.objects.filter(related_user_id=user_id).first()
    if doctor is not None:
        avatar_path = doctor.profile_picture.url
    # Check official account.
    official_account = OfficialAccount.objects.filter(related_user_id=user_id).first()
    if official_account is not None:
        avatar_path = official_account.profile_picture.url
    return avatar_path
