#!/usr/bin/python
# -*- coding: utf-8 -*-
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from commander import Commander
from config import ADMIN_IDS

class Server:
  def __init__(self, token, groupId, serverName: str="empty-server"):
    self.serverName = serverName
    self.vk = vk_api.VkApi(token=token)
    self.api = self.vk.get_api()
    self.longpoll = VkLongPoll(self.vk, groupId)
  def sendMessage(self, userId, message, keyboard = None):
    if keyboard == None:
      self.api.messages.send(peer_id=userId, message=message, random_id=random.randint(0, 2048))
    else:
      self.api.messages.send(peer_id=userId, message=message, random_id=random.randint(0, 2048), keyboard=open(f'keyboard/{keyboard}.json',"r",encoding="UTF-8").read())
  def start(self):
    for event in self.longpoll.listen():
      if event.to_me:
        if event.type == VkEventType.MESSAGE_NEW:
          commander = Commander(self.api, event.user_id)
          message = commander.input(event.text)
          if message[0] == '' or message[0] == None:
            continue
          try:
            if message[2]:
              self.sendMessage(event.user_id, message[0], message[1])
              for ADMIN_ID in ADMIN_IDS:
                self.sendMessage(ADMIN_ID, message[2], 'admin-dialog')
          except:
            self.sendMessage(event.user_id, message[0], message[1])
  def getUserName(self, userId):
    return self.api.users.get(user_id=userId)[0]['first_name']
