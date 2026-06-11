import logging
import shutil
import tempfile
from pathlib import Path
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from app.models import StreamInfo
from app.resolvers.resolver_interface import StreamResolver, ResolutionError

logger = logging.getLogger(__name__)


class YtDlpBaseResolver(StreamResolver):

    def __init__(self, cookies_file: str | None = None):
        self.options = {
            "quiet": True,
            "no_warnings": True,
        }
        if cookies_file:
            writable = self._writable_copy(cookies_file)
            if writable:
                self.options["cookiefile"] = writable

    def _writable_copy(self, source: str) -> str | None:
        src = Path(source)
        if not src.exists():
            logger.warning("Cookies file not found at %s — starting without cookies.", source)
            return None
        tmp = Path(tempfile.gettempdir()) / "yt_dlp_cookies.txt"
        shutil.copy2(src, tmp)
        return str(tmp)

    def resolve(self, url: str) -> StreamInfo:
        try:
            with YoutubeDL(self.options) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "id": info.get("id"),
                    "title": info.get("title"),
                    "live_status": info.get("live_status"),
                    "formats_count": len(info.get("formats", []))
                }
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
