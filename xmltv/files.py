import datetime
import re
from pathlib import Path
from typing import List

from . import xmltv

pattern_xmltv_id = re.compile(r'(?:\w+\.)+[a-z]+$')


def is_channel(name: str):
    return pattern_xmltv_id.search(name) is not None


def parse_filename(name: str):
    channel, date = name.split('_')
    date_obj = datetime.date.fromisoformat(date)
    return channel, date, date_obj


class XMLTVFiles:
    root = None

    def __init__(self, root: Path):
        self.root = root

    def providers(self, channel: str):
        providers = []
        for entry in self.root.joinpath(channel).iterdir():
            if not entry.is_dir():
                continue
            if entry.name[0:5] != 'xmltv':
                continue
            providers.append(entry.name)
        return providers

    def find_subfolder(self, file: Path):
        channel, date, date_obj = parse_filename(file.stem)
        relative = file.relative_to(self.root)
        relative_part = self.root
        for part in relative.parts:
            relative_part = relative_part.joinpath(part)
            if part in [date_obj.year, date, channel, file.name]:
                continue
            return relative_part
        return None

    def find_files(self, directory: Path = None, date_filter: datetime.date = None):
        if not directory:
            directory = self.root
        files = {}
        for file in directory.iterdir():
            if file.is_dir():
                files.update(self.find_files(file))
                continue
            try:
                channel, date = file.stem.split('_')
            except ValueError:
                continue
            date_obj = datetime.date.fromisoformat(date)
            if channel not in files:
                files[channel] = {}
            if date_obj.year not in files[channel]:
                files[channel][date_obj.year] = []

            channel, date, date_obj = parse_filename(file.stem)
            if date_filter and date_filter != date_obj:
                continue
            files[channel][date_obj.year].append(file)
            pass

            # subfolder = self.find_subfolder(file)

        return files

    def find_channels(self) -> List[xmltv.Channel]:
        files = self.root.glob('channels*.xml')
        channels = []
        for file in files:
            channels += xmltv.parse_channel_file(file)
        return channels

    def channel_folder(self, channel: str):
        return self.root.joinpath(channel)

    def file(self, channel: str, date: datetime.date, sub_folder: str = 'xmltv'):
        return self.channel_folder(channel).joinpath(sub_folder, date.strftime('%Y'),
                                                     f'{channel}_{date.isoformat()}.xml')

    def get_day(self, day: datetime.date, channel: str, provider_arg: str = None):
        providers = self.providers(channel)
        for provider in providers:
            if provider != provider_arg:
                continue
            file = self.file(channel, day, provider)
            print(file)
            if file.exists():
                return xmltv.parse_file(file)

        raise RuntimeError(f"No data for {channel} {day.isoformat()}")
