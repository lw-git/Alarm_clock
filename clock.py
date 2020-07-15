import tkinter as tk
import math
from winsound import PlaySound, SND_FILENAME, SND_ASYNC, SND_LOOP, SND_PURGE
import datetime


class Application(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # -----------------Variables-----------------------------
        self.angle = 0
        self.angle2 = 0
        self.angle3 = 0
        self.angle4 = 90
        self.id = 0
        self.id2 = 0
        self.id3 = 0
        self.id4 = 0
        self.oval = 0
        self.clock_size = 170
        self.time = datetime.datetime.now()
        self.sound = False
        self.alarm = False
        self.is_alarm = False
        self.panel = 55        

        # ------------------Widgets------------------------------
        self.canvas = tk.Canvas(root, width=self.clock_size * 2.5,
                                height=self.clock_size * 2.5 + self.panel,
                                bg="white")
        self.canvas.bind("<Button-1>", self.alarm_arrow)
        self.canvas.pack()
        self.calculate_center()

        self.canvas.mute = tk.PhotoImage(data='''R0lGODlhMgAyAPAAAAAAAAAAACH5BAEAAAAALAAAAAAyADIAAALVhI+py+0Po5y02ouz3lyFH3QZ+IkXWTqgeaDpQjZv5YaJy6An3vKeP6kZaracjsYTqo4UJVAWQx6ZwxUiCo06rT1udXbbTs
        FAbJj41RavZnMXDXAaue40XJlde99EG37OBhbXp0b181JHOGYYWJSoWFjXFXgImfL3Rnlmefk0iLj3ydlpiPU4avXndYpKGqm52eqXpBcqKjs71TiHy0dm6zvaSCcJARnrOkJYmbqG0QfjqQHH
        LDgtbWd9DZztzFEczPJpzCi+xG0erZ3O3u7+Dh8vr1EAADs=''')

        self.canvas.sound = tk.PhotoImage(data='''R0lGODlhMgAyAPZjAAEBAQICAgMDAwQEBAUFBQYGBggICAkJCQoKCgsLCwwMDA0NDQ4ODg8PDxAQ\nEBERERISEhQUFBcXFxsbGxwcHCAgICMjIyUlJSgoKCkpKSoqKisrKywsLC0tLS4uLjU1NT
        k5OURE\nREZGRkpKSk9PT1NTU1dXV1hYWF5eXmNjY2ZmZmdnZ2hoaGlpaWpqam1tbW5ubnFxcXZ2dn5+foSE\nhIqKio2NjZOTk5aWlpmZmZqamqOjo6ampqioqKysrLCwsLe3t7u7u7+/v8HBwcXF
        xcrKysvLy8zM\nzM3Nzc7Ozs/Pz9TU1NjY2NnZ2dra2t/f3+Hh4eLi4ufn5+jo6Onp6evr6+7u7vHx8fPz8/T09PX1\n9fb29vf39/n5+fr6+vv7+/z8/P39/f7+/v///wAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5\nBAAAAAAALAAAAAAyADIAAAf+gGOCg4SFhoeIiYqLjI2Oj5CRkpOU
        lZaXmJmamFtEjlubhTkPDwSL\nUKQtoYIapKSLLa5doRSur4uuC5sLtreKW64gmby9D4dBC6aCF66XwMW+hAnNgq4alUDQ1IUWsoIl\n25Eq2uGEpAsJg64ykhLk5YNMrqBjH/A4Ifn6+8TvxmNVSP
        EYNO0BAEHP/g0y4a/hLXu+hmwjpmpQ\nB4cNBXVx9UIdqR6CJpwjdBHju0GtHugSBIDaEl4rBZU0qc2cryMjq0WbSbOYzQc1PCqcZ7EntJhj\nWj64pnMoqSdFjfocRIKUsjFExxA7ElWqLUI2SKVr
        ekVQQSFdvUaLYVUoPWKvRdKqJaR0gtBZWEkx\nkeuVEDF2TYWWlan2q1tBUnLmVTiG51xBI7YpHWslnOO+TS0IpUH4wVhBbAvfkrEtoC9iIQoducG6\nteuC/gRV4aViELHP3iDBJpfIFdQx46I9Ch
        H7ELGYxJhK2nHSEENSXMf4gAdJXk1DBa8atnS90A+V\ng1BQn7RbOCJXBzUR6MWo3yqei0YJXDVmRltFiQ3Sl92RUZfo+wUo4IAEFmjggfQFAgA7'
        ''')

        self.canvas.alarm_off = tk.PhotoImage(data='''R0lGODlhMgAyAPeRABQUFBcXFxgYGBkZGRoaGhsbGxwcHB0dHR4eHh8fHyAgICEhISIiIiMjIyQk\nJCUlJSYmJicnJygoKCkpKSsrKywsLC0tLS4uLi8vLzIyMjMzMzc3Nzg4ODk5OTo6Ojw8PD
        4+PkBA\nQEZGRkdHR0hISEpKSktLS01NTU9PT1BQUFJSUlVVVVZWVldXV1hYWFlZWVpaWltbW15eXmBgYGJi\nYmdnZ2hoaGtra21tbW9vb3BwcHFxcXJycnd3d3l5eXp6ent7e4CAgIGBgYKCgoOD
        g4SEhIWFhYaG\nhoeHh4mJiYqKio2NjY6Ojo+Pj5CQkJGRkZaWlpeXl5iYmJ2dnZ+fn6GhoaKioqSkpKWlpa2tra6u\nrrCwsLGxsbKysrOzs7W1tbe3t7m5ub29vb6+vr+/v8DAwMHBwcXFxcbGxs
        jIyMnJycrKys7Ozs/P\nz9DQ0NLS0tTU1NXV1dbW1tfX19nZ2dzc3N3d3d7e3uDg4OHh4eLi4uPj4+bm5ufn5+jo6Onp6erq\n6uzs7O3t7e7u7u/v7/Dw8PHx8fLy8vT09PX19fb29vf39/r6+vv7
        +/z8/P39/f7+/v///wAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAACH5BAAAAAAALAAAAAAyADIA\nAAj+ACMJHEiwoMGDCBMqXMiwocOHBxsZlBiJIsSGFgVmXLjx4sRIhJCwkIElYQ4VJwh19GgQDwYG\nDx4YkNGRigEDUBqtZEkQBoOfDxgY
        qFIQD8wTPCNWrNgoQMygQWFoFHjiJ56kC+kYgArzAQhEA6Hc\nJIoVoRYQBLrGhMmAgIw4dgwwkFrWICIYW4OyVRuTgAeYV+sOlEiC7dPDP9US0CK4oJCtahMfXsuA\nRmOCf/IaRrz3gQRDZZY2Tg
        J0LeKnPw18wUPgzeVGHkx3LR3ZRqSqQnZ6NJQWqmnKejEYEvuAxGUy\nBHwbjvyAQBk7QA1chsJ3tt6YBnJEEtE1wJ/GQjr++0asodETzQbUNM7BnGtXAmroJO9qgHFZiTC4\nTt7rIxII2gxI0Vhh
        qEm21gaNIJGXXgww0Vhs4/1GQBtvaMYVEo0tZ11QQkTyl2wx7XCfQE7xRRkI\nkfhg4HUsCGZHcsrRF4ca840HkweCcSGXfkEZwEQjGjCnmG4PhVddTCJEwsOOv+k1YV0kcIadHWUs\nuBxqDmJFCI
        ybGSCFIRqgptxhxnmkk0CkNckAUjbQJuZ1BMRBZEKN/HGaXniEweR1wLHVIkQUNVKV\nm0MZIsFmb4rpo0d4EHjdTy3SoCGIQL3nw5wEMWHlb31wAeObJpYWFAZoNNQHl8DVZyeIBY7JoFeO\nDZGx
        o4EMyBCJT3slliuDosrUEB1CICFEsArG9IcdQAwrLBLLBquss8w666xoDyEh1BeXedRGWjUQ\n9EYAuur6QLYa/YWBShI1wlqlqG1AboptkUGQREGK+RMPjVFURgAEaGeQp+559p1gFKHxBReGIARF
        \nb0FJ0Ma7U30UCR5M2MADFWdCrPHGHHfsMUsBAQA7''')

        self.canvas.alarm_on = tk.PhotoImage(data='''R0lGODlhMgAyAPZiABcXFxgYGBkZGRoaGhsbGxwcHB0dHR4eHh8fHyAgICEhISIiIiMjIyQkJCUl\nJScnJzIyMjMzMzQ0NDY2Njc3Nzw8PD4+PkFBQUJCQkVFRVBQUFNTU11dXV5eXmBgYGFhYW
        JiYmZm\nZmhoaGpqam5ubm9vb3BwcHNzc3V1dXd3d3l5eXp6en19fX5+foODg4SEhIWFhYmJiY2NjY6OjpOT\nk5aWlpiYmJqamp2dnaCgoKSkpKampqysrLCwsLGxsbOzs7S0tLW1tba2tri4uL6+
        vsbGxsfHx8jI\nyMrKys3NzdLS0tPT09TU1NjY2NnZ2dvb29zc3N/f3+Li4uPj4+bm5u3t7e7u7vDw8PLy8vPz8/T0\n9PX19fn5+fr6+vv7+/z8/P39/f7+/v///wAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5\nBAAAAAAALAAAAAAyADIAAAf+gGKCg4SFhoeIiYqLjI2Oj5CRkFyF
        lJKXiFMrGyJCmJ+DRwkNDQkD\nLpagk2ITo6QNA0Wqkk0Dr6UNK4Ops4apPa63IZS8vYSWNhMGt68JBiRTxpkXy8ykrgkJPdKFVq3W\n4LCegsWgHMHhzAlU5MZHy+jp1ybcXCLx8q8DW9Jc+PnXck
        h7BzBcCmk0/hW8IG1FwXAGpHF4CA7A\nFWMZFAIc0MQYBIrWYhnTCNDAuFnVQDYTCIrSFVsqb9HoxQRmTFIsevVIeZNDrxkkAULo9eHmrX2q\nuBi9ZWCbpFQEl5KiB+qe1GtWPimxeRObrkverh49
        +UjJN7GuDNSAZMJA0JtrBix0ZESEq1hrIRrV\ncHsN1zVsfrM1awY4AUNGRVzAWOxCMWMYjRdLhvzYMWXKim2IKcet86IdbrFlS6DBc6Kd4XyaPnSF\n5ysDOFYjigHvFgXOssWkGDDKmYUouX0JYg
        KDRAoewZMrX858eSAAOw==''')

        self.btn_sound = self.canvas.create_image(
            35, self.y * 2 + 30, image=self.canvas.sound)
        self.btn_alarm = self.canvas.create_image(
            self.x * 2 - 35, self.y * 2 + 30, image=self.canvas.alarm_on)

        self.canvas.tag_bind(self.btn_sound, "<Button-1>", self.toggle_sound)
        self.canvas.tag_bind(self.btn_alarm, "<Button-1>", self.toggle_alarm)

        self.canvas.create_rectangle(
            5, 5, self.x * 2 - 5, self.y * 2 - 5, width=2)

        # ---------------First render and start------------------
        self.first_render()
        self.tick()

    # ---------------------Service methods--------------------------
    def calculate_center(self):
        self.x = int(self.canvas['width']) // 2
        self.y = (int(self.canvas['height']) - self.panel) // 2

    def get_position(self, angle):
        _angle = math.radians(angle)
        x = self.x + self.clock_size * math.cos(_angle)
        y = self.y + self.clock_size * math.sin(_angle)
        return x, y

    def toggle_sound(self, event):
        self.sound = not self.sound
        if self.sound:
            self.canvas.itemconfig(self.btn_sound, image=self.canvas.mute)
        else:
            self.canvas.itemconfig(self.btn_sound, image=self.canvas.sound)

    def toggle_alarm(self, event):
        self.alarm = not self.alarm
        if self.alarm:
            self.canvas.itemconfig(self.btn_alarm,
                                   image=self.canvas.alarm_off)
        else:
            self.canvas.itemconfig(self.btn_alarm,
                                   image=self.canvas.alarm_on)
        if self.is_alarm:
            self.is_alarm = False
            PlaySound(None, SND_PURGE)

    # ----------------------Alarm methods---------------------------
    def alarm_arrow(self, event):
        if event.y >= self.y * 2 - 5:
            return
        radians = math.atan2(event.y - self.y, event.x - self.x)
        self.angle4 = math.degrees(radians)
        self.canvas.delete(self.id4)
        self.create_new_line(150, 3, self.angle4, color='yellow', id=4)
        self.create_oval()

    # ----------------------Time methods----------------------------
    def set_angle(self):
        self.angle = int(self.time.second) * 6 - 90
        self.angle2 = int(self.time.minute) * 6 - 90
        self.angle3 = int(self.time.hour) * 30 - 90 \
            + (int(self.time.minute) // 2)

    def do_tick(self):
        self.time += datetime.timedelta(seconds=1)
        self.tick()

    def tick(self):
        self.set_angle()
        self.render()
        self.canvas.after(1000, self.do_tick)

        if self.sound:
            PlaySound("tick.wav", SND_FILENAME | SND_ASYNC)

        if self.alarm and not self.is_alarm:
            test_angle = int(self.angle4 if self.angle4 >= 0
                             else self.angle4 + 360)

            if test_angle == self.angle3 % 360:
                self.is_alarm = True

        if self.is_alarm:
            PlaySound("alarm.wav", SND_FILENAME | SND_LOOP | SND_ASYNC)

    # --------------------Render methods----------------------------
    def create_oval(self):
        self.canvas.delete(self.oval)
        self.oval = self.canvas.create_oval(
            self.x - 6, self.y - 6, self.x + 6, self.y + 6, fill='black')

    def first_render(self):
        for i, angle in enumerate(range(-60, 300, 30)):
            x, y = self.get_position(angle)
            self.canvas.create_text(
                x, y, text=str(i + 1), justify=tk.CENTER, font="Consolas 25")

        self.create_new_line(150, 5, self.angle2, id=2)
        self.create_new_line(80, 9, self.angle3, id=3)
        self.create_new_line(150, 3, self.angle, color='red')
        self.create_new_line(150, 3, self.angle4, id=4, color='yellow')
        self.create_oval()

    def render(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.id2)
        self.canvas.delete(self.id3)

        self.create_new_line(150, 5, self.angle2, id=2)
        self.create_new_line(80, 9, self.angle3, id=3)
        self.create_new_line(150, 3, self.angle, color='red')
        self.create_oval()

    def create_new_line(self, length, width, angle_, color='black', id=''):
        angle = math.radians(angle_)
        end_x = self.x + length * math.cos(angle)
        end_y = self.y + length * math.sin(angle)
        setattr(self, 'id' + str(id), self.canvas.create_line(
            self.x, self.y, end_x, end_y, width=width, fill=color))


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Clock')
    root.resizable(False, False)
    Application(root)
    root.mainloop()
