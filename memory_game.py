import os
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import random

english_colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'brown']
russian_colors = ['красный', 'синий', 'зеленый', 'желтый', 'фиолетовый', 'оранжевый', 'розовый', 'голубой',
                  'коричневый']


class LanguageButton(Button):
    def __init__(self, language, **kwargs):
        super(LanguageButton, self).__init__(**kwargs)
        self.language = language
        self.text = language


class MemoryGame(BoxLayout):
    def __init__(self, **kwargs):
        super(MemoryGame, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.colors = ['красный', 'синий', 'зеленый', 'желтый', 'фиолетовый', 'оранжевый', 'розовый', 'голубой',
                       'коричневый']
        self.correct_sequence = []
        self.user_sequence = []
        self.language = 'English'
        self.init_ui()

    def save_results(self, result):
        results_df = pd.DataFrame({
            'Result': [result]
        })
        results_df.to_csv('results.csv', mode='a', header=not os.path.exists('results.csv'), index=False)

    def init_ui(self):
        self.clear_widgets()
        self.intro_label = Label(text=self.get_text('intro'), font_size=30)
        self.add_widget(self.intro_label)

        self.sequence_label = Label(text=self.get_text('sequence'), font_size=20)
        self.dif_label = Label(text=self.get_text('difficulty'), font_size=20)
        self.start_button = Button(text=self.get_text('start'), background_color=(0.5, 0.5, 0.5, 1),
                                   on_press=self.show_color_sequence_v2)
        self.add_widget(self.start_button)

        if self.language == 'English':
            self.colors = english_colors
        elif self.language == 'Русский':
            self.colors = russian_colors

        self.color_menu = BoxLayout(orientation='horizontal')
        for color in self.colors:
            color_button = Button(text=color, background_color=self.get_color_rgb(color),
                                  on_press=self.add_color_to_sequence)
            self.color_menu.add_widget(color_button)
        self.play_again_button = Button(text=self.get_text('play_again'), on_press=self.play_again)
        self.exit_button = Button(text=self.get_text('exit'), on_press=self.exit_game)
        self.easy = Button(text=self.get_text('easy'), background_color=(0, 1, 0), on_press=self.easy_dif)
        self.mid = Button(text=self.get_text('mid'), background_color=(1, 1, 0), on_press=self.mid_dif)
        self.hard = Button(text=self.get_text('hard'), background_color=(1, 0, 0), on_press=self.hard_dif)

        self.language_label = Label(text=self.get_text('language'), font_size=20)
        self.add_widget(self.language_label)

        self.language_menu = BoxLayout(orientation='horizontal')
        self.english_button = LanguageButton(language='English', on_press=self.set_language)
        self.russian_button = LanguageButton(language='Русский', on_press=self.set_language)
        self.language_menu.add_widget(self.english_button)
        self.language_menu.add_widget(self.russian_button)
        self.add_widget(self.language_menu)

    def get_text(self, key):
        english_texts = {
            'intro': 'Welcome to the Memory Game',
            'sequence': 'Remember the sequence',
            'difficulty': 'Choose difficulty',
            'start': 'Start Game',
            'play_again': 'Play Again',
            'exit': 'Exit Game',
            'easy': 'Easy',
            'mid': 'Medium',
            'hard': 'Hard',
            'language': 'Choose Language'
        }
        russian_texts = {
            'intro': 'Добро пожаловать в игру "Memory Game"',
            'sequence': 'Запомните последовательность',
            'difficulty': 'Выберите сложность',
            'start': 'Начать игру',
            'play_again': 'Играть снова',
            'exit': 'Выход из игры',
            'easy': 'Легкая',
            'mid': 'Средняя',
            'hard': 'Сложная',
            'language': 'Выберите язык'
        }
        if self.language == 'English':
            return english_texts.get(key, '')
        elif self.language == 'Русский':
            return russian_texts.get(key, '')
        else:
            return ''

    def set_language(self, instance):
        self.language = instance.language
        self.init_ui()

    def show_color_sequence_v2(self, instance):
        self.clear_widgets()
        self.add_widget(self.dif_label)
        self.add_widget(self.easy)
        self.add_widget(self.mid)
        self.add_widget(self.hard)

    def hard_dif(self, instance):
        self.clear_widgets()
        self.add_widget(self.sequence_label)
        self.create_hard_sequence()  # Создание последовательности для сложной сложности
        self.display_sequence()  # Отображение последовательности
        Clock.schedule_once(self.show_color_menu, len(self.correct_sequence) * 1.5)

    def mid_dif(self, instance):
        self.clear_widgets()
        self.add_widget(self.sequence_label)
        self.create_mid_sequence()  # Создание последовательности для средней сложности
        self.display_sequence()  # Отображение последовательности
        Clock.schedule_once(self.show_color_menu, len(self.correct_sequence) * 1.5)

    def easy_dif(self, instance):
        self.clear_widgets()
        self.add_widget(self.sequence_label)
        self.create_easy_sequence()  # Создание последовательности для легкой сложности
        self.display_sequence()  # Отображение последовательности
        Clock.schedule_once(self.show_color_menu, len(self.correct_sequence) * 1.5)

    def show_color_sequence(self, instance):
        self.clear_widgets()
        self.create_sequence()  # Создание случайной последовательности цветов
        self.display_sequence()  # Отображение последовательности
        Clock.schedule_once(self.show_color_menu,
                            len(self.correct_sequence) * 1.5)  # Show color menu after sequence display duration

    def create_easy_sequence(self):
        for _ in range(4):  # Создание последовательности из 4 цветов для легкой сложности
            color = random.choice(self.colors)
            self.correct_sequence.append(color)

    def create_mid_sequence(self):
        for _ in range(6):  # Создание последовательности из 6 цветов для средней сложности
            color = random.choice(self.colors)
            self.correct_sequence.append(color)

    def create_hard_sequence(self):
        for _ in range(8):  # Создание последовательности из 8 цветов для сложной сложности
            color = random.choice(self.colors)
            self.correct_sequence.append(color)

    def display_sequence(self):
        for color in self.correct_sequence:
            button = ColoredButton(text=color, background_color=self.get_color_rgb(color))
            self.add_widget(button)

    def display_result(self, result):
        self.remove_widget(self.new_sequence_label)
        self.remove_widget(self.color_menu)
        result_label = Label(text=result, font_size=20)
        self.add_widget(result_label)
        menu_layout = BoxLayout(orientation='vertical')
        menu_layout.add_widget(self.play_again_button)
        menu_layout.add_widget(self.exit_button)
        self.add_widget(menu_layout)
        self.save_results(result)  # Вызов функции для сохранения результата

    def show_color_menu(self, dt):
        # Удалить все дочерние виджеты текущего меню
        self.clear_widgets()

        # Добавить новый заголовок для нового меню
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
            self.save_results("Правильно!")  # Сохранение результата
        else:
            self.display_result("Неправильно!")
            self.save_results("Неправильно!")  # Сохранение результата

    def display_result(self, result):
        self.remove_widget(self.new_sequence_label)
        self.remove_widget(self.color_menu)
        result_label = Label(text=result, font_size=20)
        self.add_widget(result_label)
        menu_layout = BoxLayout(orientation='vertical')
        menu_layout.add_widget(self.play_again_button)
        menu_layout.add_widget(self.exit_button)
        self.add_widget(menu_layout)

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
            'коричневый': (0.48, 0.14, 0),
            'red': (1, 0, 0),
            'blue': (0, 0, 1),
            'green': (0, 1, 0),
            'yellow': (1, 1, 0),
            'purple': (0.73, 0, 1),
            'orange': (1, 0.53, 0),
            'pink': (1, 0, 0.72),
            'cyan': (0, 1, 1),
            'brown': (0.48, 0.14, 0)
        }
        return color_map.get(color, (1, 1, 1, 1))  # Default color to white

    def play_again(self, instance):
        self.clear_widgets()
        self.__init__()

    def exit_game(self, instance):
        App.get_running_app().stop()


class ColoredButton(Button):
    def __init__(self, **kwargs):
        super(ColoredButton, self).__init__(**kwargs)

class MemoryGameApp(App):
    def build(self):
        return MemoryGame()


if __name__ == '__main__':
    MemoryGameApp().run()
