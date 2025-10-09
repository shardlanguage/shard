from shardc.utils.style.colorize import colorize
from shardc.utils.style.colors import ANSIColorCode

class ErrorClass:
    NOTE = 0
    WARNING = 1
    ERROR = 2
    FATAL = 3

error_types = {
    ErrorClass.NOTE: colorize("note", ANSIColorCode.CYAN),
    ErrorClass.WARNING: colorize("warning", ANSIColorCode.YELLOW),
    ErrorClass.ERROR: colorize("error", ANSIColorCode.RED),
    ErrorClass.FATAL: colorize("fatal", ANSIColorCode.BOLD_RED)
}