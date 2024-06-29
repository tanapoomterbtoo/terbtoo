import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

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
        self.cap = cv2.VideoCapture(0)

        # Start the video loop
        self.update_video()

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

    def on_closing(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
