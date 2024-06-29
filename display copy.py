import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import rippleTank as rt
import matplotlib.pyplot as plt

class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Webcam Display with Buttons")
        self.root.geometry("1280x720")

        # Create a frame for the video and buttons
        self.video_frame = ttk.Frame(self.root, width=960, height=720)
        self.video_frame.grid(row=0, column=0)

        self.button_frame = ttk.Frame(self.root, width=320, height=720)
        self.button_frame.grid(row=0, column=1, sticky="ns")

        # Create a canvas for the video
        self.canvas = tk.Canvas(self.video_frame, width=960, height=720)
        self.canvas.pack()

        # Create buttons and place them in the button_frame
        self.buttons = []
        for i in range(4):
            button = ttk.Button(self.button_frame, text=f"Button {i+1}")
            button.pack(pady=20)
            self.buttons.append(button)

        # Initialize the video capture
        # self.cap = cv2.VideoCapture(0)
        self.tank = rt.RippleTank()

        # Start the video loop
        self.read_gif()

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (960, 720))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk
        
        self.root.after(10, self.update_video)

    def read_gif(self):
        gif_path = "rippleTank-master/media/singleSlit.gif"
        info = Image.open(gif_path)
        self.frames = info.n_frames 
        self.photoimage_objects = []
        for i in range(self.frames):
            obj = tk.PhotoImage(file = gif_path, format = f"gif -index {i}")
            self.photoimage_objects.append(obj)
        self.update_gif()

    def update_gif(self,current_frame=0):
        image = self.photoimage_objects[current_frame]
        print(image)
        imgtk = ImageTk.PhotoImage(image=image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
        self.canvas.imgtk = imgtk
        current_frame = current_frame + 1

        if current_frame == self.frames:
            current_frame = 0 
        self.root.after(10, self.update_gif(current_frame))

    def animatiotank(self):
        rt.Source(self.tank, rt.sineSource, freq=10)
        self.tank.simulateTime(2.0, animation_speed = 0.5)
        ani = self.tank.makeAnimation()
        ani.save('sim.gif', writer='imagemagick')
            
    def on_closing(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
