class ExportError(Exception):
    """Base exception for export-related errors."""
    pass


class ExportFormatError(ExportError):
    """Raised when there's an error with the export format."""
    pass


class ExportPermissionError(ExportError):
    """Raised when user doesn't have permission to export."""
    pass


class ExportLimitError(ExportError):
    """Raised when export exceeds limits."""
    pass


class ExportFieldError(ExportError):
    """Raised when there's an error with field selection."""
    pass


class ExportQuerysetError(ExportError):
    """Raised when there's an error with the queryset."""
    pass 