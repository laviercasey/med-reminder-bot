import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/bot_{datetime.now().strftime('%Y-%m-%d')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("med_reminder_bot")

def log_info(message: str) -> None:
    logger.info(message)

def log_error(message: str, exc_info=None) -> None:
    logger.error(message, exc_info=exc_info)

def log_warning(message: str) -> None:
    logger.warning(message)

def log_user_action(user_id: int, action: str, details: str = None) -> None:
    message = f"User {user_id}: {action}"
    if details:
        message += f" - {details}"
    log_info(message)

def log_payment(user_id: int, amount: float, plan: str, status: str) -> None:
    log_info(f"Payment: User {user_id} - {plan} plan ({amount}) - Status: {status}")

def log_admin_action(admin_id: int, action: str, target_user_id: int = None) -> None:
    message = f"ADMIN {admin_id}: {action}"
    if target_user_id:
        message += f" - Target user: {target_user_id}"
    log_info(message)
