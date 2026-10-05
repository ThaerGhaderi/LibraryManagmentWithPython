import hashlib
import logging
import os
import hmac

from auth.exceptions import WeakPasswordError

import config.config as config


logger = logging.getLogger(__name__)


class PasswordHasher:
    HASH_NAME = "sha256"
    ITERATIONS = 600_000
    SALT_LENGTH = 16
    KEY_LENGTH = 32


    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128


    @classmethod
    def  validate_password(cls , password : str)->None:
        if not isinstance(password,str):
            logger.warning("Password validation failed: value is not a string")
            raise TypeError("Password must be a string.")

        if not (
            config.PASSWORD_MIN_LENGTH
            <= len(password)
            <= config.PASSWORD_MAX_LENGTH
        ):
             logger.warning("Password validation failed: invalid length")
             raise WeakPasswordError("Password must be between 8 and 128 characters.")

    @classmethod
    def hash_password(cls,password:str)->tuple[str,str]:
       cls.validate_password(password)
       salt = os.urandom(cls.SALT_LENGTH)
       
       password_hash = hashlib.pbkdf2_hmac(
            cls.HASH_NAME,
            password.encode("utf-8"),
            salt,
            cls.ITERATIONS,
            dklen=cls.KEY_LENGTH,
       )
       return (
            password_hash.hex(),
            salt.hex(),
        )



    @classmethod
    def verify_password(cls, password:str , stored_hash : str , stored_salt : str)->bool:
        cls.validate_password(password)
        try:
            salt = bytes.fromhex(stored_salt)
            expected_hash = bytes.fromhex(stored_hash)
        except ValueError:
            logger.warning("Password verification failed: invalid stored credentials format")
            return False

        password_hash = hashlib.pbkdf2_hmac(
            cls.HASH_NAME,
            password.encode("utf-8"),
            salt,
            cls.ITERATIONS,
            dklen=cls.KEY_LENGTH,
        )

        is_valid = hmac.compare_digest(password_hash, expected_hash)
        logger.debug("Password verification completed: valid=%s", is_valid)
        return is_valid
