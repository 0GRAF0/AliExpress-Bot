#!/usr/bin/python
# -*- coding: utf-8 -*-
class Command:
  def __init__(self):
    self.begin = 'Начать'
    self.beginQuest = [
        ['Узнать цену', 'что бы приобрести нужный вам товар по скидке'],
        ['Задать вопрос', 'что бы связаться с продавцом на прямую без подсчёта цены'],
    ]
    self.keepLink = 'Получить ссылку'
    self.cancelQuest = 'Отмена'
    self.adminDialog = 'Диалог с продавцом'
    self.cancelAdminDialog = 'Закрыть диалог'
    self.youSure = ['Да', 'Нет']
