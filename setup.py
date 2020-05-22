#!/usr/bin/python
# -*- coding: utf-8 -*-
from server import Server

from config import TOKEN, GROUP_ID

server = Server(TOKEN, GROUP_ID, 'server-one')

server.start()
