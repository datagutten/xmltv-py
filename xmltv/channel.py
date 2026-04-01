import dataclasses
from typing import Optional, List
from xml.etree.ElementTree import Element

from . import elements
from .tv import TV


@dataclasses.dataclass
class Channel:
    channel_id: str
    display_names: Optional[List[elements.DisplayName]] = None
    tv: TV = None

    @classmethod
    def from_xml(cls, channel: Element, tv: Element = None):
        if channel.tag != 'channel':
            raise RuntimeError('Tag is not channel')
        channel_obj = cls(channel.attrib.get('id'))
        if tv is not None:
            channel_obj.tv = TV.from_xml(tv)
        channel_obj.display_names = [elements.DisplayName(name) for name in channel.findall('display-name')]

        return channel_obj

    @property
    def display_name(self):
        return self.display_names[0] if self.display_names else None

    def programs(self):
        pass
