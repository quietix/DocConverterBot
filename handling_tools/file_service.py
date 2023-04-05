import json
import shutil
import dotenv
import telepot
from handling_tools import data_extractor as dxtr
from PIL import Image, ImageOps
import os, glob


downloads_path = dotenv.dotenv_values('.env')['DOWNLOADS_PATH']

class File_service:

    def full_data_clean(self):
        with open(dotenv.dotenv_values('.env')['JSON_DATA_PATH'], 'r') as rd:
            data_list: list = json.load(rd)
            data_list = [data_list[len(data_list) - 1]]

        with open(dotenv.dotenv_values('.env')['JSON_DATA_PATH'], 'w') as fp:
            json.dump(data_list, fp, indent=4)


    def clean_data_file(self):
        limit = (int)(dotenv.dotenv_values('.env')['DATA_LIST_LIMIT'])
        with open(dotenv.dotenv_values('.env')['JSON_DATA_PATH'], 'r') as rd:
            data_list: list = json.load(rd)
            clear_num = (int)(len(data_list) / 2)
            if len(data_list) > limit:
                del data_list[:clear_num]

        with open(dotenv.dotenv_values('.env')['JSON_DATA_PATH'], 'w') as fp:
            json.dump(data_list, fp, indent=4)


    def record_update(self, msg):
        if os.path.exists(dotenv.dotenv_values('.env')['JSON_DATA_PATH']):
            with open(dotenv.dotenv_values('.env')['JSON_DATA_PATH'], 'r') as f:
                data_list: list = json.load(f)

            data_list.append(msg)

            with open(dotenv.dotenv_values('.env')['JSON_DATA_PATH'], 'w') as f:
                json.dump(data_list, f, indent=4)

            try:
                self.clean_data_file()
            except:
                self.full_data_clean()
        else:
            data_list: list = []

            data_list.append(msg)

            with open(dotenv.dotenv_values('.env')['JSON_DATA_PATH'], 'w') as f:
                json.dump(data_list, f, indent=4)

            try:
                self.clean_data_file()
            except:
                self.full_data_clean()


    def get_last_command(self, user_id):
        data_extractor = dxtr.Data_extractor()
        with open(dotenv.dotenv_values('.env')['JSON_DATA_PATH'], 'r') as f:
            data_list: list = json.load(f)
            for i in range(0, len(data_list)):
                content_type, chat_type, chat_id = telepot.glance(data_list[i])
                tmp_user_id = data_extractor.get_user_id_fast(data_list[i])
                if tmp_user_id == user_id:
                    if content_type == 'text':
                        if '/' in data_list[i]['text']:
                            return data_list[i]['text']
        return dotenv.dotenv_values('.env')['LAST_COMMAND_NOT_FOUND_ERROR_CODE']


    def create_photo_list_from_existing_files_in_directory(self, user_id):
        photo_list = []
        i = 1
        while 1:
            if os.path.exists(f'{downloads_path}\\{user_id}\\image{i}.jpg'):
                photo_list.append(f'{downloads_path}\\{user_id}\\image{i}.jpg')
                i += 1
            else:
                break
        return photo_list


    def download_photo(self, user_id):
        bot = telepot.Bot(dotenv.dotenv_values('.env')['TOKEN'])
        data_extractor = dxtr.Data_extractor()
        if not os.path.exists(downloads_path):
            os.mkdir(dotenv.dotenv_values('.env')['DOWNLOADS_PATH'])
        with open(dotenv.dotenv_values('.env')['JSON_DATA_PATH'], 'r') as rd:
            data_list = json.load(rd)
            data_list.reverse()
            photos_list = []
            counter = 1
            for i in range(0, len(data_list)):
                if data_extractor.get_user_id_fast(data_list[i]) == user_id:
                    content_type, chat_type, chat_id = telepot.glance(data_list[i])
                    if content_type == 'text':
                        msg_text = data_extractor.get_message_text_fast(data_list[i])
                        if msg_text == '/create_pdf' or msg_text == 'Завершити сеанс' or msg_text == 'Відмінити створення':
                            break

                    else:
                        if content_type == 'photo':
                            if not os.path.exists(f'{downloads_path}\\{user_id}'):
                                os.mkdir(f'{downloads_path}\\{user_id}')
                            array = data_list[i]['photo']
                            len1 = len(array)
                            dict1: dict = data_list[i]
                            file_id = dict1['photo'][len1 - 1]['file_id']
                            file_name = f'image{counter}.jpg'
                            file_path = f'{downloads_path}\\{user_id}\\{file_name}'
                            counter += 1
                            photos_list.append(file_path)
                            bot.download_file(file_id, file_path)

        return photos_list


    # when photo_list is ready
    def create_pdf_from_photo_list(self, user_id, photos_list: list, file_name):
        photos_count = len(photos_list)
        image_list = []

        for i in range(photos_count - 1, -1, -1):
            image = Image.open(f'{downloads_path}\\{user_id}\\image{i + 1}.jpg')
            image = ImageOps.exif_transpose(image)
            image_list.append(image)

        image_list[0].save(f'{downloads_path}\\{user_id}\\{file_name}.pdf', resolution=100.0, save_all=True,
                           append_images=image_list[1:])

        return f'{downloads_path}\\{user_id}\\{file_name}.pdf'


    def delete_directory(self, user_id):
        if os.path.exists(f'{downloads_path}\\{user_id}'):
            shutil.rmtree(f'{downloads_path}\\{user_id}\\')


    def get_last_non_command_message_text(self, user_id):
        data_extractor = dxtr.Data_extractor()
        with open(dotenv.dotenv_values('.env')['JSON_DATA_PATH'], 'r') as f:
            data_list: list = json.load(f)
            data_list.reverse()
            for i in range(0, len(data_list)):
                content_type, chat_type, chat_id = telepot.glance(data_list[i])
                tmp_user_id = data_extractor.get_user_id_fast(data_list[i])
                if tmp_user_id == user_id:
                    if content_type == 'text':
                        if data_list[i]['text'] == "/ready":
                            return data_list[i+1]['text']

        return dotenv.dotenv_values('.env')['LAST_NON_COMMAND_NOT_FOUND_ERROR_CODE']