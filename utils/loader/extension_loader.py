from pathlib import Path

class ExtensionLoader:
    def __init__(self, bot, extension_dir='extensions'):
        self.bot = bot
        self.extension_dir = Path(extension_dir)

    def _iterate_extensions(self, action):
        # Determine the action verb from input for user-friendly messages.
        action_verb = action.__name__.split('_')[0]

        for filepath in self.extension_dir.iterdir():
            if filepath.suffix == '.py' and filepath.name != '__init__.py':
                extension_name = f"{self.extension_dir.name}.{filepath.stem}"
                try:
                    action(extension_name)
                    print(f"{action_verb.capitalize()}ed extension: {filepath.stem}")
                except Exception as e:
                    print(f"Failed to {action_verb} extension {filepath.stem}. Reason: {e}")

    def load_extensions(self):
        self._iterate_extensions(self.bot.load_extension)

    def unload_extensions(self):
        self._iterate_extensions(self.bot.unload_extension)
