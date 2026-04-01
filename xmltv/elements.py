from abc import ABC
from typing import List
from xml.etree.ElementTree import Element


class MultiString(ABC):
    _tag: str

    def __init__(self, element: Element):
        self.text = element.text

    def __str__(self):
        return self.text

    @classmethod
    def find_multi(cls, program: Element) -> List:
        elements_obj = []
        for element in program.findall(cls._tag):
            elements_obj.append(cls(element))
        return elements_obj


class LocalizedElement(MultiString, ABC):
    language: str

    def __init__(self, element: Element):
        super().__init__(element)
        if 'lang' in element.attrib:
            self.language = element.attrib['lang']


class Title(LocalizedElement):
    _tag = 'title'


class DisplayName(LocalizedElement):
    _tag = 'display-name'


class Description(LocalizedElement):
    _tag = 'desc'


class SubTitle(LocalizedElement):
    _tag = 'sub-title'


class URL(MultiString):
    _tag = 'url'
    system: str

    def __init__(self, element: Element):
        super().__init__(element)
        self.system = element.attrib.get('system')
