from typing import List
from xml.etree import ElementTree

from .program import Program


def filter_programs(programs: List[Program], title: str) -> List[Program]:
    """
    Filter a list of program objects by title
    :param programs: List of program objects
    :param title: Title to filter
    :return: Filtered list of program objects
    """
    return [program for program in programs if program.title.text == title]


def parse_file(file) -> List[Program]:
    """
    Parse an XMLTV file into a list of Program objects.
    :param file: XMLTV file
    :return: List of Program objects
    """
    tree = ElementTree.parse(file)
    root = tree.getroot()
    programs = [Program.from_xml(program) for program in root]
    return programs
