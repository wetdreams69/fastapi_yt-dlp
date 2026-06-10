from app.resolvers.base_ytdlp_resolver import YtDlpBaseResolver


class YoutubeResolver(YtDlpBaseResolver):

    def supports(self, url: str) -> bool:
        return "youtube.com" in url or "youtu.be" in url
