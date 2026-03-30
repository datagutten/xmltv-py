import dataclasses
import datetime
from typing import Optional, List
from xml.etree.ElementTree import Element

from . import elements


def parse_time(time: str) -> Optional[datetime.datetime]:
    if time is None:
        return None
    return datetime.datetime.strptime(time, "%Y%m%d%H%M%S %z")


def parse_episode(epnum: list[Element]):
    for num in epnum:
        if num.attrib['system'] != 'xmltv_ns':
            continue
        season, episode, part = num.text.split('.')
        if '/' in episode:
            episode, total_episodes = episode.split('/')
        if '/' in season:
            season, total_seasons = season.split('/')
        if '/' in part:
            part, total_parts = part.split('/')

        if season:
            season = int(season) + 1
        else:
            season = None
        if episode:
            episode = int(episode) + 1
        else:
            episode = None
        if part:
            part = int(part) + 1
        else:
            part = None

        return season, episode, part
    return None, None, None


@dataclasses.dataclass
class Program:
    titles: Optional[List[elements.Title]]  # = None
    sub_titles: Optional[List[elements.SubTitle]] = None
    description: str = None
    start: datetime.datetime = None
    end: datetime.datetime = None
    first_aired: datetime.datetime = None
    urls: Optional[List[elements.URL]] = None
    categories: list[str] = None
    season: int = None
    episode: int = None
    part: int = None
    time_zone = None

    @classmethod
    def from_xml(cls, program: Element):
        season, episode, part = parse_episode(program.findall('episode-num'))
        return cls(
            titles=elements.Title.find_multi(program),
            sub_titles=elements.SubTitle.find_multi(program),
            start=parse_time(program.attrib["start"]),
            end=parse_time(program.attrib.get("stop")),
            urls=elements.URL.find_multi(program),
            categories=[category.text for category in program.findall('categories')],
            season=season,
            episode=episode,
            part=part,
            description=program.find('desc').text,
        )

    @property
    def title(self):
        return self.titles[0] if self.titles else None

    @property
    def sub_title(self):
        return self.sub_titles[0] if self.sub_titles else None

    @property
    def url(self):
        return self.urls[0] if self.urls else None

    @property
    def duration(self):
        return self.end - self.start

    @property
    def time_format(self):
        if not self.end:
            return self.start.strftime('%H:%M')
        else:
            return '%s-%s' % (self.start.strftime('%H:%M'), self.end.strftime('%H:%M'))
