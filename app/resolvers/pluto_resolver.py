from app.resolvers.base_ytdlp_resolver import YtDlpBaseResolver


class PlutoResolver(YtDlpBaseResolver):

    def supports(self, url: str) -> bool:
        return "pluto.tv" in url
