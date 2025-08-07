import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration - Replace with your actual values
BOT_TOKEN = '8287677323:AAECdUnuEtOVMhYdkJ2T2j5Tgc7vNDzR56w'  # Get this from BotFather
PRIMARY_CHANNEL_ID = '@FUNToken_OfficialChat'  # Replace with primary channel username or ID
SECONDARY_CHANNEL_ID = '@Anstoearn' # Replace with secondary channel username or ID

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages from the primary channel and forward them to the secondary channel."""
    # Check if the message is from the primary channel
   if update.effective_chat.username == PRIMARY_CHANNEL_ID.replace('@', ''):
        try:
            # Forward the message to the secondary channel
            await context.bot.forward_message(
                chat_id=SECONDARY_CHANNEL_ID,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.message_id
            )
            logger.info(f"Forwarded message {update.message.message_id} from {PRIMARY_CHANNEL_ID} to {SECONDARY_CHANNEL_ID}")
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Run the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handler for all message types from the primary channel
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_message))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()