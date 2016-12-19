import rumps
from ScriptingBridge import *
import AppKit
import time
from Foundation import *
#rumps.debug_mode(True)
import io
from math import sin, cos


info = AppKit.NSBundle.mainBundle().infoDictionary()
info["LSBackgroundOnly"] = "1"

class MailHelper:
    def __init__(self, mailapp="com.apple.Mail"):
        self.mail = SBApplication.applicationWithBundleIdentifier_("com.apple.Mail")

    def mailCount(self):
        ret = {}
    	if self.mail.isRunning():
    		for mailbox in self.mail.inbox().mailboxes():
    		    ret[mailbox.account().name()] = mailbox.unreadCount()
    	return ret

class IconManipulator:
    @staticmethod    
    def add_circle(position, size, color):
        gRect = NSMakeRect(position[0]+.5, position[1]+.5, size-1, size-1)
        gRectb = NSMakeRect(position[0]-.5, position[1]-.5, size+1, size+1)     
    
        circle2 = NSBezierPath.bezierPathWithOvalInRect_(gRectb)
        NSColor.whiteColor().set()
        circle2.fill()
        
        circle = NSBezierPath.bezierPathWithOvalInRect_(gRect)
        color.set()
        circle.fill()
        return

class MailNotifier(rumps.App):
    def __init__(self, ml, interval = 30, ic = "u3.png"):
        super(MailNotifier, self).__init__("MailNotifier", icon=ic)
        self.MailHelper = MailHelper()
        self.timer = rumps.Timer(self.timerb, 5)
        self.maillist = ml
        self.defaulticon = ic
        self.timer.start()

        
    def timercb(self, sender):
        return
    
    def timerb(self, sender):
        
        mc = self.MailHelper.mailCount()
        self.icon = self.defaulticon
        
        iconxdim = int(self._icon_nsimage.size().width)
        iconydim = int(self._icon_nsimage.size().height)
        
        icongrid = [[None]*2 for i in range(2)]
        self._icon_nsimage.lockFocus()
        
        for acc, inf in self.maillist.items():
            if mc[acc] != 0:
                icongrid[inf['posy']][inf['posx']]
                #IconManipulator.add_circle((inf['posx'] * iconxdim - iconxdim/2, inf['posy'] * iconydim - iconydim/2), iconydim, inf['color'])
                IconManipulator.add_circle((inf['posx'] * iconxdim/2, inf['posy'] * iconydim/2), iconydim/2, inf['color'])
                
        self._icon_nsimage.unlockFocus()

        return

if __name__ == "__main__":
    ml = {'mailboxname':{'color':NSColor.purpleColor(), 'posx' : 0, 'posy' : 0} , 'Google':{'color':NSColor.redColor(), 'posx' : 1, 'posy' : 0}, 'AnotherMailboxName':{'color':NSColor.blueColor(), 'posx' : 0, 'posy' : 1}}
    m = MailNotifier(ml)
    m.run()
