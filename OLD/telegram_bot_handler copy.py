from telegram import Update, ReplyKeyboardMarkup, Bot
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    Application,
    filters
)

import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Estados para o ConversationHandler
CHOOSING, TYPING_REPLY, ASKING_QUESTION = range(3)

class TelegramBotHandler:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.application = Application.builder().token(token).build()
        self.bot = self.application.bot
        self.setup()

    def setup(self):
        # Adiciona manipuladores de comandos e mensagens
        '''conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.regular_choice)],
                TYPING_REPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.received_information)],
            },
            fallbacks=[MessageHandler(filters.Regex('^Done$'), self.done)]
        )'''

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.regular_choice)],
                TYPING_REPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.received_information)],
                ASKING_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.thank_for_response)]  # Novo estado
            },
            fallbacks=[MessageHandler(filters.Regex('^Done$'), self.done)]
        )


        self.application.add_handler(conv_handler)
        self.application.add_error_handler(self.error)

    def start(self, update: Update, context: CallbackContext) -> int:
        reply_keyboard = [['Código', 'Sim/Não']]
        update.message.reply_text(
            "Olá! Sou o seu bot de automação. Por favor escolha uma opção:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return CHOOSING

    def regular_choice(self, update: Update, context: CallbackContext) -> int:
        text = update.message.text
        context.user_data['choice'] = text
        if text.lower() == 'código':
            update.message.reply_text('Por favor, envie o código.')
        else:
            update.message.reply_text('Por favor, responda com "Sim" ou "Não".')
        return TYPING_REPLY

    def received_information(self, update: Update, context: CallbackContext) -> int:
        user_data = context.user_data
        text = update.message.text
        category = user_data['choice']
        user_data[category] = text
        del user_data['choice']
        update.message.reply_text("Entendido!")
        return CHOOSING

    def done(self, update: Update, context: CallbackContext) -> int:
        update.message.reply_text("Até a próxima!")
        return ConversationHandler.END

    def error(self, update: Update, context: CallbackContext):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def send_message(self, message):
        self.bot.send_message(chat_id=self.chat_id, text=message)

    def ask_question(self):
        question = "Qual é a sua cor favorita?"
        self.bot.send_message(chat_id=self.chat_id, text=question)
        return ASKING_QUESTION  # Retorna o novo estado

    def thank_for_response(self, update: Update, context: CallbackContext) -> int:
        response = update.message.text
        thank_you_message = f"Obrigado pela resposta! Você disse: {response}"
        update.message.reply_text(thank_you_message)
        return ConversationHandler.END  # Retorna o estado final, encerrando a conversa
    

    def run(self):
        # Inicia o bot
        self.application.run_polling()

# Para usar a classe:
TELEGRAM_TOKEN = "5798790746:AAH68kkyPykFVhGUcMGswKxOLCXbKh3If2k"
CHAT_ID = "-726936965"

# Criar uma instância da classe e iniciar o bot
bot_handler = TelegramBotHandler(TELEGRAM_TOKEN, CHAT_ID)
bot_handler.run()

# Realizar o teste
#bot_handler.test()
