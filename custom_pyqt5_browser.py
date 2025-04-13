# importing necessary modules
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
from PyQt5.QtWebEngineWidgets import *
import sys

# creating a class to edit the right click menu
class CustomizedBrowser(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # changing the color set of the right click menu
        #background color: orange; font color: black; selected action: gray
        self.setStyleSheet('''QMenu {background: orange; color: black;}
         QMenu::item:selected {background: lightGray; }''')
    # forming and adding actions to the right click menu
    def contextMenuEvent(self, event):
        self.menu = QMenu(self)
        # creating the reload button
        back_action = self.menu.addAction('Back')
        next_action = self.menu.addAction('Next')
        reload_action = self.menu.addAction('Reload')
        close_action = self.menu.addAction('Close')
        right_click_action = self.menu.exec_(self.mapToGlobal(event.pos()))
        # adjusting the reload button so that if it pressed, the current page will reload itself
        if right_click_action == reload_action:
            self.reload()
        if right_click_action == back_action:
            self.back()
        if right_click_action == next_action:
            self.forward()
        if right_click_action == close_action:
            app.closeAllWindows()
        # there was a bug that keeps right click menu intact after the browser closed.
        # for that closeEvent used to prevent this situation.
            self.closeEvent()
        self.menu.popup(event.globalPos())

# creating a class for the main window of the browser
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # creating a widget for tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.urlbar = QLineEdit()

        # web addresses are just for test purposes 
        # first tab web address 
        self.add_new_tab(QUrl('http://www.example.com')) 
        # second tab web address 
        self.add_new_tab(QUrl('https://www.wikipedia.org')) 
        # third tab web address 
        self.add_new_tab(QUrl('https://www.github.com')) 

        # display the window and tabs in maximized mode
        self.showMaximized()
        self.setFixedSize(self.size())

        # naming the window
        self.setWindowTitle("Secure Kiosk Browser") 

    #defining request to exit from browser and browser's responds to these requests
    def closeEvent(self, event):
        request = QMessageBox.question(None, 'Closing request', 'Are you sure you want to quit this browser?',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)
        if request == QMessageBox.Yes:
            QMainWindow.closeEvent(self, event)
        else:
            event.ignore()

    # function to create new tabs
    def add_new_tab(self, qurl=None, label="Blank"):

        # making a QWebEngineView object and setting url
        browser = CustomizedBrowser()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # make browser to change when url is changed, updating url, titling tabs
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    # if double click occurs:
    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    # if the current tab is switched:
    def current_tab_changed(self, i):

        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        # changing the title
        self.update_title(self.tabs.currentWidget())

    # if a tab is closed:
    def close_current_tab(self, i):

        # if the number of remaining tabs is one
        if self.tabs.count() < 2:
            return
        # if not the tab needs to be removed
        self.tabs.removeTab(i)

    # updating the title of the browser
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        # naming the title of the window
        self.setWindowTitle("%s - Secure Kiosk Browser" % title) 

    # function for url navigation
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    # function for url update
    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return

        self.urlbar.setText(q.toString())
        # adjust the cursor position for browsing
        self.urlbar.setCursorPosition(0)

# making a new PyQt app
app = QApplication(sys.argv)
# naming the app
app.setApplicationName("Secure Kiosk Browser") 
window = MainWindow()
# executing the app
app.exec_()