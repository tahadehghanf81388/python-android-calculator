"""
Calculator App for Android
Built with Kivy and Python
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


class CalculatorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Python Calculator"
        self.equation = ""
        self.history = []
    
    def build(self):
        # تنظیم رنگ زمینه
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        
        # لایه اصلی
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # عنوان
        title_label = Label(
            text="Python Calculator",
            font_size=28,
            size_hint=(1, 0.1),
            color=(0, 0.8, 1, 1)
        )
        main_layout.add_widget(title_label)
        
        # نمایشگر
        self.display = TextInput(
            text='0',
            multiline=False,
            readonly=True,
            halign='right',
            font_size=48,
            size_hint=(1, 0.15),
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        main_layout.add_widget(self.display)
        
        # لایه دکمه‌ها
        buttons_grid = GridLayout(cols=4, spacing=8, size_hint=(1, 0.7))
        
        # لیست دکمه‌ها
        buttons = [
            ('C', 'red'), ('(', 'orange'), (')', 'orange'), ('/', 'orange'),
            ('7', 'gray'), ('8', 'gray'), ('9', 'gray'), ('*', 'orange'),
            ('4', 'gray'), ('5', 'gray'), ('6', 'gray'), ('-', 'orange'),
            ('1', 'gray'), ('2', 'gray'), ('3', 'gray'), ('+', 'orange'),
            ('⌫', 'red'), ('0', 'gray'), ('.', 'gray'), ('=', 'green')
        ]
        
        # ایجاد دکمه‌ها
        for text, color in buttons:
            btn = CalculatorButton(
                text=text,
                button_color=color,
                font_size=32
            )
            btn.bind(on_press=self.on_button_press)
            buttons_grid.add_widget(btn)
        
        main_layout.add_widget(buttons_grid)
        
        # نمایش آخرین نتیجه
        self.result_label = Label(
            text="",
            font_size=20,
            size_hint=(1, 0.05),
            color=(0.7, 0.7, 0.7, 1)
        )
        main_layout.add_widget(self.result_label)
        
        return main_layout
    
    def on_button_press(self, instance):
        current_text = self.display.text
        button_text = instance.text
        
        if button_text == 'C':
            # پاک کردن همه چیز
            self.display.text = '0'
            self.equation = ""
            self.result_label.text = ""
            
        elif button_text == '⌫':
            # حذف آخرین کاراکتر
            if current_text != '0' and current_text != 'Error':
                new_text = current_text[:-1]
                self.display.text = new_text if new_text else '0'
                self.equation = self.equation[:-1]
        
        elif button_text == '=':
            try:
                # ارزیابی عبارت
                expression = self.equation.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                self.result_label.text = f"{self.equation} = {result}"
                
                # ذخیره در تاریخچه
                self.history.append(f"{self.equation} = {result}")
                if len(self.history) > 10:
                    self.history.pop(0)
                
                # نمایش نتیجه
                self.display.text = str(result)
                self.equation = str(result)
                
            except ZeroDivisionError:
                self.display.text = "Error: Division by zero"
                self.equation = ""
            except Exception as e:
                self.display.text = "Error"
                self.equation = ""
        
        else:
            # اضافه کردن کاراکتر جدید
            if current_text == '0' or current_text == 'Error':
                self.display.text = button_text
                self.equation = button_text
            else:
                # برای نمایش زیباتر
                display_char = button_text
                if button_text == '*':
                    display_char = '×'
                elif button_text == '/':
                    display_char = '÷'
                
                self.display.text = current_text + display_char
                self.equation = self.equation + button_text


class CalculatorButton(Button):
    def __init__(self, button_color='gray', **kwargs):
        super().__init__(**kwargs)
        self.button_color = button_color
        self.set_color()
    
    def set_color(self):
        """تنظیم رنگ دکمه"""
        color_map = {
            'gray': (0.3, 0.3, 0.35, 1),
            'orange': (1, 0.6, 0, 1),
            'red': (1, 0.2, 0.2, 1),
            'green': (0.2, 0.8, 0.2, 1)
        }
        
        color = color_map.get(self.button_color, (0.3, 0.3, 0.35, 1))
        self.background_color = color
        self.background_normal = ''
        
        # سایه برای دکمه
        with self.canvas.before:
            Color(color[0]*0.8, color[1]*0.8, color[2]*0.8, 1)
            Rectangle(pos=(self.x+2, self.y-2), size=self.size)


if __name__ == '__main__':
    CalculatorApp().run()
