import tkinter
from typing import Callable
import pandas as pd

import numpy as np
import seaborn as sns
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def init_gui(root) -> FigureCanvasTkAgg:

    # create empty figure and draw
    init_figure = create_figure()
    canvas = FigureCanvasTkAgg(init_figure, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    # call key press event
    return canvas


def create_figure() -> Figure:
    # generate some data
    # matrix = np.random.randint(20, size=(10, 10))
    # plot the data
    figure = Figure(figsize=(6, 6))
    ax = figure.subplots()
    rs = np.random.RandomState(365)
    values = rs.randn(365, 4).cumsum(axis=0)
    dates = pd.date_range("1 1 2016", periods=365, freq="D")
    
    data = pd.DataFrame(values, dates, columns=["A", "B", "C", "D"])
    data = data.rolling(7).mean()
    sns.lineplot(data=data, palette="tab10", linewidth=2.5, ax=ax)
    #sns.heatmap(matrix, square=True, cbar=False, ax=ax)
    return figure


def redraw_figure():
    figure = create_figure()
    canvas.figure = figure
    canvas.draw()


sns.set()
root = tkinter.Tk()
canvas = init_gui(root)
#canvas.after(1000,redraw_figure)

tkinter.mainloop()