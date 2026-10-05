from enum import Enum

from Models.book import Book

class UserRole(Enum):
  MEMBER = "member"
  LIBRARIAN = "librarian"
class User:
    user_id = 0
    def __init__(self,
        full_name: str,
        username: str,
        password_hash: str,
        salt: str,
        role: UserRole = UserRole.MEMBER,
        active: bool = True,
        id_user: int | None = None,
)->None:
        full_name = full_name.strip()
        username = username.lower().strip()
        if not full_name:
            raise ValueError("Full name cannot be empty.")

        if not username:
            raise ValueError("Username cannot be empty.")

        if not password_hash:
            raise ValueError("Password hash cannot be empty.")

        if not salt:
            raise ValueError("Salt cannot be empty.")
        if isinstance(role, str):
            try:
             role = UserRole(role)
            except ValueError:
             raise ValueError(f"Invalid user role: {role}")


       
        if not isinstance(role, UserRole):
            raise TypeError("role must be a UserRole.")     


        if not isinstance(active, bool):
            raise TypeError("active must be a bool.")

        
   
        self._full_name = full_name
        self._username = username
        self._password_hash = password_hash
        self._salt = salt
        self._role = role
        self._active = active


        if id_user is None:
         User.user_id = User.user_id +1
         self._id_user = User.user_id
        else:
           self._id_user = id_user
           if id_user>User.user_id:
            User.user_id = id_user


    
    @property
    def id_user(self) -> int:
        return self._id_user

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def username(self) -> str:
        return self._username

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def salt(self) -> str:
        return self._salt

    @property
    def role(self) -> UserRole:
        return self._role
  
    @property
    def active(self) -> bool:
        return self._active

    def activate(self) -> None:
        self._active = True

    def deactivate(self) -> None:
        self._active = False
  
  
  
    def to_dict(self) -> dict:
       return{
       "id_user": self._id_user,
       "full_name": self._full_name,    
       "username": self._username,
       "password_hash": self._password_hash,
       "salt": self._salt,
       "role": self._role.value,
       "active": self._active,
  
       }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
     id_user = data.get("id_user")
     full_name = data.get("full_name")
     username = data.get("username")
     password_hash = data.get("password_hash")
     salt = data.get("salt")
     role = data.get("role")
     active = data.get("active", True)

     if role is None:
        raise ValueError("Role is missing in the data.")

     try:
        role = UserRole(role)
     except ValueError:
        raise ValueError(
            f"Invalid user role: {role}"
        )

     return cls(
        full_name=full_name,
        username=username,
        password_hash=password_hash,
        salt=salt,
        role=role,
        active=active,
        id_user=id_user,
     )

    def update_password(
            self,
            password_hash: str,
            salt: str,
        ) -> None:
            if not password_hash:
                raise ValueError("Password hash cannot be empty.")

            if not salt:
                raise ValueError("Salt cannot be empty.")

            self._password_hash = password_hash
            self._salt = salt


    def update_full_name(self,full_name: str)->None:
        full_name = full_name.strip()
        if not full_name: 
                    raise ValueError("Full name cannot be empty.")
        self._full_name = full_name 

    def __str__(self) -> str:
        status = "Active" if self._active else "Inactive"

        return (
            f"User #{self._id_user} | "
            f"{self._full_name} | "
            f"@{self._username} | "
            f"{self._role.value} | "
            f"{status}"
        )