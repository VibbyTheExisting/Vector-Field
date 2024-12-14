import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

class Graph:
    def __init__(self, vector_field):
        self.x, self.y = np.meshgrid(np.linspace(-5, 5, 10), np.linspace(-5, 5, 10))
        self.step = 0.5
        self.polygon = None
        self.ani= None
        self.frames = 30
        self.vector_field = vector_field
        u,v = vector_field(self.x,self.y)

        self.drawn = False
        self.points = []
        plt.quiver(self.x, self.y, u, v)
        plt.connect("button_press_event", self.on_click)
        plt.connect("button_release_event", self.on_release)

        plt.grid()
        plt.show()

    def on_click(self, event):
        if self.drawn:
            return
        if event.button is MouseButton.LEFT:
            self.points.append((event.xdata, event.ydata))

    def on_release(self, event: MouseEvent):
        if self.drawn:
            return
        if not (event.button is MouseButton.LEFT):
            return
        if self.points:
            x,y = event.xdata, event.ydata
            self.points.append((x,y))
            self.points.insert(1, (self.points[0][0], self.points[1][1]))
            self.points.append((self.points[2][0], self.points[0][1]))
            self.polygon = patches.Polygon(self.points, closed=True, edgecolor='red', facecolor='none')
            plt.gca().add_patch(self.polygon)
            self.ani = FuncAnimation(plt.gcf(), self.update, frames=self.frames, interval=50, repeat=False)
            self.drawn = True
            plt.draw()

    def update(self, frame):
        for i,(x1,y1) in enumerate(self.points):
            u,v = self.vector_field(x1,y1)
            self.points[i] = (x1+self.step*u, y1+self.step*v)
        if self.polygon: self.polygon.set_xy(self.points)
        plt.draw()

        if frame == self.frames-1:
            self.remove_polygon()

    def remove_polygon(self, *args, **kwargs):
        if self.polygon:
            self.polygon.remove()
            self.polygon = None
            self.points = []
            self.drawn = False
            plt.draw()

Graph(lambda x,y: (x / np.sqrt(x**2 + y**2), y / np.sqrt(x**2 + y**2)))