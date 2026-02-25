from rbeesoft.app.ui import RbeesoftMainWindow
from rbeesoft.common.logmanager import LogManager
from rbeesoft.app.ui.processes.processrunner import ProcessRunner
from rbeesoft.common.utils import current_time_in_seconds, elapsed_time_in_seconds, duration
from mosamaticinsights.ui.widgets.pages.homepage.homepage import HomePage
from mosamaticinsights.ui.widgets.pages.l3analysispage.l3analysispage import L3AnalysisPage
from mosamaticinsights.ui.widgets.pages.l3autoselectionpage.l3autoselectionpage import L3AutoSelectionPage
from mosamaticinsights.ui.processes.rescaledicomimagesprocess import RescaleDicomImagesProcess
from mosamaticinsights.ui.processes.selectslicefromscansprocess import SelectSliceFromScansProcess

MAJOR_VERSION = 1.0
LOG = LogManager()


class MainWindow(RbeesoftMainWindow):
    def __init__(self, app_icon):
        super(MainWindow, self).__init__(
            bundle_identifier='rbeesoft.nl',
            app_name='mosamaticinsights',
            app_title='Mosamatic Insights',
            app_major_version=MAJOR_VERSION,
            app_width=800,
            app_height=600,
            app_icon=app_icon,
            requires_license=False,
        )
        self.add_page(
            HomePage('home', 'Home', self.settings()), home_page=True)
        self.add_page(
            L3AnalysisPage('l3analysis', 'L3 analysis', self.settings()))
        self.add_page(
            L3AutoSelectionPage('l3autoselection', 'L3 auto-selection', self.settings()))
        self._process_runner = None
        self._process_start_time = None
        self._process_elapsed_time = None
        self.init()

    # INITIALIZATION

    def init(self):
        page = self.page('l3autoselection')
        page.start_process.connect(self.handle_l3autoselection_start_process)

    # GETTERS

    def process_runner(self):
        if not self._process_runner:
            self._process_runner = ProcessRunner()
        return self._process_runner

    # EVENT HANDLERS

    def handle_l3autoselection_start_process(self, inputs, output, params, overwrite, create_task_subdir):
        process = SelectSliceFromScansProcess(inputs, output, params, overwrite, create_task_subdir)
        process.progress.connect(self.handle_progress)
        process.finished.connect(self.handle_finished)
        process.canceled.connect(self.handle_canceled)
        process.failed.connect(self.handle_failed)
        self._process_start_time = current_time_in_seconds()
        self.process_runner().start(process)

    def handle_progress(self, step, nr_steps):
        LOG.info(f'Progress: {step} of {nr_steps}')

    def handle_finished(self, result):
        self._process_elapsed_time = elapsed_time_in_seconds(self._process_start_time)
        LOG.info(f'Finished in {duration(self._process_elapsed_time)}')

    def handle_canceled(self):
        LOG.info('Canceled')

    def handle_failed(self, e):
        LOG.info(f'Failed ({str(e)})')