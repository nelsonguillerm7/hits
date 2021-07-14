from .utils import check_big_boss, check_managers


class CheckRol:
    """Service validate type the rol their user"""

    @classmethod
    def rol(cls, user):
        """Return str type the rol"""
        if check_big_boss(user):
            return "The Big Boss"
        elif check_managers(user):
            return "Managers"
        else:
            return "Hitman"
