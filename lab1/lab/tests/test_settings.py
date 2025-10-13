from lab1.lab.src.settings import Settings


def test_check_settings_loaded_correctly():
    settings = Settings()
    assert settings.APP_NAME == "model"
    assert settings.ENVIRONMENT == "test"
    # assert settings.SECRET == "kochac_morgula"
