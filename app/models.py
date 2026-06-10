from pydantic import BaseModel


class StreamInfo(BaseModel):
    title: str | None
    is_live: bool | None
    stream_url: str
    format_id: str | None
