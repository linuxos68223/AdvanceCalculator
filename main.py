import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from math import sin, cos, tan, log, sqrt, radians, pi, e

Window.clearcolor = (0.1, 0.1, 0.2, 1)  # Premium look

USER_MANUAL = """
Welcome to the Premium Scientific Calculator!

Features:
- Basic operations: +, -, ×, ÷
- Scientific: sin, cos, tan, log, sqrt, ^, pi, e
- Use 'sin(45)' for angle in degrees, or 'sin(pi/2)' for radians
- Use ^ for power, e.g., 2^3
- Press 'C' to clear, '<-' to backspace, '=' to evaluate

Tip: Tap functions/buttons to enter them. All input is shown above.

Enjoy premium calculation experience!
"""

class Calculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.manual_shown = False

        # Top bar with Help button
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.13))
        self.display = TextInput(font_size=32, halign='right', readonly=True, background_color=(0.15,0.15,0.25,1))
        top_bar.add_widget(self.display)

        help_btn = Button(text='Help', font_size=20, size_hint=(0.2, 1), background_color=(0.14,0.26,0.36,1))
        help_btn.bind(on_press=self.show_manual)
        top_bar.add_widget(help_btn)
        self.add_widget(top_bar)

        buttons = [
            ['7', '8', '9', '/', 'sin', 'cos'],
            ['4', '5', '6', '*', 'tan', 'log'],
            ['1', '2', '3', '-', 'sqrt', '^'],
            ['0', '.', 'pi', '+', 'e', '<-'],
            ['C', '(', ')', '=', '', '']
        ]

        grid = GridLayout(cols=6, spacing=3, size_hint=(1, 0.8))
        for row in buttons:
            for text in row:
                if text:
                    btn = Button(text=text, font_size=24, background_color=(0.22,0.22,0.33,1))
                    btn.bind(on_press=self.on_button)
                    grid.add_widget(btn)
                else:
                    grid.add_widget(Label())
        self.add_widget(grid)

        self.show_manual_once()

    def show_manual_once(self):
        if not self.manual_shown:
            self.show_manual()
            self.manual_shown = True

    def show_manual(self, *args):
        popup = Popup(title='User Manual',
                      content=Label(text=USER_MANUAL, font_size=18),
                      size_hint=(0.85, 0.65))
        popup.open()

    def on_button(self, instance):
        text = instance.text
        if text == 'C':
            self.display.text = ""
        elif text == '<-':
            self.display.text = self.display.text[:-1]
        elif text == '=':
            try:
                expr = self.display.text.replace('^', '**')
                expr = expr.replace('pi', str(pi)).replace('e', str(e))
                for fun in ['sin', 'cos', 'tan', 'log', 'sqrt']:
                    expr = expr.replace(fun, f'{fun}')
                allowed = {'sin':lambda x: sin(radians(x)), 'cos':lambda x: cos(radians(x)),
                           'tan':lambda x: tan(radians(x)), 'log':log, 'sqrt':sqrt,
                           'pi':pi, 'e':e}
                result = eval(expr, {"__builtins__": None}, allowed)
                self.display.text = str(result)
            except Exception:
                self.display.text = "Error"
        else:
            self.display.text += text

class SciCalcApp(App):
    def build(self):
        self.title = 'Premium Scientific Calculator'
        return Calculator()

if __name__ == '__main__':
    SciCalcApp().run()