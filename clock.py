import tkinter as tk
import math
from winsound import PlaySound, SND_FILENAME, SND_ASYNC, SND_LOOP, SND_PURGE
import datetime


class Element():
    def __init__(self, params):
        self.canvas = params['canvas']
        self.size = params['size']
        self.panel = params['panel']
        self.calculate_center()
        self.id = 0

    # ----------------------Service Methods-----------------------
    def calculate_center(self):
        self.x = int(self.canvas['width']) // 2
        self.y = (int(self.canvas['height']) - self.panel) // 2

    def get_position(self, angle, length):
        _angle = math.radians(angle)
        x = self.x + length * math.cos(_angle)
        y = self.y + length * math.sin(_angle)
        return x, y

    def do_resize(self, new_size, canvas):
        self.size = new_size
        self.canvas = canvas
        self.calculate_center()
        self.resize()

    # -----------------------Abstract Methods---------------------
    def create(self):
        pass

    def render(self):
        pass


class Line(Element):
    def __init__(self, params, **kwargs):
        super().__init__(params)
        self.angle = kwargs.get('angle') or 0
        self.mult = kwargs.get('mult') or 0
        self.length = self.calculate_length()
        self.delta = kwargs.get('delta')
        self.width = kwargs['width']
        self.color = kwargs.get('color') or 'black'
        self.create()

    def calculate_length(self):
        return self.size * self.mult

    def get_coords(self):
        if self.delta is None:
            x2, y2 = self.get_position(self.angle, self.length)
            return self.x, self.y, x2, y2
        x1, y1 = self.get_position(self.angle, self.size - self.delta)
        x2, y2 = self.get_position(self.angle, self.size - self.delta - 5)
        return x1, y1, x2, y2

    def create(self):
        self.id = self.canvas.create_line(
            self.get_coords(), width=self.width, fill=self.color)

    def render(self):
        if self.delta is None:
            self.canvas.coords(self.id, self.get_coords())


class Oval(Element):
    def __init__(self, params, **kwargs):
        super().__init__(params)
        self.width = kwargs.get('width')
        self.color = kwargs.get('color') or 'black'
        self.angle = kwargs.get('angle')
        self.delta = kwargs.get('delta') or 0
        self.create()

    def create(self):
        if self.angle is None:
            self.id = self.canvas.create_oval(
                self.x - self.width, self.y - self.width,
                self.x + self.width, self.y + self.width, fill=self.color)
        else:
            x, y = self.get_position(self.angle, self.size - self.delta)
            self.id = self.canvas.create_oval(
                x - self.width, y - self.width,
                x + self.width, y + self.width, fill=self.color)


class Text(Element):
    def __init__(self, params, **kwargs):
        super().__init__(params)
        self.is_time = kwargs.get('is_time') or False
        self.angle = kwargs.get('angle')
        self.text = kwargs.get('text')
        self.x1 = kwargs.get('x1') or 0
        self.y1 = kwargs.get('y1') or 0
        self.delta = kwargs.get('delta') or 0
        self.create()

    def create(self):
        if not self.is_time:
            x, y = self.get_position(self.angle, self.size + self.delta)
            self.id = self.canvas.create_text(
                x, y, text=self.text, justify=tk.CENTER, font="Consolas 25")
        else:
            self.id = self.canvas.create_text(
                self.x1, self.y1, text=self.text,
                justify=tk.CENTER, font="Consolas 18")

    def render(self):
        if self.is_time:
            self.canvas.itemconfigure(self.id, text=self.text)


class Widget(Element):
    def __init__(self, params, **kwargs):
        super().__init__(params)
        self.type_ = kwargs.get('type') or 'image'
        self.width = kwargs.get('width') or 0
        self.x1 = kwargs.get('x1')
        self.y1 = kwargs.get('y1')
        self.left = kwargs.get('left') or False
        self.get_deltas()
        self.widget = kwargs.get('widget')
        self.create()

    def get_deltas(self):
        if self.x1 is None or self.y1 is None:
            return
        if self.left:
            self.deltaX = self.x1
        else:
            self.deltaX = self.x * 2 - self.x1
        self.deltaY = self.y * 2 - self.y1

    def create(self):
        if self.type_ == 'rect':
            self.id = self.canvas.create_rectangle(
                5, 5, self.x * 2 - 5, self.y * 2 - 5, width=self.width)

        elif self.type_ == 'window':
            self.id = self.canvas.create_window(
                self.x1, self.y1, window=self.widget)
        else:
            self.id = self.canvas.create_image(
                self.x1, self.y1, image=self.widget)


