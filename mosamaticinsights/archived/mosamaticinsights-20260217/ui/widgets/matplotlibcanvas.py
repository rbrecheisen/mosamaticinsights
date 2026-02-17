from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent, nrows=1, ncols=1, width=6, height=4, dpi=100, axes_off=True):
        self._figure = Figure(figsize=(width, height), dpi=dpi, layout='tight')
        self._axes = self._figure.subplots(nrows, ncols)
        if axes_off:
            for ax in self._figure.axes:
                ax.set_axis_off()
        super(MatplotlibCanvas, self).__init__(self._figure)
        self.setParent(parent)
        self._nrows = nrows
        self._ncols = ncols
        self._navigation_toolbar = None

    def axes(self, idx=0, idy=0):
        assert idx<self._nrows and idy<self._ncols
        if idx>0 and idy>0:
            return self._axes[idx, idy]
        elif idx>0:
            return self._axes[idx]
        else:
            return self._axes
        
    def navigation_toolbar(self):
        if not self._navigation_toolbar:
            self._navigation_toolbar = NavigationToolbar(self, self.parent())
        return self._navigation_toolbar