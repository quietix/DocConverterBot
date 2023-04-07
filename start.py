import os
import shutil
import time
import telepot
from telepot.loop import MessageLoop
from handling_tools import response as res
from handling_tools import file_service as fl
from handling_tools import interaction_handler as ih
from handling_tools import data_extractor as dxtr
import dotenv
#asssasadsasdad
dotenv.load_dotenv()
bot = telepot.Bot(dotenv.dotenv_values('.env')['TOKEN'])

response = res.Response()
file_service = fl.File_service()
interaction_handler = ih.Interaction_handler()
data_extractor = dxtr.Data_extractor()

def handle(msg):
    file_service.record_update(msg)
    interaction_handler.handle_interaction(msg)


MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)