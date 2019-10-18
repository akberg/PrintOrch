'''
Utility methods for PrintOrch
Andreas Klavenes Berg
08.01.2019
'''
# Imports
from os import listdir, system
from PyPDF2 import PdfFileReader, PdfFileMerger
#import json

# TODO: Add json parser to allow a settings file


instruments = [
    ["violin 1", ["vln", "1.fiolin", "violin"], 16],
    ["violin 2", ["vln", "2.fiolin", "violin"], 16],
    ["viola", ["vla", "bratsj", "viola", "viole"], 14],
    ["cello", ["vcl", "cello", "celli", "violoncello"], 9],
    ["bass", ["vba", "bass", "contrabass", "kontrabass"], 6],
    ["oboe", ["obo", "oboe", "oboi"], 2],
    ["clarinet", ["cl", "klarinett", "clarinet"], 2],
    ["flute", ["fl", "fløyte", "flute"], 2],
    ["bassoon", ["bassoon", "bn", "fagott"], 2],
    ["percussion", ["perc", "percussion", "slagverk"], 4],
    ["horns", ["horn", "hn"], 4]
    ]

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
    return True if [filename.lower().find(w) == -1 for w in exclude_keywords] else False

    '''return True if \
        "score" not in filename.lower() and \
        "partitur" not in filename.lower() and \
        "merged" not in filename.lower() and \
        "ikkebruk" not in filename.lower() and \
        "printready" not in filename.lower() else False'''


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
        files.append(PdfFileReader(path + "\\" + f, strict=False))
    return files


def get_instrument(file: str, work: str):
    '''
    Recognize instrument from filename
    :param file: filename
    :param work: Name of selected musical work
    :return: Recognized instrument
    '''
    i = file.find(work)
    file = file[:i] + file[i + len(work):]

    i = file.find(".pdf")
    file = file[:i]
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
        print(e)'''
    return file


def get_num(file: str, work):
    '''
    Determine the probable number for the given part
    Ting å tenke på:
    * En fil kan inneholde flere stemmer etter hverandre (eks. "Cello, Kontrabass", "klarinett 1,2")
    * Mange forskjellige konvensjoner. Kan prøve å standardisere, men bør dekke så mange som mulig
    
    :param file: filename
    :return: An integer
    '''
    file = get_instrument(file, work)
    n = 2
    for k in instruments:
        for l in k[1]:
            if file.lower().find(l) != -1:
                n = k[2]
    return n



def merge_files(out_file: PdfFileMerger, files, nums, n):
    for i in range(n):
        for j in range(nums[i]):
            try:
                out_file.append(files[i])
                print("Appending", files[i], nums[i], "times")
            except Exception as err:
                print(err)
                print(files[i])


def file_exists(path, name):
    return name + ".pdf" in listdir(path)

