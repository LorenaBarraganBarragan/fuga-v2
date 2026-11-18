from app.repositories.profiles import ProfilesRepository


class ProfilesService:
    @staticmethod
    def get_or_bootstrap_profile(user, db, nombres=None, apellido=None):
        return ProfilesRepository(user.user_id).ensure_profile(db, nombres, apellido)
