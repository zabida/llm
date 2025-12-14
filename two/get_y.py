import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

class CurveDrawer:
    def __init__(self, x=24, y=50):
        self.xs = []
        self.ys = []
        self.x_max = x
        self.y_max = y
        self.drawing = False

        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'b-', linewidth=2)

        self.ax.set_xlim(0, x)
        self.ax.set_ylim(0, y)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title("drow x:0~24, y:0~50 ")

        self.fig.canvas.mpl_connect("button_press_event", self.on_press)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_move)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)

    def on_press(self, event):
        if event.button == 1 and event.inaxes == self.ax:
            self.drawing = True
            self.xs = [event.xdata]
            self.ys = [event.ydata]

    def on_move(self, event):
        if self.drawing and event.inaxes == self.ax:
            if 0 <= event.xdata <= self.x_max and 0 <= event.ydata <= self.y_max:
                self.xs.append(event.xdata)
                self.ys.append(event.ydata)
                self.line.set_data(self.xs, self.ys)
                self.fig.canvas.draw_idle()

    def on_release(self, event):
        if event.button == 1:
            self.drawing = False
            self.process_curve()

    def process_curve(self):
        # 排序，防止回拉
        xs = np.array(self.xs)
        ys = np.array(self.ys)
        order = np.argsort(xs)
        xs, ys = xs[order], ys[order]

        # 插值
        f = interp1d(xs, ys, kind="linear", fill_value="extrapolate")

        x_sample = np.arange(0, self.x_max + 1, 1)
        y_sample = f(x_sample)

        print(f"\n采样结果（x=0~{self.x_max}，步长=1）：")
        for x, y in zip(x_sample, y_sample):
            print(f"x={x:2d}, y={y:.2f}")

if __name__ == "__main__":
    drawer = CurveDrawer(x=300, y=128)
    plt.show()
