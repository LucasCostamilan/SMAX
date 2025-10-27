
from app.config import settings
from app.logger import logger

from pydantic import BaseModel

class AuthModel(BaseModel):
    username: str
    password: str

    def validate_credentials(self) -> bool:
        """
        Validate the provided username and password against stored credentials.
        """
        valid_username = settings.smax_user
        valid_password = settings.smax_password

        if self.username == valid_username and self.password == valid_password:
            logger.info("Authentication successful.")
            return True
        else:
            logger.warning("Authentication failed.")
            return False