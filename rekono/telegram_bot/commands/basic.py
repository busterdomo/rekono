from security.otp import generate, get_expiration
from telegram import ParseMode
from telegram.ext import CallbackContext
from telegram.update import Update
from telegram_bot.messages.basic import LOGOUT, WELCOME
from telegram_bot.models import TelegramChat


def start(update: Update, context: CallbackContext) -> None:
    '''Initialize Telegram Bot chat.

    Args:
        update (Update): Telegram Bot update
        context (CallbackContext): Telegram Bot context
    '''
    if update.effective_chat and update.message:
        chat, _ = TelegramChat.objects.update_or_create(                        # Create or update the Telegram chat
            defaults={'user': None, 'otp': generate(), 'otp_expiration': get_expiration()},
            chat_id=update.effective_chat.id
        )
        # Send welcome message including OTP to link Telegram Chat with an user account
        update.message.reply_text(WELCOME.format(otp=chat.otp), parse_mode=ParseMode.MARKDOWN_V2)


def logout(update: Update, context: CallbackContext) -> None:
    '''Unlink Telegram Bot chat for an user account.

    Args:
        update (Update): Telegram Bot update
        context (CallbackContext): Telegram Bot context
    '''
    if update.effective_chat and update.message:
        chat = TelegramChat.objects.filter(chat_id=update.effective_chat.id).first()    # Get Telegram chat by Id
        if chat:
            chat.delete()                                                       # Remove Telegram chat update
        update.message.reply_text(LOGOUT, parse_mode=ParseMode.MARKDOWN_V2)     # Send goodbye message
