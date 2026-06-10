from app.resolvers.base_ytdlp_resolver import YtDlpBaseResolver


class TwitchResolver(YtDlpBaseResolver):

    def supports(self, url: str) -> bool:
        return "twitch.tv" in url
