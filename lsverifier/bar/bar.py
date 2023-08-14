from tqdm import tqdm

class Bar(tqdm):
    def __init__(self, iterable=None, leave=True, verbose=False):
        self.iterable = iterable
        self.leave = leave

        self.disable = True if verbose else False
        self.bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt}"

        super().__init__(self.iterable, leave=self.leave, disable=self.disable, bar_format=self.bar_format)


