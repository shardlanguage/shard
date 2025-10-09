from shardc.utils.style.colors import ANSIColorCode

def colorize(text: str, color: str, reset: bool=True) -> str:
    return f"{color}{text}{ANSIColorCode.RESET if reset else ''}"