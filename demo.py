import os
import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        # Initialize the window
        self.init()
        # Initialize the tray settings
        self.initPall()
        # Load the static gif image of the pet
        self.initPetImage()
        # Normal standby for the pet, implementing random actions
        self.petNormalAction()

    # Initialize the window
    def init(self):
        # Initialization
        # Set window properties: window without title bar and fixed at the top
        # FrameWindowHint: window without borders
        # WindowStaysOnTopHint: the window always stays on top
        # SubWindow: the new window component is a subwindow, regardless of whether the window component has a parent window component
        # https://blog.csdn.net/kaida1234/article/details/79863146
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        # setAutoFillBackground(True) means automatically fill the background, False for transparent background
        self.setAutoFillBackground(False)
        # Window transparency, window space is opaque
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # Repaint the component, refresh
        self.repaint()

    # Initialize the tray settings
    def initPall(self):
        # Import the icon to be used for display in the tray
        icons = os.path.join('1.png')
        # Set the right-click menu item for minimizing
        # Menu item exit, call quit function when clicked
        quit_action = QAction('Exit', self, triggered=self.quit)
        # Set the image for this click option
        quit_action.setIcon(QIcon(icons))
        # Menu item display, call showing function when clicked
        showing = QAction(u'Show', self, triggered=self.showwin)
        # Create a new menu item control
        self.tray_icon_menu = QMenu(self)
        # Add a menu item 'Exit' without submenu to the menu bar
        self.tray_icon_menu.addAction(quit_action)
        # Add a menu item 'Show' without submenu to the menu bar
        self.tray_icon_menu.addAction(showing)
        # QSystemTrayIcon class provides an icon for the application in the system tray
        self.tray_icon = QSystemTrayIcon(self)
        # Set the tray icon
        self.tray_icon.setIcon(QIcon(icons))
        # Set the tray menu items
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        # Display
        self.tray_icon.show()

    # Load the static gif image of the pet
    def initPetImage(self):
        # Define dialog
        self.movie = QMovie(":/image1")
        # Set the pet image component to a gif
        self.label = QLabel(self)
        self.label.setMovie(self.movie)
        self.movie.start()
        self.resize(self.movie.currentImage().size())
        self.movie.frameChanged.connect(self.update_frame)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.setGeometry(QRect(0, 0, self.movie.currentImage().width(), self.movie.currentImage().height()))

    # Implement random actions for the pet in normal standby
    def petNormalAction(self):
        # Import gif file list
        self.gif_list = [':/image1', ':/image2']
        self.gif = random.choice(self.gif_list)
        self.movie.setFileName(self.gif)
        self.movie.start()

    # Define dialog
    def talk(self):
        talk_list = ['Hello', 'I am your desktop pet!', 'I can do many things.']
        self.label.setText(random.choice(talk_list))

    def update_frame(self, frame_number):
        # Redraw the component
        self.repaint()

    def quit(self):
        qApp.quit()

    def showwin(self):
        self.setWindowOpacity(1)

    def mousePressEvent(self, event):
        # Change pet state to clicked
        self.condition = 1
        # Change pet dialog state
        self.talk_condition = 1
        # Call dialog state change
        self.talk()
        # Load pet click animation immediately
        self.randomAct()
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
        # globalPos() The position of the event trigger point relative to the desktop
        # pos() The position of the program relative to the top left corner of the desktop, which is actually the coordinates of the top left corner of the window
        self.mouse_drag_pos = event.globalPos() - self.pos()
        event.accept()
        # Set the mouse icon during dragging
        self.setCursor(QCursor(Qt.OpenHandCursor))

    # Called when the mouse moves, making the pet follow the mouse
    def mouseMoveEvent(self, event):
        # If the left mouse button is pressed and is in the binding state
        if Qt.LeftButton and self.is_follow_mouse:
            # Move the pet with the mouse
            self.move(event.globalPos() - self.mouse_drag_pos)
        event.accept()

    # Called when the mouse is released, cancel the binding
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        # Set the mouse icon to an arrow
        self.setCursor(QCursor(Qt.ArrowCursor))

    # Called when the mouse enters
    def enterEvent(self, event):
        # Set the mouse shape to Qt.ClosedHandCursor
        self.setCursor(Qt.ClosedHandCursor)

    # Pet right-click interaction
    def contextMenuEvent(self, event):
        # Define the menu
        menu = QMenu(self)
        # Define menu items
        quitAction = menu.addAction("Exit")
        hide = menu.addAction("Hide")
        # Use exec_() method to display the menu. Get the current coordinates from the mouse right-click event object. mapToGlobal() method converts the current component's relative coordinates to the window's absolute coordinates.
        action = menu.exec_(self.mapToGlobal(event.pos()))
        # Click event is exit
        if action == quitAction:
            qApp.quit()
        # Click event is hide
        if action == hide:
            # Hide the pet by setting opacity
            self.setWindowOpacity(0)

if __name__ == '__main__':
    # Create a QApplication object, named app, with two parameters argc, argv
    # All PyQt5 applications must create an Application object. sys.argv parameter is a list of arguments from the command line.
    app = QApplication(sys.argv)
    # Initialize the window component
    pet = DesktopPet()
    # 1. Enter the event loop;
    # 2. Wait, until responding to possible input from the app;
    # 3. QT receives and processes user and system events (messages), and passes them to each window;
    # 4. When the program encounters exit(), it returns the value of exec().
    sys.exit(app.exec_())
