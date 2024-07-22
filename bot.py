import telebot
import tomllib
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

class MistralBot:

    def __init__(self):
        with open('conf.toml', "rb") as f:
            data = tomllib.load(f)
            print(data)
        self.telegram_token = data['telegram_bot_key']
        self.mistral_api_key = data['mistral_api_key']
        self.bot = telebot.TeleBot(self.telegram_token)
        self.allowed_users = [ int(d) for d in data['allowed_users']]
        self.model = data['model']


        @self.bot.message_handler(commands=['start', 'hello'])
        def send_welcome(message):
            self.bot.reply_to(message, message.from_user.id)

        @self.bot.message_handler(func=lambda msg: True)
        def echo_all(message):
            print(message.from_user.id)
            print(self.allowed_users)
            if message.from_user.id in self.allowed_users:
                client = MistralClient(api_key=self.mistral_api_key)

                #message.text
                print(self.allowed_users)

                chat_response = client.chat(
                    model=self.model,
                    messages=[ChatMessage(role="user", content=message.text)]
                )

                print(chat_response)
                self.bot.reply_to(message, chat_response.choices[0].message.content)


    def serve(self):
        self.bot.infinity_polling()



if __name__ == "__main__":
    d = MistralBot()
    d.serve()