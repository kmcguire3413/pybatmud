from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit

from pkg.qsubwindow import QSubWindow

class QConsoleWindow(QtGui.QWidget):
    """A Qt widget that provides a console like window.

    A Qt widget that provides a console like window with support for rendering
    terminal codes visually, and provides command input. This can be used to
    display select information such as game messages, channel messages, or even
    messages produced soley by the system.
    """
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.wp.resize(self.width() - 6, self.height() - (3 + 25))
        self.ce.move(2, self.height() - (25 + 3))
        self.ce.resize(self.width() - 5, 26)

    def keyPressEvent(self, event):
        """Helps ensure keystrokes go to the command box.
        """
        # we seem to be sent key press events even
        # if the command line box has focus, so we
        # need to check if it has focus, and if not
        # send it the key pressed then switch focus
        # to it
        if not self.ce.hasFocus():
            self.ce.setFocus()
            self.ce.keyPressEvent(event)
        # look for up and down arrows
        key = event.key()
        if key == QtCore.Qt.Key_Up or key == QtCore.Qt.Key_Down:
            if key == QtCore.Qt.Key_Up:
                up = True
            else:
                up = False
            if self.updowncallback is not None:
                self.updowncallback(up)

    def commandEvent(self, line):
        pass

    def focusInEvent(self, event):
        pass

    def showEvent(self, event):
        pass

    def _commandEvent(self):
        print(self, '<ENTER>')
        text = self.ce.text()       # get command box text
        self.ce.setText('')         # clear command box
        #self.setprompt(b'')         # clear prompt
        return self.commandEvent(text)

    def dummyKeyPressEvent(self, event):
        pass

    def commandchange_event(self):
        print('CHANGED_EVENT')
        if self.commandchangedcallback is not None:
            self.commandchangedcallback(self.ce.text())

    def setcommandchangedcallback(self, cb):
        self.commandchangedcallback = cb

    def setupdowncallback(self, cb):
        self.updowncallback = cb

    def setcommandline(self, text):
        self.ce.setText(text)

    def __init__(self, pwin, css):
        super().__init__(pwin)
        self.pwin = pwin

        self.setObjectName('ConsoleWindow')

        self.commandchangedcallback = None
        self.updowncallback = None

        self.ce = QtGui.QLineEdit(self)
        self.ce.setObjectName('CommandLine')
        self.ce.show()
        self.ce.textChanged.connect(lambda: self.commandchange_event())
        #self.ce.setEnabled(False)
        #self.ce._keyPressEvent = self.ce.keyPressEvent
        #self.ce.keyPressEvent = self.dummyKeyPressEvent

        self.wp = QtWebKit.QWebView(self)
        self.wp.move(3, 0)
        self.wp.keyPressEvent = self.keyPressEvent

        self.ce.returnPressed.connect(lambda: self._commandEvent())

        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # hopefully this ends up calling resizeEvent
        self.wp.resize(600, 100)

        self.wp.setObjectName('ConsoleHTMLView')
        # style="font-size: 8pt; line-height: 1; font-family: consolas;"
        self.wp.setHtml('<html><head><style>%s</style></head><body><span class="lines" id="lines"></span><span class="xprompt" id="xprompt"></span></body></html>' % css)

        self.wp.show()

        #self.wp.contentSizeChanged.connect(lambda: print('CHANGED'))

        #self.sa.setWidgetResizable(1)
        #self.sa.setWidget(self.wp)
        #self.sa.show()

        self.resize(600, 100)

        self.show()

        # used to handle terminal escape sequences
        self.colormap = {
            '0': 'black',
            '1': 'red',
            '2': 'green',
            '3': 'yellow',
            '4': 'blue',
            '5': 'magenta',
            '6': 'cyan',
            '7': 'white',
            '9': 'default',
        }

        self.fgbright = False
        self.nfgcolor = 'hc_fg_default'
        self.nbgcolor = 'hc_bg_default'
        self.fgcolor = self.nfgcolor
        self.bgcolor = self.nbgcolor

    def processline(self, line, fgdef = None, bgdef = None):
        """Add line but convert terminal codes into HTML and convert from bytes to string.
        """
        # remove crazy escape codes
        parts = line.split(b'\xff')
        
        line = []
        line.append(parts[0])

        for x in range(1, len(parts)):
            part = parts[x]
            if part[0] == 0xf9:
                # prompt (clear line buffer), as far as i can tell the server
                # sends it to setup the prompt to be displayed to the user and
                # not as part of the normal flow of messages, so i just drop
                # it in here
                line = []
                continue
            line.append(part[1:])

        line = b''.join(line)

        # convert to string and replace any crazy characters
        line = line.decode('utf8', 'replace')

        # escape any quotes because we encode this string into
        # javascript call and unescaped quotes will screw it up
        line = line.replace('"', '\\"')

        # split it to handle terminal escape codes
        parts = line.split('\x1b')

        line = []

        fgdef = fgdef or self.fgcolor
        bgdef = bgdef or self.bgcolor

        line.append('<span class=\\"%s %s\\">%s</span>' % (fgdef, bgdef, parts[0].replace(' ', '&nbsp')))

        for x in range(1, len(parts)):
            part = parts[x]
            cstr = part[0:part.find('m')]
            rmsg = part[part.find('m') + 1:]
            codes = cstr[1:].split(';')
            if len(codes) < 1:
                self.fgcolor = self.nfgcolor
                self.bgcolor = self.nbgcolor
            for code in codes:
                if len(code) < 1:
                    continue
                if code == '0':
                    self.fgcolor = self.nfgcolor
                    self.bgcolor = self.nbgcolor
                    self.fgbright = False
                    continue
                if code == '1':
                    self.fgbright = True
                    continue
                if code == '2':
                    self.fgbright = False
                    continue
                if code[0] == '3':
                    val = code[1]
                    if val in self.colormap:
                        if self.fgbright:
                            self.fgcolor = 'hc_bfg_%s' % self.colormap[val]
                        else:
                            self.fgcolor = 'hc_fg_%s' % self.colormap[val]
                    continue
                if code[0] == '4':
                    if code[1] in self.colormap:
                        self.bgcolor = 'hc_bg_' % self.colormap[code[1]]
                    continue
                raise Exception('Ignored Code "%s"' % code)

            rmsg = rmsg.replace('\t', '&#9;')
            rmsg = rmsg.replace(' ', '&nbsp;')
            line.append('<span class=\\"%s %s\\">%s</span>' % (self.fgcolor, self.bgcolor, rmsg))

        line = ''.join(line)

        return line

    def processthenaddline(self, line):
        line = self.processline(line)
        if len(line) > 0:
            self.addline(line)

    def scrolltoend(self):
        self.wp.page().mainFrame().evaluateJavaScript('window.scrollTo(0, document.body.scrollHeight);')

    def setprompt(self, prompt, fgdef = None, bgdef = None):
        # set the prompt AND scroll the window buffer to end
        prompt = self.processline(prompt, fgdef, bgdef)
        self.wp.page().mainFrame().evaluateJavaScript('xprompt.innerHTML = "%s";' % prompt)
        self.scrolltoend()

    def addline(self, html):
        # add line to content with magic to make
        # it scroll ONLY if already scrolled near
        # to end of document (helps to lock it if
        # the user has it scrolled upwards when new
        # stuff is added)
        self.wp.page().mainFrame().evaluateJavaScript('var scrollit; if (document.body.scrollTop > document.body.scrollHeight - document.body.clientHeight - 1 || document.body.scrollTop == 0) scrollit = true; else scrollit = false; var m = document.createElement("div"); m.innerHTML = "%s"; lines.appendChild(m); if (scrollit) window.scrollTo(0, document.body.scrollHeight);' % html)


