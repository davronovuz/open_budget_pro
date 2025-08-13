from handlers.users.admin import admin_router
from handlers.users.echo import echo_router
from handlers.users.start import user_router
from handlers.users.vote import vote_router
from handlers.users.account import account_router
from handlers.users.invite import invite_router
from handlers.users.withdraw import withdraw_router

routers_list = [
    admin_router,
    user_router,
    vote_router,
    account_router,
    invite_router,
    withdraw_router,
    echo_router,
]

__all__ = ["routers_list"]
