import shutil
import tempfile
from pathlib import Path
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from app.models import StreamInfo
from app.resolvers.resolver_interface import StreamResolver, ResolutionError


class YtDlpBaseResolver(StreamResolver):

    def __init__(self, cookies_file: str | None = None):
        self.options = {
            "quiet": True,
            "no_warnings": True,
        }
        if cookies_file:
            self.options["cookiefile"] = self._writable_copy(cookies_file)

    def _writable_copy(self, source: str) -> str:
        src = Path(source)
        if not src.exists():
            raise ResolutionError(f"Cookies file not found: {source}")
        if src.parent == Path(tempfile.gettempdir()):
            return source
        dest = Path(tempfile.gettempdir()) / "yt_dlp_cookies.txt"
        shutil.copy2(src, dest)
        return str(dest)

    def resolve(self, url: str) -> StreamInfo:
        try:
            with YoutubeDL(self.options) as ydl:
                info = ydl.extract_info(url, download=False)
        except (DownloadError, Exception) as e:
            raise ResolutionError(str(e)) from e

        formats = info.get("formats", [])

        if not formats:
            raise ResolutionError("No formats found")

        m3u8_formats = [
            f for f in formats
            if f.get("ext") == "m3u8" or "m3u8" in f.get("protocol", "")
        ]

        target_formats = m3u8_formats if m3u8_formats else formats

        best = max(
            target_formats,
            key=lambda f: f.get("height") or 0
        )

        return StreamInfo(
            title=info.get("title"),
            is_live=info.get("is_live"),
            stream_url=best["url"],
            format_id=best.get("format_id")
        )
