#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from command_enum import Command
from config import MIN_PRICE, FIRST_PRICE_THRESHOLD, SECOND_PRICE_THRESHOLD, THIRD_PRICE_THRESHOLD 
from config import REDUCE_ON_FITST_THRESHOLD, REDUCE_ON_SECOND_THRESHOLD, REDUCE_ON_THIRD_THRESHOLD, REDUCE_ON_MAX_THRESHOLD, DISCOUNT_AMOUNT

command = Command()
class Commander:
  lastCommand = None
  retryEnterLinkCount = 0
  LINK = None
  PRICE = 0
  def __init__(self, api, userId):
    self.api = api
    self.userId = userId
  def input(self, message):
    if Commander.lastCommand == None:
      text = f'Привет, {self.getUserName(self.userId)}! Выбери одно из действий что бы продолжить:\n'
      for comm in command.beginQuest:
        text += f'"{comm[0]}": {comm[1]}\n'
      Commander.lastCommand = command.begin
      return [text, 'begin-question']
    if command.begin == Commander.lastCommand:
      if message == command.beginQuest[0][0]:
        Commander.lastCommand = command.beginQuest[0][0]
        return [f'Введите цену товара (она не должна быть меньше чем 300 рублей):', 'cancel-question']
      Commander.lastCommand = command.adminDialog
      return ['Вы вошли в режим диалога с продавцом. Будьте вежливы и соблюдайте правила приличия', 'admin-dialog']
    if Commander.lastCommand == command.beginQuest[0][0]:
      if message == command.cancelQuest:
        Commander.lastCommand = command.begin
        return ['Отменяю', 'begin-question']
      try:
        price = int(message)
        if price < MIN_PRICE:
          Commander.lastCommand = command.beginQuest[0][0]
          return [f'{price} руб - цена слишком мала (она не должна быть меньше чем 300 рублей). Попробуйте ещё раз', 'cancel-question']
        if price >= MIN_PRICE:
          finallyPrice = price
          if price < FIRST_PRICE_THRESHOLD:
            finallyPrice-=REDUCE_ON_FITST_THRESHOLD
          if price > FIRST_PRICE_THRESHOLD and price < SECOND_PRICE_THRESHOLD:
            finallyPrice-=REDUCE_ON_SECOND_THRESHOLD
          if price > SECOND_PRICE_THRESHOLD and price < THIRD_PRICE_THRESHOLD:
            finallyPrice-=REDUCE_ON_THIRD_THRESHOLD
          if price > THIRD_PRICE_THRESHOLD:
            finallyPrice-=REDUCE_ON_MAX_THRESHOLD
          Commander.lastCommand = command.keepLink
          Commander.PRICE = self.price(finallyPrice)
          return [f'Приблизительная цена: {Commander.PRICE}. Введите ссылку на товар с AliExpress (пожалуйста, убедитесь что ссылка корректна и не является фишинговым сайтом, в ином случае вы можете быть заблокированны):', 'cancel-question']
      except:
        Commander.lastCommand = command.beginQuest[0][0]
        return [f'"{message}" не является числом. Попробуйте ещё раз:', 'cancel-question']
    if Commander.lastCommand == command.keepLink:
      if message == command.cancelQuest:
        Commander.lastCommand = command.begin
        return ['Отменяю', 'begin-question']
      if Commander.LINK == None:
        message = message
      else:
        message = Commander.LINK
      link = re.sub(r'&(amp;)+', '&amp;', message)
      aliexpressLinkReExp = r'https://(m\.|a\.)?aliexpress\.(com|ru)/(item/(\d|\w)+\.html(\?(trace=[\d\w#]+)?([\d\w]+=[\d\w_,\.#-]+\&?(amp;)?)+([\d\w_\.,#-]+=([\d\w\./]+)?\&?(amp;)?)+)?)?([\d\w_\.,#-]+)?'
      matches = re.search(aliexpressLinkReExp, link)
      try:
        Commander.LINK = matches.group().strip()
        Commander.lastCommand = command.adminDialog
        return ['Ваш заказ обрабатывается и вы перенаправлены в мод общения с продавцом, ждите ответ. Спасибо за покупки через нашего продавца, совершая каждую покупку помните, что где-то радуется сердечко разработчика этого бота)', 'admin-dialog', f'Цена на товар: {Commander.PRICE}\nСсылка на пользователя: https://vk.com/id{self.userId}\nСсылка на товар: {Commander.LINK}']
      except:
        Commander.lastCommand = command.keepLink
        return [f'"{link}" не является корректной ссылкой. Повторите ещё раз:', 'cancel-question']
    if message == command.cancelAdminDialog:
      Commander.lastCommand = command.youSure
      return ['Вы собираетесь закрыть диалог с продавцом! Если вы его закроете, то продавец не сможет c вами связаться!', 'you-sure']
    if Commander.lastCommand == command.youSure:
      if message == command.youSure[0]:
        Commander.lastCommand = command.begin
        return ['Вы закрыли диалог с продавцом. Возвращаю в главное меню', 'begin-question']
      if message == command.youSure[1]:
        Commander.lastCommand = command.adminDialog
        return ['Возвращаю вас в диалог с продавцом. Что бы войти в диалог напишите одно любое сообщение', 'admin-dialog']
    if Commander.lastCommand == command.adminDialog:
      return ['', 'admin-dialog']
    else:
      Commander.lastCommand = command.begin
      return [f'Я не знаю такую коиианду "{message}". Попробуйте ещё раз:']
    Commander.lastCommand = command.begin
    return ['Что-то пошло не так...', 'begin-question']
  def getUserName(self, userId):
    return self.api.users.get(user_id=userId)[0]['first_name']
  def price(self, price):
    return f'от {price - DISCOUNT_AMOUNT} до {price} руб'
