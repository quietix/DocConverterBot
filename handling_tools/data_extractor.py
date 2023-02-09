import dotenv
import telepot
import os


#TODO exception class, replace error codes in .env with exception class
class Data_extractor:

    def get_user_id_safe(self, msg):
        return_value = "initial_value"
        try:
            return_value = msg['from']['id']
        except:
            return_value = dotenv.dotenv_values('.env')['USER_ID_NOT_FOUND_ERROR_CODE']

        return return_value


    def get_user_id_fast(self, msg):
        return msg['from']['id']


    def get_message_text_safe(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
            return msg['text']
        return dotenv.dotenv_values('.env')['MESSAGE_TEXT_NOT_FOUND_ERROR_CODE']


    def get_message_text_fast(self, msg):
        return msg['text']


    def get_message_id_fast(self, msg):
        return msg['from']['id']

