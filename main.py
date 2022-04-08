import time
import traceback
from typing import List
from threading import Thread, Condition
from utils import Firebase
from utils import Logger
from utils import Assistant

def manage_reminders(reminders: List, condition: Condition):
    while execute:
        try:
            i = 0
            condition.acquire()
            for r in reminders:
                if r != None:
                    r.join()
                del reminders[i]
                i+=1
            # print("Hilo dormido")
            condition.wait()
            # print("Hilo despierto")
        except Exception:
            print(traceback.format_exc())
    print("Hilo de recordatorios finalizado")

def main():
    
    # logger = Logger(__file__)
    # logger.info('Iniciando app')
    threads = []
    global execute 
    execute = True
    t_condition = Condition()
    reminders_thread = Thread(target=manage_reminders, args=(threads, t_condition))
    reminders_thread.daemon = True
    
    try:
        reminders_thread.start()

        assistant = Assistant()

        while True:

            if threads and t_condition.acquire():
                t_condition.notify()
                t_condition.release()

            if assistant.has_reminders_to_notify():
                # Notificamos los reminders y continuamos 
                reminders = assistant.get_reminders()
                assistant.notify_reminders(reminders)
                reminders.clear()

            new_t = assistant.process_cmd()

            threads.append(new_t)

            time.sleep(5)
    except (KeyboardInterrupt, Exception) as ex:
        print(f"Ejecucion finalizada por: {traceback.format_exc()}")
        execute = False
        if t_condition.acquire():
            t_condition.notify()
            t_condition.release()
        reminders_thread.join()

if __name__ == '__main__':
    main()