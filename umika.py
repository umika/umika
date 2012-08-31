#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''umika
'''

import sys, os, stat
import wx

APP_TITLE = u'umika'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_BLANC = os.path.join(BASE_DIR, 'fileblanc.png')
TRANSPARENT_COLOR = '#ffffff' # '#808080'

class FileListBox(wx.VListBox):
  def __init__(self, *args, **kwargs):
    super(FileListBox, self).__init__(*args, **kwargs)
    self.bmp = wx.Bitmap(FILE_BLANC, wx.BITMAP_TYPE_PNG)
    self.bh = self.bmp.GetHeight()
    self.dir, self.files = None, []
    self.RefreshFiles()

  def OnMeasureItem(self, idx):
    # return super(FileListBox, self).OnMeasureItem(idx)
    return self.bh + 4

  def OnDrawSeparator(self, dc, rect, idx):
    oldpen = dc.GetPen()
    dc.SetPen(wx.Pen(wx.BLACK))
    dc.DrawLine(rect.x, rect.y, rect.x + rect.width, rect.y)
    rect.Deflate(0, 2)
    dc.SetPen(oldpen)

  def OnDrawItem(self, dc, rect, idx):
    dc.SetBackground(wx.Brush(TRANSPARENT_COLOR))
    dc.SetBrush(wx.Brush(TRANSPARENT_COLOR))
    dc.SetPen(wx.Pen(TRANSPARENT_COLOR))
    dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)
    dc.DrawBitmap(self.bmp, rect.x + 2, rect.y + (rect.height - self.bh) / 2)
    txtx = rect.x + 2 + self.bh + 2
    lblrect = wx.Rect(txtx, rect.y, rect.width - txtx, rect.height)
    dc.SetPen(wx.Pen(wx.BLACK))
    dc.DrawLabel(self.files[idx], lblrect,
      wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)

  def RefreshFiles(self):
    if self.dir:
      self.files = [f for f in os.listdir(self.dir) if not os.path.isdir(f)]
    self.SetItemCount(len(self.files))

  def SetDir(self, dir):
    self.dir = dir
    self.RefreshFiles()

class Umika(wx.Frame):
  def __init__(self, *args, **kwargs):
    super(Umika, self).__init__(title=APP_TITLE, size=(640, 480), pos=(0, 0),
      *args, **kwargs)
    szv = wx.BoxSizer(wx.VERTICAL)
    pnl = wx.Panel(self)
    if pnl:
      szp = wx.BoxSizer(wx.VERTICAL)
      self.lblfile = wx.StaticText(self, wx.NewId(), 'select a file')
      szp.Add(self.lblfile, 0, wx.ALIGN_LEFT|wx.ALL, 5)
      self.flist = FileListBox(self, wx.NewId(), style=wx.LC_VIRTUAL)
      self.flist.SetDir(os.path.abspath('.'))
      szp.Add(self.flist, 1, wx.EXPAND)
      line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
      szp.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
      szbtn = wx.StdDialogButtonSizer()
      if szbtn:
        sztopbtns = wx.BoxSizer(wx.HORIZONTAL)
        btnclose = wx.Button(pnl, wx.ID_CLOSE)
        sztopbtns.Add(btnclose)
        szbtn.Add(sztopbtns)
        btnapply = wx.Button(pnl, wx.ID_APPLY)
        btnapply.SetDefault()
        szbtn.AddButton(btnapply)
        szbtn.Realize()
        szp.Add(szbtn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
      pnl.SetSizer(szp)
      # szp.Fit(pnl)
      szv.Add(pnl, 1, wx.EXPAND)
    self.SetSizer(szv)
    self.Bind(wx.EVT_LISTBOX, self.OnFlistSelect, self.flist)
    self.Bind(wx.EVT_BUTTON, self.OnBtnClose, btnclose)
    self.Bind(wx.EVT_BUTTON, self.OnBtnApply, btnapply)

  def OnBtnClose(self, ev):
    print 'close'

  def OnBtnApply(self, ev):
    print 'apply'

  def OnFlistSelect(self, ev):
    print 'flist'

if __name__ == '__main__':
  app = wx.App(False)
  frm = Umika(parent=None, id=wx.NewId())
  app.SetTopWindow(frm)
  frm.Show()
  app.MainLoop()
