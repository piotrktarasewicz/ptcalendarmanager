from .core import GlobalPlugin as _CoreGlobalPlugin
from .search_ui import InlineSearchMixin


class GlobalPlugin(InlineSearchMixin, _CoreGlobalPlugin):
    pass
