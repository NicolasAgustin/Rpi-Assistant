from multiprocessing.sharedctypes import Value
import traceback
import requests
import json
import time
from threading import Thread
from threading import Lock
from datetime import datetime
from typing import List
from utils import Firebase

class Assistant:

    def __init__(self):
        self.db = Firebase()
        self.reminders = []
        self.lock = Lock()

    def show_reminders(self):
        reminders = self.db.get_childs_from('/reminders/')
        if reminders == []:
            return ""
        result = ""
        for r in reminders:
            result = f"{result}[{r[1]['description']}]{r[1]['time']}\n"
        return result

    def notify_reminders(self, reminders: List):
        new_list = reminders.copy()
        self.db.push_list_to(new_list, '/operations/notify/')

    def get_reminders(self):
        return self.reminders

    def parse_command(self, cmd: str):
        pass 

    def has_reminders_to_notify(self) -> bool:
        return bool(self.reminders) 

    def get_news(self):
        url="http://api.mediastack.com/v1/news?access_key=fd1e83f25850b31aa2ff72be75f5252d&languages=es"
        response = requests.get(url)
        
        news = json.loads(response.text)

        result = ''

        for new in news['data']:
            result = f"{result}[{new['title']}]{new['description']}\n"

        return result

    def handler_reminder(self, date, description: str, id):
        try:
            now = datetime.now()
            alarm_time = datetime.combine(now.date(), date)
            seconds = (alarm_time - now).total_seconds()
            time_info = f"{alarm_time.hour}:{alarm_time.minute}"
            if seconds > 0:
                time.sleep(seconds)
            self.lock.acquire()
            self.reminders.append(f"{description}|{time_info}")
            self.lock.release()
        except Exception:
            print(traceback.format_exc())
        finally:
            self.db.delete_by_id(id)
            print("Termino el reminder")


    def set_reminder(self, args) -> Thread:
        r_description = args[0]
        r_time = ' '.join(args[1:])
        try:
            date = datetime.strptime(r_time, '%d/%m/%Y %H:%M').time()

            id = self.db.create_reminder({
                    'description': r_description, 
                    'time': r_time
                    })

            t = Thread(target=self.handler_reminder, args=(date, r_description, id))
            t.start()

        except Exception:
            print("Error creando reminder", traceback.format_exc())
            return None

    def process_cmd(self):

        raw_cmd = self.db.get_cmd()['cmd']

        raw_cmd = raw_cmd.split(' ')
        cmd = raw_cmd[0]
        try:
            args = raw_cmd[1:]
        except:
            args = None

        if cmd == '':
            return
        
        if cmd == 'news':
            news = self.get_news()
            self.db.update_cmd_result(news)
            self.db.clear_cmd()
        elif cmd == 'reminders':
            reminders = self.show_reminders()
            self.db.update_cmd_result(reminders)
            self.db.clear_cmd()
        elif cmd == 'reminder':
            if args:
                thread = self.set_reminder(args)
                self.db.clear_cmd()
                return thread
            else: 
                print("Faltan argumentos para el comando reminder")
                return None
