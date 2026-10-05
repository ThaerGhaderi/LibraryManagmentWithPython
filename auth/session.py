import logging

from Models.user import User
from auth.exceptions import ( NotAuthenticatedError, PermissionDeniedError)


logger = logging.getLogger(__name__)


class Session:
    def __init__(self)->None:
        self._current_user: User | None = None


    @property
    def current_user(self) -> User | None:
        return self._current_user    

    @property 
    def is_authenticated(self) -> bool:
        return self._current_user is not None



    def login(self,user:User):
     self._current_user = user
     logger.debug(
         "Session authenticated: id=%s username=%s",
         user.id_user,
         user.username,
     )




    def logout(self):
       if self._current_user is not None:
           logger.debug(
               "Session cleared: id=%s username=%s",
               self._current_user.id_user,
               self._current_user.username,
           )
       self._current_user = None



    def require_authentication(self)->User:
        if self._current_user is None:
                   logger.warning("Authentication required but no user is logged in")
                   raise NotAuthenticatedError(
                "You must be logged in to perform this operation."
            )
        return self._current_user



    def require_role(self , required_role)->User:
        user = self.require_authentication()
        if user.role != required_role:
               logger.warning(
                "Session role check failed: user_id=%s required_role=%s actual_role=%s",
                user.id_user,
                required_role,
                user.role,
               )
               raise PermissionDeniedError(
                "You do not have permission to perform this operation."
            )
        return user

    
   