from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'Topdesk x SMAX -- '
    root_path: str
    debug: bool
    log_file: str 
    conn_str: str
    topdesk_base_url: str
    topdesk_user: str
    topdesk_password: str
    smax_base_url: str
    smax_user: str
    smax_password: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitivity=False)


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')