class Application(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # -----------------Variables-----------------------------
        self.clock_size = 170
        self.panel = 55
        self.time = datetime.datetime.now()
        self.sound = False
        self.alarm = False
        self.is_alarm = False
        self.oldHours = '00'
        self.oldMinutes = '00'
        self.hours = tk.StringVar()
        self.minutes = tk.StringVar()

        # ------------------Widgets------------------------------
        self.canvas = tk.Canvas(root, width=self.clock_size * 2.5,
                                height=self.clock_size * 2.5 + self.panel,
                                bg="white")
        self.canvas.bind("<Button-1>", self.set_alarm_by_arrow)
        self.canvas.pack()

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

        self.s1 = tk.Spinbox(self.canvas, font="Consolas 20",
                             width=2, values=self.get_values(12), wrap=True,
                             textvariable=self.hours)
        self.s2 = tk.Spinbox(self.canvas, font="Consolas 20",
                             width=2, values=self.get_values(60), wrap=True,
                             textvariable=self.minutes)

        # -------------------Elements----------------------------
        self.params = {'canvas': self.canvas,
                       'size': self.clock_size,
                       'panel': self.panel}

        self.arrow3 = Line(self.params, mult=0.5, width=9)
        self.arrow2 = Line(self.params, mult=0.8, width=5)
        self.arrow4 = Line(self.params, mult=0.8, width=3, color='yellow',
                           angle=90)
        self.arrow1 = Line(self.params, mult=0.8, width=3, color='red')

        self.hours.trace('w', lambda *args: self.set_alarm_by_time())
        self.minutes.trace('w', lambda *args: self.set_alarm_by_time())
        self.hours.set('06')
        self.minutes.set('00')

        self.time_string = Text(self.params, is_time=True,
                                text=self.time.strftime('%H:%M:%S'),
                                x1=120, y1=450)

        self.btn_sound = Widget(self.params, x1=35, y1=450,
                                widget=self.canvas.sound, left=True)
        self.btn_alarm = Widget(self.params, x1=290, y1=450,
                                widget=self.canvas.alarm_on)

        self.canvas.tag_bind(self.btn_sound.id, "<Button-1>",
                             self.toggle_sound)
        self.canvas.tag_bind(self.btn_alarm.id, "<Button-1>",
                             self.toggle_alarm)

        self.elems = [self.arrow3, self.arrow2, self.arrow4, self.arrow1,
                      self.time_string, self.btn_sound, self.btn_alarm]

        ids = []
        ids.append(Oval(self.params, width=6))
        ids.append(Widget(self.params, type='rect', width=2))

        hours = 0
        for i, angle in enumerate(range(-60, 300, 6)):
            if abs(angle) % 30 == 0:
                ids.append(Text(self.params, angle=angle,
                                text=str(hours + 1), delta=10))
                hours += 1
                ids.append(Line(self.params, angle=angle, width=3, delta=30))

            ids.append(Oval(self.params, angle=angle, width=1,
                            delta=30))

        ids.append(Widget(self.params, x1=340, y1=450, widget=self.s1,
                          type='window'))
        ids.append(Widget(self.params, x1=390, y1=450, widget=self.s2,
                          type='window'))

        self.elems += ids

        # -------------------------Start----------------------------
        self.calculate_center()
        self.tick()

    # ---------------------Service methods--------------------------
    def calculate_center(self):
        self.x = int(self.canvas['width']) // 2
        self.y = (int(self.canvas['height']) - self.panel) // 2

    def toggle_sound(self, event):
        self.sound = not self.sound
        if self.sound:
            self.canvas.itemconfig(self.btn_sound.id, image=self.canvas.mute)
        else:
            self.canvas.itemconfig(self.btn_sound.id, image=self.canvas.sound)

    def toggle_alarm(self, event):
        self.alarm = not self.alarm
        if self.alarm:
            self.canvas.itemconfig(self.btn_alarm.id,
                                   image=self.canvas.alarm_off)
        else:
            self.canvas.itemconfig(self.btn_alarm.id,
                                   image=self.canvas.alarm_on)
        if self.is_alarm:
            self.is_alarm = False
            PlaySound(None, SND_PURGE)

    def get_values(self, num):
        return ['{:0>2}'.format(str(i)) for i in range(num)]

    def validate_time(self):
        if self.hours.get() == '':
            self.hours.set(self.oldHours)
        if len(self.hours.get()) > 2:
            self.hours.set(self.hours.get()[:2])
        if [i for i in self.hours.get()[:2] if not i.isdigit()]:
            self.hours.set(self.oldHours)

        if int(self.hours.get()[:2]) > 24:
                self.hours.set(self.oldHours)

        if self.minutes.get() == '':
            self.minutes.set(self.oldMinutes)
        if [i for i in self.minutes.get()[:2] if not i.isdigit()]:
            self.minutes.set(self.oldMinutes)
        if len(self.minutes.get()) > 2:
            self.minutes.set(self.minutes.get()[0:2])

        if int(self.minutes.get()[:2]) > 59:
            self.minutes.set(self.oldMinutes)

    # ---------------------Alarm methods------------------------
    def set_alarm_by_time(self):
        self.validate_time()
        try:
            hours = int(self.hours.get())
        except ValueError:
            hours = 0
        try:
            minutes = int(self.minutes.get()) // 2
        except ValueError:
            minutes = 0
        self.arrow4.angle = hours % 12 * 30 - 90 + minutes
        self.oldHours = '{:0>2}'.format(self.hours.get())
        self.oldMinutes = '{:0>2}'.format(self.minutes.get())

        self.arrow4.render()
        root.focus()

    def check_area(self, y):
        if y >= self.y * 2 - 5:
            return False
        return True

    def set_alarm_by_arrow(self, event):
        if self.check_area(event.y):
            radians = math.atan2(event.y - self.y, event.x - self.x)
            self.arrow4.angle = math.degrees(radians)

            self.arrow4.render()
            self.calculate_alarm_time()

    def calculate_alarm_time(self):
        angle = self.arrow4.angle + 90
        time_ = (angle if angle >= 0 else 360 + angle) / 30
        hours = int(time_)
        minutes = time_ - int(time_)

        self.hours.set('{:0>2}'.format(str(hours)))
        self.minutes.set('{:0>2}'.format(str(int(60 * minutes))))

    # ----------------------Time methods----------------------------
    def set_angle(self):
        self.arrow1.angle = int(self.time.second) * 6 - 90
        self.arrow2.angle = int(self.time.minute) * 6 - 90
        self.arrow3.angle = int(self.time.hour) * 30 - 90 \
            + (int(self.time.minute) // 2)

    def do_tick(self):
        self.time += datetime.timedelta(seconds=1)
        self.tick()

    def tick(self):
        self.set_angle()
        self.time_string.text = self.time.strftime('%H:%M:%S')
        self.render()
        self.canvas.after(1000, self.do_tick)

        if self.sound:
            PlaySound("tick.wav", SND_FILENAME | SND_ASYNC)

        if self.alarm and not self.is_alarm:
            test_angle = int(self.arrow4.angle
                if self.arrow4.angle >= 0 else self.arrow4.angle + 360)

            if test_angle == self.arrow3.angle % 360:
                self.is_alarm = True

        if self.is_alarm:
            PlaySound("alarm.wav", SND_FILENAME | SND_LOOP | SND_ASYNC)

    # --------------------Render method----------------------------
    def render(self):
        for elem in self.elems:
            elem.render()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Alarm Clock')
    root.resizable(False, False)
    Application(root)
    root.mainloop()
