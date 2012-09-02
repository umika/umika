#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''umika
'''

import sys, os, stat
import time
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

  def OnDrawBackground(self, dc, rect, idx):
    # super(FileListBox, self).OnDrawBackground(dc, rect, idx)
    # self.GetSelectionBackground()
    col = wx.CYAN if self.IsSelected(idx) else TRANSPARENT_COLOR
    dc.SetBackground(wx.Brush(col))
    dc.SetBrush(wx.Brush(col))
    dc.SetPen(wx.Pen(col))
    dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)

  def OnDrawSeparator(self, dc, rect, idx):
    # super(FileListBox, self).OnDrawSeparator(dc, rect, idx)
    oldpen = dc.GetPen()
    dc.SetPen(wx.Pen(wx.BLACK))
    btm = rect.y + rect.height - 1
    dc.DrawLine(rect.x, btm, rect.x + rect.width, btm)
    rect.Deflate(0, 2)
    dc.SetPen(oldpen)

  def OnDrawItem(self, dc, rect, idx):
    # super(FileListBox, self).OnDrawItem(dc, rect, idx)
    dc.DrawBitmap(self.bmp, rect.x + 2, rect.y + (rect.height - self.bh) / 2)
    txtx = rect.x + 2 + self.bh + 2
    wsz, wts = 200, 200
    lblrect = wx.Rect(txtx, rect.y, rect.width - txtx - wsz - wts, rect.height)
    dc.SetPen(wx.Pen(wx.BLACK))
    dc.DrawLabel(self.files[idx], lblrect,
      wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
    if self.dir:
      st = os.stat(os.path.join(self.dir, self.files[idx]))
      ts = time.strftime('%Y-%m-%d %H:%M:%S',
        time.localtime(st[stat.ST_MTIME]))
      lblrect = wx.Rect(rect.width - wsz - wts, rect.y, wsz, rect.height)
      dc.DrawLabel(str(st[stat.ST_SIZE]), lblrect,
        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
      lblrect = wx.Rect(rect.width - wts, rect.y, wts, rect.height)
      dc.DrawLabel(' %s' % ts, lblrect,
        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)

  def RefreshFiles(self):
    if self.dir is None: self.files = []
    else:
      self.files = [f for f in os.listdir(self.dir) if not os.path.isdir(f)]
    self.SetItemCount(len(self.files))
    if(len(self.files)): self.Select(0, True) # self.SetSelection(0)

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
      self.lblfile = wx.StaticText(pnl, wx.NewId(), 'select a file')
      szp.Add(self.lblfile, 0, wx.ALIGN_LEFT|wx.ALL, 5)
      self.flist = FileListBox(pnl, wx.NewId(),
        style=wx.LB_MULTIPLE|wx.LB_EXTENDED|wx.LB_HSCROLL|wx.LB_NEEDED_SB)
      self.flist.SetDir(os.path.abspath('.'))
      szp.Add(self.flist, 1, wx.EXPAND)
      line = wx.StaticLine(pnl, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
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
    self.Close()

  def OnBtnApply(self, ev):
    self.DisplaySelectedItems('apply')

  def OnFlistSelect(self, ev):
    self.DisplaySelectedItems('flist')

  def DisplaySelectedItems(self, fname):
    print fname,
    c = self.flist.GetSelectedCount()
    print c,
    # print self.flist.GetSelection() # -1: wx.NOT_FOUND
    lst = []
    s, ck = self.flist.GetFirstSelected()
    while s != wx.NOT_FOUND:
      lst.append(s)
      s, ck = self.flist.GetNextSelected(ck)
    print lst

if __name__ == '__main__':
  app = wx.App(False) # wx.InitAllImageHandlers()
  frm = Umika(parent=None, id=wx.NewId())
  app.SetTopWindow(frm)
  frm.Show()
  app.MainLoop()
