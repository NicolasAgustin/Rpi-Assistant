import traceback
from firebase_admin import credentials
from firebase_admin import initialize_app
from firebase_admin import db

class Firebase:
    def __init__(self):
        self.cred_obj = credentials.Certificate('credential.json')
        default_app = initialize_app(self.cred_obj , {
            'databaseURL': "https://asistente-rpi-13f9b-default-rtdb.firebaseio.com/"
        })

    def get_cmd(self) -> dict:
        ref = db.reference('/operations/')
        return ref.get('cmd')[0]

    def clear_cmd(self):
        ref = db.reference('/operations/')
        ref.update({'cmd': ''})

    def update_cmd_result(self, result: str):
        ref = db.reference('/operations/')
        ref.update({'result': result})

    def create_reminder(self, name: dict) -> db.Reference:
        ref = db.reference('/reminders/')
        id = ref.push(name)
        return id

    def delete_by_id(self, id: db.Reference):
        try:
            id.delete()
        except Exception:
            print(traceback.format_exc())
        