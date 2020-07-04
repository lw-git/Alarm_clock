import tkinter as tk


class Application(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.canvas = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Clock')
    root.geometry('500x460+300+100')
    root.resizable(False, False)
    Application(root)
    root.mainloop()
