from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from datetime import datetime


class StopwatchApp(BoxLayout):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.icon = None
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None
        self.paused_time = None
        self.is_running = False
        self.is_paused = False
        self.filepath = "stopwatch_log.txt"

        self.output_label = Label(text="0:00:00", font_size=20)
        self.add_widget(self.output_label)

        self.start_button = Button(text="Start", on_press=self.start)
        self.add_widget(self.start_button)

        self.stop_button = Button(text="Stop", on_press=self.stop)
        self.stop_button.disabled = True
        self.add_widget(self.stop_button)

        self.pause_button = Button(text="Pause", on_press=self.pause)
        self.pause_button.disabled = True
        self.add_widget(self.pause_button)

        self.resume_button = Button(text="Resume", on_press=self.resume)
        self.resume_button.disabled = True
        self.add_widget(self.resume_button)

    def start(self, instance):
        if self.is_running:
            return

        self.is_running = True
        self.start_time = datetime.now()
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.pause_button.disabled = False
        Clock.schedule_interval(self.update_output, 1)

    def stop(self, instance):
        if not self.is_running:
            return

        self.is_running = False
        self.is_paused = False
        self.end_time = datetime.now()
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.pause_button.disabled = True
        self.resume_button.disabled = True
        self.save_log()
        Clock.unschedule(self.update_output)

    def pause(self, instance):
        if not self.is_running or self.is_paused:
            return

        self.is_paused = True
        self.paused_time = datetime.now()
        self.elapsed_time += self.paused_time - self.start_time
        self.pause_button.disabled = True
        self.resume_button.disabled = False
        Clock.unschedule(self.update_output)

    def resume(self, instance):
        if not self.is_paused:
            return

        self.is_paused = False
        self.start_time += (datetime.now() - self.paused_time)
        self.pause_button.disabled = False
        self.resume_button.disabled = True
        Clock.schedule_interval(self.update_output, 1)

    def update_output(self, dt):
        if not self.is_running:
            return

        if not self.is_paused:
            self.elapsed_time = datetime.now() - self.start_time
        time_string = "{:02}:{:02}:{:02}".format(self.elapsed_time.seconds // 3600,
                                                 (self.elapsed_time.seconds // 60) % 60, self.elapsed_time.seconds % 60)
        self.output_label.text = time_string

    def save_log(self):
        with open(self.filepath, "w") as f:
            f.write("Start Time: " + str(self.start_time) + "\n")
            f.write("End Time: " + str(self.end_time) + "\n")
            f.write("Elapsed Time: " + str(self.elapsed_time) + "\n")


class StopwatchAppApp(App):
    def build(self):
        self.icon = "stopwatch.png"
        return StopwatchApp()


if __name__ == "__main__":
    StopwatchAppApp().run()
