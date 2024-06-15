from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivymd.icon_definitions import md_icons
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer, MDDialogContentContainer
import asyncio
from websockets.sync.client import connect


Bonjour = SoundLoader.load('ASCE_bonjour1.wav')


class RootLayout(MDRelativeLayout):
    screen_mngr = ObjectProperty()
    settingsBtn = ObjectProperty()
    homeBtn = ObjectProperty()
    controlsBtn = ObjectProperty()
    testLab = ObjectProperty()
    waterLVL = NumericProperty()

    BtnsOffset = 0

    defaultSize = .16, .05
    #defaultSizeH = 50
    defaultSizeHome = .17,.06
    #defaultSizeHomeH = 60
    inflatedSize = .2,.1
    #inflatedSizeH = 70
    lastTransistion = 'right'

    def communicate(self):
        with connect("ws://4.4.4.100:80") as websocket:
            websocket.send("ss")
            message = float(websocket.recv())
            self.waterLVL = message



    def openDiag(self):
        MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon="information",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="ASCE Levler X1 (Experimental)",
            ),
            # -----------------------Supporting text-----------------------
            MDDialogSupportingText(
                text="This is an experimental app that displays and controls the water level monitoring device (Levler X1), developed by Assil Ferahta (ASCE) at the request of Dr. Aissa",
            ),
            # -----------------------Custom content------------------------
            # ---------------------Button container------------------------
            # -------------------------------------------------------------
            ).open()


    def hopScreens(self,screen,lr,btn):
        self.screen_mngr.current = screen

        if lr=='last':
            self.BtnsOffset = 0
            if self.lastTransistion == 'right':
                lr = 'left'
            else :
                lr = 'right'
        else:
            if lr == 'right':
                self.BtnsOffset = .08
            else:
                self.BtnsOffset = -.08

        self.screen_mngr.transition.direction = lr
        self.lastTransistion = lr


        self.settingsBtn.style = 'tonal'
        self.settingsBtn.size_hint= self.defaultSize
        #self.settingsBtn.height = self.defaultSizeH

        self.controlsBtn.style = 'tonal'

        self.controlsBtn.size_hint= self.defaultSize
        #self.controlsBtn.height = self.defaultSizeH
        self.homeBtn.style = 'tonal'

        self.homeBtn.size_hint = self.defaultSizeHome
        #self.homeBtn.height=  self.defaultSizeHomeH
        self.homeBtn.pos_hint = {"center_x":.5+self.BtnsOffset,"center_y":.94}
        self.settingsBtn.pos_hint = {"center_x":.28+self.BtnsOffset,"center_y": .94}
        self.controlsBtn.pos_hint = {"center_x":.72+self.BtnsOffset,"center_y": .94}
        btn.size_hint = self.inflatedSize
        # btn.width = self.inflatedSizeW
        # btn.height = self.inflatedSizeH
        btn.style = "filled"



class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette= "Lightgreen"
        self.theme_cls.theme_style=  "Light"
        return Builder.load_file("lvlrApp.kv")

    def on_start(self):
        super().on_start()
        if Bonjour:
            Bonjour.play()

MainApp().run()
