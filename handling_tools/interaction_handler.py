import os.path
import telepot
from handling_tools import response as res
from handling_tools import file_service as fl
from handling_tools import data_extractor as dxtr
import dotenv
import time


response = res.Response()
file_service = fl.File_service()
data_extractor = dxtr.Data_extractor()
bot = telepot.Bot(dotenv.dotenv_values('.env')['TOKEN'])

class Interaction_handler:

    def gentle_get_user_id(self, msg, chat_id):
        user_id = data_extractor.get_user_id_safe(msg)
        if user_id == dotenv.dotenv_values('.env')['USER_ID_NOT_FOUND_ERROR_CODE']:
            tmp_answer = dotenv.dotenv_values('.env')['USER_ID_NOT_FOUND_ERROR_CODE']
            response.send_message(chat_id, f'Oops, some error has occured. Please, contact {tmp_answer}.')
            return
        return user_id


    def handle_interaction(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        user_id = self.gentle_get_user_id(msg, chat_id)
        if content_type == 'text':
            msg_text = data_extractor.get_message_text_safe(msg)
            if msg_text == dotenv.dotenv_values('.env')['CLEANUP_COMMAND']:
                response.send_message(chat_id, "DATA WAS CLEANED UP")
                return

            elif msg_text == '/start':
                response.send_message(chat_id, "Хайль")

            elif msg_text == '/help':
                response.send_message(chat_id, "Допомога")

            elif msg_text == '/create_pdf':
                response.response_with_reply_keyboard_when_waiting_photos(chat_id)

            elif msg_text == "Створити pdf":
                photo_list = file_service.download_photo_and_create_photo_list(user_id)
                if len(photo_list) <= 0:
                    response.response_with_reply_keyboard_when_waiting_photos_state_2(chat_id)
                else:
                    response.response_with_reply_keyboard_when_received_photos(chat_id)

            elif msg_text == "Відмінити створення pdf":
                response.delete_reply_keyboard(chat_id, 'Сеанс створення pdf завершено.')
                file_service.delete_directory(user_id)

            elif msg_text == "Автоматична назва":
                response.send_message(chat_id, 'Створюється pdf...')
                photo_list = file_service.create_photo_list_from_existing_files_in_directory(user_id)
                auto_file_name: str = (str)(user_id) + '-' + (str)(time.strftime("%Y%m%d-%H%M%S"))
                pdf_path = file_service.create_pdf_from_photo_list(user_id, photo_list, auto_file_name)
                zip_path, zipObj = file_service.push_into_zip(pdf_path, user_id)

                response.send_document(chat_id, f'{auto_file_name}.pdf', zipObj)
                zipObj.close()

                file_service.delete_directory(user_id)
                response.response_with_reply_keyboard_when_pdf_is_sent(chat_id)

            elif msg_text == "Продовжити створення":
                response.response_with_reply_keyboard_when_session_was_continued(chat_id)

            elif msg_text == "Завершити сеанс":
                response.delete_reply_keyboard(chat_id, "Сеанс створення pdf завершено.")

            elif msg_text == "Моя назва":
                response.delete_reply_keyboard(chat_id, "Введіть назву pdf. Коли буде кінцевий варіант, натисніть /ready")

            elif msg_text == "/ready":
                response.send_message(chat_id, 'Створюється pdf...')
                photo_list = file_service.create_photo_list_from_existing_files_in_directory(user_id)
                file_name = file_service.get_last_non_command_message_text(user_id)
                pdf_path = file_service.create_pdf_from_photo_list(user_id, photo_list, file_name)
                zip_path, zipObj = file_service.push_into_zip(pdf_path, user_id)

                response.send_document(chat_id, f'{file_name}.pdf', zipObj)
                zipObj.close()

                file_service.delete_directory(user_id)
                response.response_with_reply_keyboard_when_pdf_is_sent(chat_id)





