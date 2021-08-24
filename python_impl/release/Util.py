'''
Utility methods for PrintOrch
Andreas Klavenes Berg
08.01.2019
'''
# Imports
from os import listdir, system
import os
import json
from PyPDF2 import PdfFileReader, PdfFileMerger

# TODO: Add json parser to allow a settings file


instruments = {
    "violin": ["vln", "fiolin", "violin"],
    "viola": ["vla", "bratsj", "viola", "viole"],
    "cello": ["vcl", "cello", "celli", "violoncello"],
    "bass": ["vba", "bass", "contrabass", "kontrabass"],
    "oboe": ["obo", "oboe", "oboi"],
    "clarinet": ["cl", "klarinett", "clarinet"],
    "flute": ["fl", "fløyte", "flute"],
    "bassoon": ["bn", "fagott"]
}

exclude_keywords = [
    "score",
    "partitur",
    "merged",
    "ikkebruk",
    "printready"
]

def get_content(path, filter=True):
    '''
    :param path: Path to target directory
    :param filter: Set to false to include all pdf files
    :return: list of pdf files
    '''
    content = []
    for f in listdir(path):
        if f.split(".")[-1] == "pdf" and (include(f) or not filter):
            content.append(f)
    return content


def include(filename):
    '''
    TODO: Allow a settings (xml or json) file to contain
    excluding keywords to be added or changed by user.
    :param filename: Filename
    :return: If the file should be included
    '''
    with open("settings.json", "r") as f:
        exclude = json.load(f)["exclude-keywords"]
        print("Loaded settings.json")
    return all([w not in filename.lower() for w in exclude])


def open_files(path, content):
    '''
    Open selected files for copying. Should be done as 
    late as possible.
    :param path: Path to selected directory
    :param content: List of containing files that should be opened
    :return: Open file objects
    '''
    files = []
    for f in content:
        files.append(PdfFileReader(os.path.join(path, f), strict=False))
    return files


def get_instrument(file: str, work: str):
    '''
    Recognize instrument from filename
    :param file: filename
    :param work: Name of selected musical work
    :return: Recognized instrument
    '''
    file = file.lower()
    w = work.lower()
    try:
        for c in w + " - ":
            file = file.strip(c)
            if c == " ":
                file = file.strip("_")
        file = file.split(".")
        file.pop()
    except Exception as e:
        print(e)
    return ".".join(file)


def merge_files(out_file: PdfFileMerger, files, nums, n):
    for i in range(n):
        for j in range(nums[i]):
            try:
                out_file.append(files[i])
            except Exception as err:
                print(err)
                print(files[i])


def file_exists(path, name):
    return name + ".pdf" in listdir(path)
