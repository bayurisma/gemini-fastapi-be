class AppError(Exception):

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class GeminiServiceError(AppError):

    def __init__(
        self,
        message: str,
        status_code: int = 502,
    ):
        super().__init__(
            code="GEMINI_ERROR",
            message=message,
            status_code=status_code,
        )