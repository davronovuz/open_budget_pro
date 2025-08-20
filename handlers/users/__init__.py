
from handlers.users.start import user_router
from handlers.users.check_subscribe import subscribe_router
from handlers.users.menu_buttons import menu_router
from handlers.users.referal_user import referral_router
from handlers.users.payment_user import withdraw_router
from handlers.users.withdraw_updates import poll_withdraw_updates


routers_list = [
    subscribe_router,
    user_router,
    menu_router,
    referral_router,
    withdraw_router,
    poll_withdraw_updates


]

__all__ = ["routers_list"]


