from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class RenderCanvas(FigureCanvas):
    def __init__(self, parent, width, height, dpi):
        self._figure = Figure(figsize=(width, height), dpi=dpi)
        self._ax = self._figure.add_subplot(111)
        super(RenderCanvas, self).__init__(self._figure)
        self.setParent(parent)

    def figure(self):
        return self._figure
    
    def ax(self):
        return self._ax