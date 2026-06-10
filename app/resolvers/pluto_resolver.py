from app.resolvers.base_ytdlp_resolver import YtDlpBaseResolver


class PlutoResolver(YtDlpBaseResolver):

    def __init__(self, cookies_file: str | None = None):
        super().__init__(cookies_file=cookies_file)

    def supports(self, url: str) -> bool:
        return "pluto.tv" in url
