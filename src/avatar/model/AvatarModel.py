from .entities import *

class AvatarModel:

    @classmethod
    def obtener_avatar(cls, session, hash):
        assert hash is not None
        return session.query(Avatar).filter(hash=hash).one_or_none()
