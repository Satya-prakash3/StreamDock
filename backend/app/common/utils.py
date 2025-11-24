import pytz
import random
from fastapi import status
from pyfiglet import Figlet
from datetime import datetime, timezone
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, field_serializer

from app.common.constants import Constants


T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Operation Successful"
    data: Optional[T] = None


def success_response(
    message: Optional[str] = None,
    data: dict | list | None = None,
    status_code: int = status.HTTP_200_OK,
) -> dict[str, any]:
    """
    Standard format for successful responses.
    Example:
        return success_response("User registered", {"id": user.id})
    """
    response = {
        "success": True,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    # response["status_code"] = code
    return response


IST = pytz.timezone(Constants.TIME_ZONE)


def utc_now() -> datetime:
    """Always use UTC time."""
    return datetime.now(timezone.utc)


def to_ist(dt: datetime) -> datetime:
    """Convert UTC datetime to IST."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)
    return dt.astimezone(IST)


class ISTTimeStampedResponse(BaseModel):
    """Base model that converts ALL datetime fields to IST when serializing."""

    @field_serializer("*", when_used="always")
    def serialize_any_datetime(self, value: any, _info):
        if isinstance(value, datetime):
            return to_ist(value).strftime("%Y-%m-%d %H:%M:%S")
        return value


SAFE_FONTS = [
    "big",
    "bubble",
    "colossal",
    "doom",
    "standard",
    "small",
    "rectangles",
    "slant",
    "larry3d",
    "ansi_shadow",
    "ansi_regular",
]


class ASCIIART:
    def __init__(self, text="Twogether", font=None):
        art = self.render_ascii(text, font)
        self.box(art)

    def render_ascii(self, text, font=None):
        figlet = Figlet()

        if font:
            figlet.setFont(font=font)
        else:
            random_font = random.choice(SAFE_FONTS)
            figlet.setFont(font=random_font)

        return figlet.renderText(text)

    def box(self, content, padding=2, symbol_ver="│", symbol_hor="─"):
        lines = [line.rstrip() for line in content.split("\n")]
        max_width = max(len(line) for line in lines if line.strip())
        total_inner_width = max_width + (padding * 2)

        print(" " + symbol_hor * total_inner_width)
        for line in lines:
            clean = line.rstrip()
            padded = " " * padding + clean.ljust(max_width) + " " * padding
            print(f"{symbol_ver}{padded}{symbol_ver}")
        print(" " + symbol_hor * total_inner_width)


# if __name__ == "__main__":
#     ASCIIART()
