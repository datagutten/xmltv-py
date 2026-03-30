import dataclasses
from typing import Optional, List

from . import elements


@dataclasses.dataclass
class Channel:
    channel_id: str
    display_names: Optional[List[elements.DisplayName]] = None

    @property
    def display_name(self):
        return self.display_names[0] if self.display_names else None

    def programs(self):
        pass
