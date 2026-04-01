import dataclasses
from typing import Optional
from xml.etree.ElementTree import Element


@dataclasses.dataclass
class TV:
    source_info_url: Optional[str] = None
    source_info_name: Optional[str] = None
    source_data_url: Optional[str] = None
    generator_info_name: Optional[str] = None
    generator_info_url: Optional[str] = None

    @classmethod
    def from_xml(cls, tv: Element):
        if tv.tag != 'tv':
            raise RuntimeError('Tag is not tv')
        return cls(
            source_info_url=tv.attrib.get('source-info-url'),
            source_info_name=tv.attrib.get('source-info-name'),
            source_data_url=tv.attrib.get('source-data-url'),
            generator_info_name=tv.attrib.get('generator-info-name'),
            generator_info_url=tv.attrib.get('generator-info-url'),
        )
