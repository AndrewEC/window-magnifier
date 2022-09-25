from pathlib import Path


def get_icon_path() -> Path | None:
    icon_path = Path(__file__).absolute().parent.parent.joinpath('resources').joinpath('icon.png')
    if icon_path.is_file():
        return icon_path
    icon_path = Path(__file__).absolute().parent.parent.parent.joinpath('resources').joinpath('icon.png')
    return icon_path if icon_path.is_file() else None
