import os
import json

settings_dir = os.path.dirname(os.path.realpath(__file__))
settings_path = f"{settings_dir}/settings.json"

def get_bot_token():
     with open(settings_path, "r", encoding="utf-8") as file:
        settings = json.loads(file.read())
        return settings["bot-token"]

def get_admins():
    with open(settings_path, "r", encoding="utf-8") as file:
        settings = json.loads(file.read())
        return settings["admins"]

def get_chat_ids_for_distribution():
    with open(settings_path, "r", encoding="utf-8") as file:
        settings = json.loads(file.read())
        return settings["chat_ids_for_distribution"]

def delete_admin(user_id):
    with open(settings_path, "r+", encoding="utf-8") as file:
        settings = json.loads(file.read())
        if user_id in settings["admins"]:
            settings["admins"].remove(user_id)
        file.seek(0)
        file.truncate(0)
        file.write(json.dumps(settings, ensure_ascii=False))
            
def delete_chat_id_for_distribution(chat_id):
    with open(settings_path, "r+", encoding="utf-8") as file:
        settings = json.loads(file.read())
        if chat_id in settings["chat_ids_for_distribution"]:
            settings["chat_ids_for_distribution"].remove(chat_id)
        file.seek(0)            
        file.truncate(0)
        file.write(json.dumps(settings, ensure_ascii=False))
        
def add_admin(user_id):
    with open(settings_path, "r+", encoding="utf-8") as file:
        settings = json.loads(file.read())
        if user_id not in settings["admins"]:
            settings["admins"].append(user_id)
        file.seek(0)
        file.truncate(0)
        file.write(json.dumps(settings, ensure_ascii=False))

def add_chat_id_for_distribution(chat_id):
    with open(settings_path, "r+", encoding="utf-8") as file:
        settings = json.loads(file.read())
        if chat_id not in settings["chat_ids_for_distribution"]:
            settings["chat_ids_for_distribution"].append(chat_id)
        file.seek(0)
        file.truncate(0)
        file.write(json.dumps(settings, ensure_ascii=False))
        