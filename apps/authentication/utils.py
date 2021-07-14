def check_big_boss(user):
    check = True if user.pk == 1 else False
    return check


def check_managers(user):
    from apps.authentication.models import User

    hitman_in_charge = User.objects.filter(managers=user)
    check = hitman_in_charge.exists()
    return check
