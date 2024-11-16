import torch.backends.mps, torch.cuda
from track_almost_anything._logging import log_info


class TorchBackend:
    def __init__(self):
        self.__backend = self.__find_backend()
        log_info(f"Using Torch backend: {self.__backend}")

    def __find_backend(self):
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")

    def get(self):
        return self.__backend
