import tkinter as tk
import datetime


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

        # --------------------Render-----------------------------
        self.first_render()

    def first_render(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Clock')
    root.geometry('500x460+300+100')
    root.resizable(False, False)
    Application(root)
    root.mainloop()
