class Arguments:

    def __init__(self, target_window_title: str, capture_delay_interval: float, resampling_filter: str,
                 capture_mouse: bool, always_on_top: bool, refocus_to_target: bool):
        self.target_window_title = target_window_title
        self.capture_delay_interval = capture_delay_interval
        self.resampling_filter = resampling_filter
        self.capture_mouse = capture_mouse
        self.always_on_top = always_on_top
        self.refocus_to_target = refocus_to_target

    def __repr__(self):
        return f'Arguments(Target Window: [{self.target_window_title}], ' \
               f'Capture Delay Interval: [{self.capture_delay_interval}], ' \
               f'Resampling Filter: [{self.resampling_filter}], ' \
               f'Capture Mouse: [{self.capture_mouse}], ' \
               f'Always on Top: [{self.always_on_top}], ' \
               f'Refocus to Target: [{self.refocus_to_target}])'
