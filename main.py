from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.lang import Builder

# KV code string
kv_string = """
#:kivy 2.0.0

<WidgetsExample>:
    cols: 4
    ToggleButton:
        text: "START"
        on_state: root.on_toggle_button_state(self)
        size_hint: None, 1
        width: "110dp"
    Button:
        id: count_button
        text: "Count"
        on_press: root.on_button_click()
        disabled: not root.count_enabled
    Label:
        text: root.my_text
        font_size: "80dp"
    Label:
        id: counter_label  # Changed the ID to counter_label
        text: "0"
"""

# Load the KV code string
Builder.load_string(kv_string)

class WidgetsExample(GridLayout):
    my_text = StringProperty("1")
    timer_count = NumericProperty(0)  # Counter for the timer
    button_count = NumericProperty(0)  # Counter for the button
    count_enabled = BooleanProperty(False)
    timer_event = None  # To hold the timer event

    def on_start(self):
        pass

    def start_timer(self):
        self.timer_count = 0  # Reset the timer counter when the timer starts
        self.ids.counter_label.text = "0"
        if not self.timer_event:
            self.timer_event = Clock.schedule_interval(self.update_timer_label, 1)

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
            self.calculate_cps()

    def update_timer_label(self, *args):
        if self.count_enabled and self.timer_count < 15:
            self.timer_count += 1
            self.ids.counter_label.text = str(self.timer_count)
        elif self.timer_count == 15:
            self.stop_timer()
            self.count_enabled = False
            self.ids.count_button.disabled = True

    def calculate_cps(self):
        cps = self.button_count / 15
        self.ids.counter_label.text = f"CPS: {cps:.2f}"  # Update the timer label with CPS value

    def on_button_click(self):
        if self.count_enabled:
            self.button_count += 1
            self.my_text = str(self.button_count)  # Update the my_text attribute

    def on_toggle_button_state(self, widget):
        if widget.state == "normal":
            widget.text = "START"
            self.count_enabled = False
            self.stop_timer()
            self.ids.count_button.disabled = False
        else:
            widget.text = "IN PROGRESS"
            self.button_count = 0  # Reset the button counter when the timer starts
            self.my_text = "0"
            self.count_enabled = True
            self.ids.count_button.disabled = False
            self.start_timer()

class TheLabApp(App):
    def build(self):
        return WidgetsExample()

if __name__ == "__main__":
    TheLabApp().run()
