class Arguments:

    def __init__(self, target_window_title: str,
                 capture_delay_interval: float,
                 resampling_filter: str,
                 capture_mouse: bool,
                 always_on_top: bool,
                 refocus_to_target: bool,
                 screen_capture_mode: bool):

        self.target_window_title = target_window_title
        self.capture_delay_interval = capture_delay_interval
        self.resampling_filter = resampling_filter
        self.capture_mouse = capture_mouse
        self.always_on_top = always_on_top
        self.refocus_to_target = refocus_to_target
        self.screen_capture_mode = screen_capture_mode

    def __repr__(self):
        return f'\n\tArguments(' \
               f'\n\tTarget Window: [{self.target_window_title}]' \
               f'\n\tCapture Delay Interval: [{self.capture_delay_interval}]' \
               f'\n\tResampling Filter: [{self.resampling_filter}]' \
               f'\n\tCapture Mouse: [{self.capture_mouse}]' \
               f'\n\tAlways on Top: [{self.always_on_top}]' \
               f'\n\tRefocus to Target: [{self.refocus_to_target}]' \
               f'\n\tScreen Capture Mode: [{self.screen_capture_mode}]' \
               f')'
