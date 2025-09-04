from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock
import time, threading, pyaudio
from vosk import Model,KaldiRecognizer
from bidi.algorithm import get_display
import arabic_reshaper
from kivy.properties import ObjectProperty, BooleanProperty

Window.size = (300,500)

screen_helper = """
ScreenManager:
    StartScreen:
    MainScreen:
    AboutScreen:

<StartScreen>:
    name: 'start'
    MDLabel:
        text: 'Hello'
        font_style: 'H4'
        halign: 'center'
        pos_hint: {'center_x':0.5, 'center_y':0.6}

    MDSpinner:
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        active: True


<MainScreen>:
    name: 'main'
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    spacing: '0dp'
                    MDTopAppBar:
                        left_action_items: [['menu', lambda x: navigation_drawer.set_state('toggle')]]
                        right_action_items: [['white-balance-sunny', lambda x: app.light_mode()],['moon-waning-crescent', lambda x: app.dark_mode()]]    
                    MDLabel:
                        id: text_output
                        text: 'text appear here!'
                        font_name: 'arial'
                        halign: 'center'
                    MDFloatingActionButton:
                        id: record_button
                        icon: 'circle'
                        pos_hint: {'center_x': 0.5}
                        icon_size: 40
                        on_press:
                            app.record()  
                    Widget:
                        size_hint_y: None
                        height: 50

        MDNavigationDrawer:
            id: navigation_drawer
            radius: (0,16,16,0)
            size_hint_x: 0.75
            BoxLayout:
                orientation: 'vertical'
                spacing: '10dp'
                Image:
                    source: 'cute-turtle.png'
                MDLabel:
                    text: 'Welcome to CalliNour'
                    font_style: 'Subtitle1'
                    size_hint_y: None
                    height: self.texture_size[1]
                    halign: 'center'
                ScrollView:
                    MDList:
                        OneLineIconListItem:
                            text: 'About'
                            on_release:
                                root.go_to_about_page()
                            IconLeftWidgetWithoutTouch:
                                icon: 'information'
                        OneLineIconListItem:
                            text: 'Profile'
                            IconLeftWidgetWithoutTouch:
                                icon: 'face-woman-profile'
                        OneLineIconListItem:
                            text: 'Logout'
                            IconLeftWidgetWithoutTouch:
                                icon: 'logout-variant'

<AboutScreen>:
    name: 'about'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: 'About'
            left_action_items: [['keyboard-backspace', lambda x: root.back_to_main_page()]]
            right_action_items: [['white-balance-sunny', lambda x: app.light_mode()],['moon-waning-crescent', lambda x: app.dark_mode()]]
        MDLabel: 
            text: 'Hello'
            halign: 'center'
            font_style: 'H5'
"""

class StartScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.switch, 3)
    def switch(self,*args):
        self.manager.current = 'main'

class MainScreen(Screen):  
    def go_to_about_page(self):
        self.manager.current = 'about'
class AboutScreen(Screen):
    def back_to_main_page(self):
        self.manager.current = 'main'

screen_manager = ScreenManager()
screen_manager.add_widget(StartScreen(name='start'))
screen_manager.add_widget(MainScreen(name='main'))
screen_manager.add_widget(AboutScreen(name='about'))

class CallinourApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.in_progress = False
        self.mic = None
        self.stream = None
        self.recognizer = None
        self.model = None

    def build(self):
        self.theme_cls.primary_palette = 'Blue' 
        screen = Builder.load_string(screen_helper)

        threading.Thread(target=self.load_model, daemon=True).start()
        return screen

    def load_model(self):
        self.model = Model(r"D:\Briliant ideas\speech to text\Persian versian\vosk-model-small-fa-0.5")
        Clock.schedule_once(self.go_to_main_screen, 0)

    def go_to_main_screen(self,dt):
        self.root.current = 'main'

    def light_mode(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style = 'Light'
        self.update_button_color()
      
    def dark_mode(self):
        self.theme_cls.primary_palette = 'BlueGray'
        self.theme_cls.theme_style = 'Dark'
        self.update_button_color()
        
    def update_button_color(self):
        if self.theme_cls.theme_style == 'Light':
            if not self.in_progress:
                self.root.get_screen('main').ids.record_button.md_bg_color = (56/255.0,156/255.0,1,1)
            else:
                self.root.get_screen('main').ids.record_button.md_bg_color= (1,40/255.0,60/255.0,1)
        else:
            if not self.in_progress:
                self.root.get_screen('main').ids.record_button.md_bg_color= (106/255.0,137/255.0,167/255.0,1)
            else:
                self.root.get_screen('main').ids.record_button.md_bg_color= (139/255.0,0,0,1)


    def farsi_text(self,text):
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)

    def record(self):
        if not self.in_progress:
            self.start_recording() 
        else:
            self.stop_recording()
           

    def start_recording(self):
        self.in_progress = True
        threading.Thread(target=self.process_audio, daemon=True).start()
        print('start recording!')
        self.updateIcon()
    
    def process_audio(self):
        self.recognizer = KaldiRecognizer(self.model,16000)
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.stream.start_stream()

        start_time = time.time()
        while time.time() - start_time < 10 and self.in_progress:
            data = self.stream.read(8192)
            if self.recognizer.AcceptWaveform(data):
                text = self.recognizer.Result()
                main_text = text[14:-3]
                fa_text = self.farsi_text(main_text)
                Clock.schedule_once(lambda dt: self.update_label(fa_text))

        self.stop_recording()

    def update_label(self, text):
        self.label = self.root.get_screen('main').ids.text_output
        if text:
            self.label.text = text
        else:
            self.label.text = self.farsi_text('متن تشخیص داده نشد!')
        
    def updateIcon(self):
        if self.in_progress == True:
            self.root.get_screen('main').ids.record_button.icon = 'square'
            self.update_button_color()
        else:
            self.root.get_screen('main').ids.record_button.icon = 'circle'
            self.update_button_color()
        

    def stop_recording(self):
        if self.in_progress:
            if hasattr(self,'stream') and self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            if hasattr(self, 'mic') and self.mic:
                self.mic.terminate()
                self.mic = None
            if hasattr(self, 'recognizer') and self.recognizer:
                self.recognizer = None
            self.in_progress = False
            self.updateIcon()
            self.root.get_screen('main').ids.text_output.text = 'text appear here!'
            print('record stopped!')
CallinourApp().run()