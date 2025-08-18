
from handlers.users.start import user_router
from handlers.users.check_subscribe import subscribe_router
from menu_buttons import menu_router


routers_list = [
    subscribe_router,
    user_router,
    menu_router


]

__all__ = ["routers_list"]
