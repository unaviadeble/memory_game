from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import random

class MemoryGame(BoxLayout):
    def __init__(self, **kwargs):
        super(MemoryGame, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.colors = ['красный', 'синий', 'зеленый', 'желтый', 'фиолетовый', 'оранжевый', 'розовый', 'голубой', 'коричневый']
        self.correct_sequence = []
        self.user_sequence = []

        self.intro_label = Label(text="Добро пожаловать в игру 'Memory Game'", font_size=30)
        self.add_widget(self.intro_label)

        self.sequence_label = Label(text="Запомните последовательность", font_size=20)
        self.dif_label = Label(text="Выберите сложность", font_size=20)
        self.start_button = Button(text="Начать игру", background_color=(0.5, 0.5, 0.5, 1), on_press=self.show_color_sequence_v2)
        self.add_widget(self.start_button)

        self.color_menu = BoxLayout(orientation='horizontal')
        for color in self.colors:
            color_button = Button(text=color, background_color=self.get_color_rgb(color),
                                  on_press=self.add_color_to_sequence)
            self.color_menu.add_widget(color_button)
        self.play_again_button = Button(text="Играть снова", on_press=self.play_again)
        self.exit_button = Button(text="Выход из игры", on_press=self.exit_game)
        self.easy = Button(text="Легкая", background_color=(0, 1, 0), on_press=self.easy_dif)
        self.mid = Button(text="Средняя", background_color=(1, 1, 0), on_press=self.mid_dif)
        self.hard = Button(text="Сложная", background_color=(1, 0, 0), on_press=self.hard_dif)

    def show_color_sequence_v2(self, instance):
        self.clear_widgets()
        self.add_widget(self.dif_label)
        self.add_widget(self.easy)
        self.add_widget(self.mid)
        self.add_widget(self.hard)

    def hard_dif(self, instance):
        self.clear_widgets()
        self.add_widget(self.sequence_label)
        self.create_hard_sequence()
        self.display_sequence()
        Clock.schedule_once(self.show_color_menu, len(self.correct_sequence) * 1.5)

    def mid_dif(self, instance):
        self.clear_widgets()
        self.add_widget(self.sequence_label)
        self.create_mid_sequence()
        self.display_sequence()
        Clock.schedule_once(self.show_color_menu, len(self.correct_sequence) * 1.5)
    def easy_dif(self, instance):
        self.clear_widgets()
        self.add_widget(self.sequence_label)
        self.create_easy_sequence()
        self.display_sequence()
        Clock.schedule_once(self.show_color_menu, len(self.correct_sequence) * 1.5)

    def show_color_sequence(self, instance):
        self.clear_widgets()
        self.create_sequence()
        self.display_sequence()
        Clock.schedule_once(self.show_color_menu, len(self.correct_sequence) * 1.5)  # Show color menu after sequence display duration

    def create_easy_sequence(self):
        for _ in range(4):
            color = random.choice(self.colors)
            self.correct_sequence.append(color)

    def create_mid_sequence(self):
        for _ in range(6):
            color = random.choice(self.colors)
            self.correct_sequence.append(color)

    def create_hard_sequence(self):
        for _ in range(8):
            color = random.choice(self.colors)
            self.correct_sequence.append(color)
    def display_sequence(self):
        for color in self.correct_sequence:
            button = ColoredButton(text=color, background_color=self.get_color_rgb(color))
            self.add_widget(button)

    def show_color_menu(self, dt):
        self.clear_widgets()

        self.new_sequence_label = Label(text="Наберите комбинацию", font_size=20)
        self.add_widget(self.new_sequence_label)
        self.add_widget(self.color_menu)

    def add_color_to_sequence(self, instance):
        color = instance.text
        self.user_sequence.append(color)
        if len(self.user_sequence) == len(self.correct_sequence):
            self.check_sequence()

    def check_sequence(self):
        if self.user_sequence == self.correct_sequence:
            self.display_result("Правильно!")
        else:
            self.display_result("Неправильно!")

    def display_result(self, result):
        self.remove_widget(self.new_sequence_label)
        self.remove_widget(self.color_menu)
        result_label = Label(text=result, font_size=20)
        self.add_widget(result_label)
        menu_layout = BoxLayout(orientation='vertical')
        menu_layout.add_widget(self.play_again_button)
        menu_layout.add_widget(self.exit_button)
        self.add_widget(menu_layout)

    def play_again(self, instance):
        self.clear_widgets()
        self.__init__()

    def exit_game(self, instance):
        App.get_running_app().stop()

    def get_color_rgb(self, color):
        color_map = {
            'красный': (1, 0, 0),
            'синий': (0, 0, 1),
            'зеленый': (0, 1, 0),
            'желтый': (1, 1, 0),
            'фиолетовый': (0.73, 0, 1),
            'оранжевый': (1, 0.53, 0),
            'розовый': (1, 0, 0.72),
            'голубой': (0, 1, 1),
            'коричневый': (0.48, 0.14, 0)
        }
        return color_map.get(color, (1, 1, 1, 1))  # Default color to white
    def coise_difficult(self, difficult):
        self.clear_widgets()
        self.add_widget(self.easy)
        self.add_widget(self.mid)
        self.add_widget(self.hard)
class ColoredButton(Button):
    def __init__(self, **kwargs):
        super(ColoredButton, self).__init__(**kwargs)

class MemoryGameApp(App):
    def build(self):
        return MemoryGame()

if __name__ == '__main__':
    MemoryGameApp().run()
