class Arguments:

    def __init__(self, target_window_title: str, capture_delay_interval: float, resampling_filter: str,
                 capture_mouse: bool):
        self.target_window_title = target_window_title
        self.capture_delay_interval = capture_delay_interval
        self.resampling_filter = resampling_filter
        self.capture_mouse = capture_mouse

    def __repr__(self):
        return f'Arguments(Target Window: [{self.target_window_title}], ' \
               f'Capture Delay Interval: [{self.capture_delay_interval}], ' \
               f'Resampling Filter: [{self.resampling_filter}], ' \
               f'Capture Mouse: [{self.capture_mouse}])'
