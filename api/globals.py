from api.context import AppContext
from settings import Settings

settings = Settings.new()
app_context = AppContext(settings)

__all__ = [
    settings,
    app_context
]
