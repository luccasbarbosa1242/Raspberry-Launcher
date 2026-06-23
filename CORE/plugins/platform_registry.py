class PlatformRegistry:

    def __init__(self):

        self.mapping = {}

    def register(
        self,
        platform,
        plugin
    ):

        self.mapping[
            platform
        ] = plugin

    def get(
        self,
        platform
    ):

        return self.mapping.get(
            platform
        )