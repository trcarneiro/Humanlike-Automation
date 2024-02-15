import unittest
from unittest.mock import patch, MagicMock
from telegram_bot_handler import TelegramBotHandler
from telegram.ext import filters  # Importe filters para usar CHOOSING

class TestTelegramBotHandler(unittest.TestCase):

    def setUp(self):
        self.token = "dummy_token"
        self.chat_id = "dummy_chat_id"
        with patch('telegram.Bot') as self.mock_bot, \
             patch('telegram.ext.Updater') as self.mock_updater:
            self.bot_handler = TelegramBotHandler(self.token, self.chat_id)

    @patch('telegram.ext.ConversationHandler')
    @patch('telegram.ext.CommandHandler')
    @patch('telegram.ext.MessageHandler')
    @patch('telegram.ext.filters.Regex', return_value=MagicMock())  # Atualizado para filters.Regex
    @patch('telegram.Update', return_value=MagicMock())
    def test_start(self, mock_update, mock_filters, mock_message_handler, mock_command_handler, mock_conversation_handler):
        # Simular uma resposta para o comando /start
        mock_update.message.text = '/start'
        mock_context = MagicMock()
        result = self.bot_handler.start(mock_update, mock_context)

        # Verificar se o método reply_text foi chamado
        mock_update.message.reply_text.assert_called_once()
        # Verificar o valor retornado, se aplicável
        self.assertEqual(result, filters.CHOOSING)  # Atualizado para filters.CHOOSING

    # Outros testes para métodos regular_choice, received_information, done

    @patch('telegram.Bot.send_message')
    def test_send_message(self, mock_send_message):
        # Testar o envio de uma mensagem
        message = "Test message"
        self.bot_handler.send_message(message)

        # Verificar se o método send_message foi chamado com os parâmetros corretos
        mock_send_message.assert_called_with(chat_id=self.chat_id, text=message)

# Adicione mais testes conforme necessário

if __name__ == '__main__':
    unittest.main()
