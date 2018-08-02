'''


** Web Browser Desktop Application**

Language: Python3
Frameworks: PyQt5 (a wrapper around QT Framework in python)

Made by :

        Abhishek Anand
        Lakshmi Narain College of Tehnology,Bhopal

        Github-id ->  https://github.com/Abhi-2109
        HackerEarth id -> https://www.hackerearth.com/@abhishek197770
        HackerRank Id -> https://www.hackerrank.com/abhishek197770
        CodeFights/ CodeSignals -> https://app.codesignal.com/profile/abhi2109

'''




import sys
import os
import json

from PyQt5.QtWidgets import (QApplication,QWidget,QVBoxLayout,QHBoxLayout,
                             QPushButton, QLabel, QLineEdit,QTabBar,
                             QFrame, QStackedLayout, QTabWidget, QShortcut,)


from PyQt5.QtGui import QIcon, QWindow, QImage, QKeySequence

from PyQt5.QtCore import *

from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWebKit import *





class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()









class App(QFrame):
    def __init__(self):
        super().__init__()                  # Initializing the parent class
        self.setWindowTitle('Web Browser')  # Setting Window Title
        self.setBaseSize(1366,768)
        self.setWindowIcon(QIcon("download.png"))
        self.setMinimumSize(1366,768)
        self.CreateApp()                # calling the createApp function from initialization

    def CreateApp(self):

        self.layout = QVBoxLayout()         # using vertical Box layout
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)         #To set margins equal to zero from all side

        # Create Tabs

        self.tabbar = QTabBar(movable = True, tabsClosable =True)           # adding TabBar
                                                                    #  movable means we can move the tab
                                                                    # tabsClosable means the tabs should close if the cross button is pressed
        self.tabbar.tabCloseRequested.connect(self.closeTab)  #It passes the argument of index number of the tab of which close button is been clicked.
        self.tabbar.tabBarClicked.connect(self.switchtab)
        # The basic difference between QTabWidget and QTabBar
        # QtabWidget associates a QWidget to # Here we style all the buttons each tab of QTabBar, So widget management when switching from one
        # tab to another is already done by the QtabWidget Class.

        #QtabBar is only a tab bar. You can do everything you want when switching from one tab to another

        # The best advantage is that QTabWidget combines QTabBar and QstackedWidget behaviours.

        self.tabbar.setCurrentIndex(0)
        self.tabbar.setDrawBase(False)
        self.tabbar.setLayoutDirection(Qt.LeftToRight)
        self.tabbar.setElideMode(Qt.ElideLeft)

        #Keep track of tabs

        self.tabcount = 0
        self.tabs = []
        self.deletedtabslist = []

        # Create AddressBar
        self.Toolbar = QWidget()
        self.Toolbar.setObjectName("Toobar")
        self.ToolbarLayout = QHBoxLayout()
        self.addressbar = AddressBar()

        self.AddTabButton = QPushButton("+")
        self.AddTabButton.setMaximumWidth(30)



        self.addressbar.returnPressed.connect(self.BrowseTo)
        self.AddTabButton.clicked.connect(self.AddTab)

        # Set Toolbar Buttons

        self.BackButton = QPushButton("<")
        self.BackButton.clicked.connect(self.GoBack)
        self.BackButton.setMaximumWidth(30)
        self.ForwardButton = QPushButton(">")
        self.ForwardButton.clicked.connect(self.GoForward)
        self.ForwardButton.setMaximumWidth(30)
        self.ReloadButton = QPushButton("↺")
        self.ReloadButton.clicked.connect(self.Reload)
        self.ReloadButton.setMaximumWidth(30)


        self.shortcutNewTab = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_T), self)
        self.shortcutNewTab.activated.connect(self.AddTab)

        # Refresh
        self.shortcutRefresh = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcutRefresh.activated.connect(self.Reload)
        self.shortcutRefresh2 = QShortcut(QKeySequence("F5"), self)
        self.shortcutRefresh2.activated.connect(self.Reload)


        # Toolbar options
        self.Toolbar.setLayout(self.ToolbarLayout)
        self.ToolbarLayout.addWidget(self.BackButton)
        self.ToolbarLayout.addWidget(self.ForwardButton)
        self.ToolbarLayout.addWidget(self.ReloadButton)
        self.ToolbarLayout.addWidget(self.addressbar)
        self.ToolbarLayout.addWidget(self.AddTabButton)

        # set main view
        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)


        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.Toolbar)
        self.layout.addWidget(self.container)

        self.setLayout(self.layout)

        self.AddTab()

        self.show()

    def closeTab(self,i):
        self.tabbar.removeTab(i)
        self.deletedtabslist.append(i)
        self.deletedtabslist.sort()
        m = i-1
        if m == -1:
            self.AddTab()
            return
        while m >= 0:
            if m not in self.deletedtabslist :
                self.switchtab(m)
                return
            else:
                m -= 1




    def AddTab(self):
        i = self.tabcount

        # setting self.tabs[#] = QWidget
        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].layout.setContentsMargins(0,0,0,0)





        # For Tab Switching
        self.tabs[i].setObjectName("tab" + str(i))


        # Open Web View
        self.tabs[i].content = QWebView()
        self.tabs[i].content.load(QUrl("https://www.google.com/"))
        self.addressbar.setText("https://www.google.com/")

        self.tabs[i].content.titleChanged.connect(lambda : self.setTabContent(i, "title"))
        self.tabs[i].content.iconChanged.connect(lambda: self.setTabContent(i, "icon"))
        self.tabs[i].content.urlChanged.connect(lambda : self.setTabContent(i,"url"))




        # Add webview to tabs layout
        self.tabs[i].layout.addWidget(self.tabs[i].content)

        # Set top level tab from [] to layout
        self.tabs[i].setLayout(self.tabs[i].layout)


        # Add tab to top level of stackWidget
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])

        #set the tab at the top of screen
        # Set tabData to tab<#> So it knows what self.tabs[#] it needs to control

        self.tabbar.addTab("New Tab")
        self.tabbar.setTabData(i,{"object": "tab" + str(i), "initial": i})




        self.tabbar.setCurrentIndex(i)

        self.tabcount += 1

    def switchtab(self,i):

        # Switch to tab get current tabs TabData ("tab0") and find object with name
        if self.tabbar.tabData(i):
            tab_data = self.tabbar.tabData(i)["object"]

            tab_content = self.findChild(QWidget, tab_data)
            self.container.layout.setCurrentWidget(tab_content)

            new_url = tab_content.content.url().toString()

            self.addressbar.setText(new_url)


    def BrowseTo(self):
        i = self.tabbar.currentIndex()
        if self.tabbar.tabData(i):
            text = self.addressbar.text()

            # To get the tab data


            tab = self.tabbar.tabData(i)["object"]
            web_view = self.findChild(QWidget, tab).content

            if "http" not in text :
                if "." not in text:
                    url = "https://www.google.ca/#q=" + text
                else:
                    url = "http://" + text
            else:
                url = text

            web_view.load(QUrl(url))

    def setTabContent(self,i,type):
        if self.tabbar.tabData(i):
            tab_name = self.tabs[i].objectName()

            count = 0

            running = True

            current_tab = self.tabbar.tabData((self.tabbar.currentIndex()))["object"]

            if current_tab == tab_name == tab_name and type == 'url':
                new_url = self.findChild(QWidget, tab_name ).content.url().toString()
                self.addressbar.setText(new_url)
                return False

            while running:
                tab_data_name = self.tabbar.tabData(count)


                if count >= 99:
                    running = False


                if tab_name == tab_data_name["object"]:
                    if type == "title":
                        newTitle = self.findChild(QWidget, tab_name).content.title()
                        self.tabbar.setTabText(count, newTitle)
                    elif type == "icon":
                        print(12)
                        newIcon = self.findChild(QWidget,tab_name).content.icon()
                        self.tabbar.setTabIcon(count, newIcon)

                    running = False
                else:
                    count += 1

    def GoBack(self):
        active_index = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(active_index)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.back()



    def GoForward(self):
        active_index = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(active_index)["object"]
        tab_content = self.findChild(QWidget, tab_name).content
        tab_content.forward()

    def Reload(self):
        active_index = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(active_index)["object"]
        tab_content = self.findChild(QWidget, tab_name).content
        tab_content.reload()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    #os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = "^^&"
    window = App()

    with open("style.css",'r') as style:
        app.setStyleSheet(style.read())
        style.seek(0)


    sys.exit(app.exec_())


