import tkinter as tk
import datetime
import math


class Application(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # -----------------Variables-----------------------------
        self.angle = 0
        self.angle2 = 0
        self.angle3 = 0
        self.id = 0
        self.id2 = 0
        self.id3 = 0
        self.x = 250
        self.y = 200
        self.clock_size = 170
        self.time = datetime.datetime.now()
        self.sound = False
        self.alarm = False
        self.is_alarm = False

        # ------------------Widgets------------------------------
        self.canvas = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas.pack()

        self.sound_button = tk.Button(
            text='Sound On',
            font='Consolas 9', bg='white', command=None)

        self.alarm_button = tk.Button(
            text='Alarm On',
            font='Consolas 9', bg='white', command=None)

        self.sound_button.pack()
        self.alarm_button.pack()

        # ---------------First render and start------------------
        self.first_render()
        self.tick()

    # ---------------------Service methods--------------------------
    def get_position(self, angle):
        _angle = math.radians(angle)
        x = self.x + self.clock_size * math.cos(_angle)
        y = self.y + self.clock_size * math.sin(_angle)
        return x, y

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

    # --------------------Render methods----------------------------
    def first_render(self):
        for i, angle in enumerate(range(-60, 300, 30)):
            x, y = self.get_position(angle)
            self.canvas.create_text(
                x, y, text=str(i + 1), justify=tk.CENTER, font="Consolas 14")

        self.create_new_line(150, 5, self.angle2, id=2)
        self.create_new_line(80, 9, self.angle3, id=3)
        self.create_new_line(150, 3, self.angle, color='red')

        self.canvas.create_oval(self.x - 6, self.y - 6, self.x + 6,
                                self.y + 6, fill='black')

    def render(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.id2)
        self.canvas.delete(self.id3)

        self.create_new_line(150, 5, self.angle2, id=2)
        self.create_new_line(80, 9, self.angle3, id=3)
        self.create_new_line(150, 3, self.angle, color='red')
        self.canvas.create_oval(self.x - 6, self.y - 6, self.x + 6,
                                self.y + 6, fill='black')

    def create_new_line(self, length, width,
                        angle_, color='black', id=''):
        angle = math.radians(angle_)
        end_x = self.x + length * math.cos(angle)
        end_y = self.y + length * math.sin(angle)
        setattr(self, 'id' + str(id), self.canvas.create_line(
            self.x, self.y, end_x, end_y, width=width, fill=color))


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Clock')
    root.geometry('500x460+300+100')
    root.resizable(False, False)
    Application(root)
    root.mainloop()
