import tkinter as tk
from tkinter import ttk
import rippleTank as rt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

class RippleTankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ripple Tank Simulation")
        
        self.start_button = ttk.Button(self, text="Start Simulation", command=self.run_simulation)
        self.start_button.pack(pady=20)
        
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
    
    def run_simulation(self):
        # Setup the ripple tank
        self.tank = rt.RippleTank()
        rt.Source(self.tank, rt.sineSource, xcorners=(-15, 15), ycorners=(10, 11), freq=10.0)
        rt.Mask(self.tank).fromFunc(rt.singleSlit, ((-15, 15), (0, self.tank.dy)))
        self.tank.simulateTime(2.0, animation_speed=0.5)
        
        # Extract frames from the simulation
        self.frames = self.extract_frames(self.tank, duration=2.0, fps=30)
        
        # Setup the Matplotlib figure and axes
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-15, 15)
        
        # Create the animation
        self.ani = FuncAnimation(self.fig, self.update, frames=len(self.frames), blit=False, interval=1000/30)
        
        # Integrate with Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def extract_frames(self, tank, duration, fps):
        # Capture frames at each timestep
        num_frames = int(duration * fps)
        frames = []
        for _ in range(num_frames):
            tank.stepSimulation(1.0 / fps)  # Assuming stepSimulation steps the simulation forward by the given time
            frames.append(tank.get_state())  # Assuming get_state() gets the current state/frame
        return frames

    def update(self, frame_index):
        self.ax.clear()
        frame = self.frames[frame_index]
        self.ax.imshow(frame, extent=(-15, 15, -15, 15))  # Adjust extent if necessary
        return self.ax

if __name__ == "__main__":
    app = RippleTankApp()
    app.mainloop()
