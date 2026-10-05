import logging

from Storage.json_storage import JSONStorage
from Models.user import User


logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self)->None:
        self.storage = JSONStorage[User]("users.json")


    def get_all(self) -> list[User]:
        users = self.storage.load_all(User.from_dict)
        logger.debug("Users loaded from repository: count=%s", len(users))
        return users


    def save_all(self,users:list[User]) ->None:
          self.storage.save_all(users,User.to_dict)
          logger.info("Users saved to repository: count=%s", len(users))

    def find_by_id(self , user_id:int)->User:
         users = self.get_all()
         for user in users:
              if user_id == user.id_user:
                   logger.debug("User found by id: id=%s", user_id)
                   return user

         logger.debug("User not found by id: id=%s", user_id)
         return None
    def find_by_username(self,user_name:str)->User:
         users = self.get_all()
         for user in users:
              if user_name == user.username:
                   logger.debug("User found by username: username=%s", user_name)
                   return user

         logger.debug("User not found by username: username=%s", user_name)
         return None