class Settings:
    SECRET_KEY: str = '0ab19daf0b6470bf2226b17e4fa39569ab5f20b7d7f0587bd5d598dea8b30489'
    TOKEN_EXP_MIN = 10
    COOKIE_NAME = "access_token"


settings = Settings()