from typing import List
from controller.client import Client
from controller.exceptions import *

class ClientBase():
    _clients:List[Client] = []

    def get(self, chat_id:str) -> Client:
        for c in self._clients:
            if c.chat_id == chat_id:
                return c
        raise NoClientInBase(chat_id)      

    def add(self, client:Client) -> Client:
        self._clients.append(client)
        return client