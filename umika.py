#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''umika
'''

import sys, os, stat
import wx

APP_TITLE = u'umika'

class Umika(wx.Frame):
  def __init__(self, *args, **kwargs):
    super(Umika, self).__init__(title=APP_TITLE, size=(640, 480), pos=(0, 0),
      *args, **kwargs)

if __name__ == '__main__':
  app = wx.App(False)
  frm = Umika(parent=None, id=wx.NewId())
  app.SetTopWindow(frm)
  frm.Show()
  app.MainLoop()
