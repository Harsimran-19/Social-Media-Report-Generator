from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8', extra='ignore')

    # GROQ
    GROQ_API_KEY: str = ''

    # DB
    MONGO_HOST: str = 'localhost'
    MONGO_PORT: int = 27017
    MONGO_USER: str = 'user'
    MONGO_PASSWORD: str = 'password'
    MONGO_DATABASE: str = 'linkiden-reports'
    LINKEDIN_USERNAME: str = 'harsimran1869@gmail.com'
    LINKEDIN_PASSWORD: str = 'u9jcjzui35'

    @property
    def MONGO_URI(self) -> str:
        # If credentials are provided, use authenticated URI
        if self.MONGO_USER and self.MONGO_PASSWORD:
            return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DATABASE}"
        # Otherwise, use unauthenticated URI
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DATABASE}"

    # PROFILES TO CRAWL
    PROFILES_TO_SCRAP: dict = {
        "KFC": {"page_name": "kfc", "city": "Salt Lake"},
        "MC": {"page_name": "mcdonalds", "city": "San Bernardino"},
        "In-N-Out Burger": {"page_name": "innout", "city": "Baldwin Park"},
        "Taco Bell": {"page_name": "tacobell", "city": "Downey"},
        "Wendy's": {"page_name": "wendys", "city": "Columbus"},
    }


settings = Settings()