#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''umika
'''

import sys, os, stat
import time
import wx
import wx.calendar

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
    # if(len(self.files)): self.Select(0, True) # self.SetSelection(0)
    for i in xrange(len(self.files)): self.Select(i, False)
    self.Refresh()

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
      self.lblts = wx.StaticText(pnl, wx.NewId(), 'please select files')
      szp.Add(self.lblts, 0, wx.ALIGN_LEFT|wx.ALL, 5)
      self.flist = FileListBox(pnl, wx.NewId(),
        style=wx.LB_MULTIPLE|wx.LB_EXTENDED|wx.LB_HSCROLL|wx.LB_NEEDED_SB)
      self.flist.SetDir(os.path.abspath('.'))
      szp.Add(self.flist, 1, wx.EXPAND)
      line = wx.StaticLine(pnl, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
      szp.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
      pnlh0 = wx.Panel(pnl)
      if pnlh0:
        szh = wx.BoxSizer(wx.HORIZONTAL)
        self.cal = wx.calendar.CalendarCtrl(pnlh0, wx.NewId(),
          wx.DateTime_Now(), pos=(0, 0),
          style=wx.calendar.CAL_SHOW_HOLIDAYS | wx.calendar.CAL_SUNDAY_FIRST \
            | wx.calendar.CAL_SHOW_SURROUNDING_WEEKS)
        szh.Add(self.cal, 0, wx.EXPAND)
        pnlh01 = wx.Panel(pnlh0)
        if pnlh01:
          szh01g = wx.GridBagSizer(3, 3)
          btntoday = wx.Button(pnlh01, wx.NewId(), u'reset calendar to today')
          szh01g.Add(btntoday, (0, 0), (1, 2))
          sthour = wx.StaticText(pnlh01, -1, u'hour')
          szh01g.Add(sthour, (1, 0))
          self.hour = wx.TextCtrl(pnlh01, wx.NewId(), u'0')
          szh01g.Add(self.hour, (1, 1))
          stminute = wx.StaticText(pnlh01, -1, u'minute')
          szh01g.Add(stminute, (2, 0))
          self.minute = wx.TextCtrl(pnlh01, wx.NewId(), u'0')
          szh01g.Add(self.minute, (2, 1))
          stsecond = wx.StaticText(pnlh01, -1, u'second')
          szh01g.Add(stsecond, (3, 0))
          self.second = wx.TextCtrl(pnlh01, wx.NewId(), u'0')
          szh01g.Add(self.second, (3, 1))
          pnlh01.SetSizer(szh01g)
        szh.Add(pnlh01, 1, wx.EXPAND)
        pnlh0.SetSizer(szh)
      szp.Add(pnlh0, 0, wx.EXPAND)
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
    self.Bind(wx.calendar.EVT_CALENDAR, self.OnCalDClick, self.cal)
    self.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.OnCalChange, self.cal)
    self.Bind(wx.EVT_BUTTON, self.OnBtnToday, btntoday)
    self.Bind(wx.EVT_BUTTON, self.OnBtnClose, btnclose)
    self.Bind(wx.EVT_BUTTON, self.OnBtnApply, btnapply)
    wx.CallAfter(self.OnBtnToday, (None, ))

  def GetIntValue(self, tgt, min, max):
    try:
      v = int(tgt.GetValue())
      if v < min: v = min
      if v > max: v = max
      return v
    except ValueError, e:
      return 0

  def GetCalDateTime(self):
    wxdt = self.cal.GetDate()
    wxdt.SetHour(self.GetIntValue(self.hour, 0, 23))
    wxdt.SetMinute(self.GetIntValue(self.minute, 0, 59))
    wxdt.SetSecond(self.GetIntValue(self.second, 0, 59))
    return wxdt.GetTicks()

  def FmtTM(self, tm):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tm))

  def SetTSLabel(self):
    tm = self.GetCalDateTime()
    self.lblts.SetLabel(u'time stamp will be set to %s' % self.FmtTM(tm))
    return tm

  def OnCalDClick(self, ev):
    tm = self.SetTSLabel()
    print u'CalDClick %s' % self.FmtTM(tm)

  def OnCalChange(self, ev):
    tm = self.SetTSLabel()

  def OnBtnToday(self, ev):
    wxdt = wx.DateTime()
    wxdt.SetTimeT(time.time()) # must separate sentence to create instance
    self.cal.SetDate(wxdt)
    self.hour.SetValue(str(wxdt.GetHour()))
    self.minute.SetValue(str(wxdt.GetMinute()))
    self.second.SetValue(str(wxdt.GetSecond()))
    wx.CallAfter(self.OnCalChange, (None, ))

  def OnBtnClose(self, ev):
    self.Close()

  def OnBtnApply(self, ev):
    tm = self.SetTSLabel()
    self.DisplaySelectedItems('apply [%s]' % self.FmtTM(tm))
    if self.flist.GetSelectedCount() == 0: return
    d = wx.MessageDialog(self, self.lblts.GetLabel(), APP_TITLE,
      wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
    r = d.ShowModal()
    d.Destroy()
    if r != wx.ID_OK: return
    s, ck = self.flist.GetFirstSelected()
    while s != wx.NOT_FOUND:
      file = os.path.join(self.flist.dir, self.flist.files[s])
      sttm = os.stat(file)[stat.ST_MTIME]
      msg = u'%s\nfrom: %s\nto: %s' % (file, self.FmtTM(sttm), self.FmtTM(tm))
      d = wx.MessageDialog(self, msg, APP_TITLE,
        wx.YES|wx.NO|wx.CANCEL|wx.ICON_QUESTION)
      r = d.ShowModal()
      d.Destroy()
      if r == wx.ID_CANCEL: break
      if r == wx.ID_YES:
        print msg
        os.utime(file, (tm, tm))
      s, ck = self.flist.GetNextSelected(ck)
    self.flist.RefreshFiles()

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
