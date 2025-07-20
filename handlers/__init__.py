from aiogram import Router
from . import start, pills, reminders, checklist, settings, ads, admin

def setup_routers() -> Router:
    """Setup all handlers"""
    router = Router()
    
    # Include all routers
    router.include_router(start.router)
    router.include_router(pills.router)
    router.include_router(reminders.router)
    router.include_router(checklist.router)
    router.include_router(settings.router)
    router.include_router(ads.router)
    router.include_router(admin.router)
    
    return router
