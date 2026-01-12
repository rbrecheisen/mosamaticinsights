import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():

    colors = vtkNamedColors()
    
    cone = vtkConeSource()
    cone.SetHeight(3.0)
    cone.SetRadius(1.0)
    cone.SetResolution(10)

    cone_mapper = vtkPolyDataMapper()
    cone_mapper.SetInputConnection(cone.GetOutputPort())

    cone_actor = vtkActor()
    cone_actor.SetMapper(cone_mapper)
    cone_actor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))

    renderer = vtkRenderer()
    renderer.AddActor(cone_actor)
    renderer.SetBackground(colors.GetColor3d('MidnightBlue'))

    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(300, 300)
    render_window.SetWindowName('Tutorial_Step1')

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Initialize()

    render_window.Render()

    def rotate(obj, event):
        renderer.GetActiveCamera().Azimuth(1)
        render_window.Render()

    interactor.AddObserver("TimerEvent", rotate)
    interactor.CreateRepeatingTimer(10)  # ms
    interactor.Start()


if __name__ == '__main__':
    main()