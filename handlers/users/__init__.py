
from handlers.users.start import user_router
from handlers.users.check_subscribe import subscribe_router
from handlers.users.menu_buttons import menu_router
from handlers.users.referal_user import referral_router


routers_list = [
    subscribe_router,
    user_router,
    menu_router,
    referral_router


]

__all__ = ["routers_list"]
