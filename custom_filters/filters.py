from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from loader import admin_ids, db, ALL_COMMANDS

class IsAdmin(BoundFilter):
    async def check(self, message):
        user_id = message.from_user.id
        if user_id not in admin_ids:
            return False
        else:
            return True


    
class StateChecker(BoundFilter):
    def __init__(self, valid_state, command_priority: bool = False):
        """Class, which checks user state

        Args:
            valid_state : состояние для проверки\n
            command_priority (bool, optional): если юзер 'находится' в команде и отсылает другую команду, то ответа у handler не будет при значении False.
        """
        self.valid_state = valid_state
        self.command_priority = command_priority
        
    async def check(self, message: types.Message):
        user_id = message.from_user.id
        username = message.from_user.username
    
        text = message.text
        if self.command_priority and text:
            if text.strip(" \n") in ALL_COMMANDS:
                return False
        
        user_state_now = db.get_user_state(user_id, username)
        if self.valid_state == user_state_now:
            return True
        else:
            return False

        