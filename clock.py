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
        self.center = {'x': 250, 'y': 200}
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

        # --------------------First and start---------------------
        self.first_render()
        self.tick()

    # ----------------------Time methods----------------------------
    def do_tick(self):
        self.time += datetime.timedelta(seconds=1)
        self.tick()

    def tick(self):
        hours = self.time.hour
        hours = int(hours) % 12
        self.angle = int(self.time.second) * 6 - 90
        self.angle2 = int(self.time.minute) * 6 - 90
        self.angle3 = int(self.time.hour) * 30 - 90 \
            + (int(self.time.minute) // 2)
        self.render()
        self.canvas.after(1000, self.do_tick)

    # --------------------Render methods----------------------------
    def first_render(self):
        x = [335, 400, 410, 390, 330, 250, 170, 110, 90, 100, 165, 250]
        y = [55, 115, 200, 280, 340, 360, 340, 280, 200, 115, 55, 30]
        for i in range(12):
            self.canvas.create_text(x[i], y[i], text=str(i + 1),
                                    justify=tk.CENTER, font="Consolas 14")

        self.create_new_line(250, 200, 150, 5, self.angle2, id=2)
        self.create_new_line(250, 200, 80, 9, self.angle3, id=3)
        self.create_new_line(250, 200, 150, 3, self.angle, color='red')

        self.canvas.create_oval(244, 194, 256, 206, fill='black')

    def render(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.id2)
        self.canvas.delete(self.id3)

        self.create_new_line(250, 200, 150, 5, self.angle2, id=2)
        self.create_new_line(250, 200, 80, 9, self.angle3, id=3)
        self.create_new_line(250, 200, 150, 3, self.angle, color='red')
        self.canvas.create_oval(244, 194, 256, 206, fill='black')

    def create_new_line(self, x1, y1, length, width,
                        angle_, color='black', id=''):
        angle = math.radians(angle_)
        end_x = x1 + length * math.cos(angle)
        end_y = y1 + length * math.sin(angle)
        setattr(self, 'id' + str(id), self.canvas.create_line(
            x1, y1, end_x, end_y, width=width, fill=color))


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Clock')
    root.geometry('500x460+300+100')
    root.resizable(False, False)
    Application(root)
    root.mainloop()
