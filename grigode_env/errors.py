"""Error Handlers"""


class InvalidExtensionFile(Exception):
    """Invalid extension file"""

    def __init__(self) -> None:
        super().__init__("Only files with the extension '.env' are accepted.")
