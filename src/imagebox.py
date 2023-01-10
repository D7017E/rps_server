import os
from dataclasses import dataclass

@dataclass()
class ImageBox:
    """
    A class that holds the processed and raw image filename for a prediction.

    Attributes
    ----------
    processed : str
        The filename of the processed image. Contains gesture prediction and joint information.
    raw : str
        The filename of the raw image.
    """

    processed: str
    raw: str

    def get_absolute_paths(self, path: str) -> "ImageBox":
        """
        Returns the absolute paths of the processed and raw image.

        Parameters
        ----------
        path : str
            The path to the folder containing the images

        Returns
        -------
        ImageBox
            The absolute paths of this instance of ImageBox
        """
        return ImageBox(
            processed=os.path.join(path, self.processed),
            raw=os.path.join(path, self.raw)
        )
