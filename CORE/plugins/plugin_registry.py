class PluginRegistry:

    def __init__(self):

        self.plugins = {}

    def register(
        self,
        plugin_id,
        plugin
    ):

        self.plugins[
            plugin_id
        ] = plugin

    def get(
        self,
        plugin_id
    ):

        return self.plugins.get(
            plugin_id
        )

    def all(self):

        return self.plugins