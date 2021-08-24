# Printorch rewrite as a single file script
# Trying OOP solution
# 31.7.2019


# Imports
from os import listdir, system
from easygui import diropenbox
from PyPDF2 import PdfFileReader, PdfFileMerger


class Part():
    """
    Metainfo on a single part
    """

    def __init__(self, filename):
        pass


class ScoreMerger():


    # Path to pdf files
    self.path = ""
    # Name of the work
    self.work = ""
    # Path for save file
    self.save_path = ""
    # Name of save file
    self.save_name = " "
    # PdfMerger
    self.out_file = PdfFileMerger(strict=False)

    alt = -1
    self.n = 0
    self.content = []
    # Number of copies for each pdf
    self.nums = []


    instruments = [
        ["violin 1", ["vln", "1.fiolin", "violin", "^vln|^violin|"], 16],
        ["violin 2", ["vln", "2.fiolin", "violin"], 16],
        ["viola", ["vla", "bratsj", "viola", "viole"], 14],
        ["cello", ["vcl", "cello", "celli", "violoncello"], 9],
        ["bassoon", ["bassoon", "bn", "fagott"], 2],
        ["bass", ["vba", "bass", "contrabass", "kontrabass"], 6],
        ["oboe", ["obo", "oboe", "oboi"], 2],
        ["clarinet", ["cl", "klarinett", "clarinet"], 2],
        ["flute", ["fl", "fløyte", "flute"], 2],
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

    def __init__(self):
        print()

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


    def get_instrument_full(file: str, work: str):
        '''
        Recognize instrument from filename, returns instrument and other details
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
        :param file: filename
        :return: An integer
        '''
        file = get_instrument_full(file, work)
        n = 2
        for k in instruments:
            for l in k[1]:
                if file.lower().find(l) != -1:
                    n = k[2]
        return n


    # TODO:
    def get_num_2(content, n, work):
        return "number for content[n]"


    def set_directory():
        path = diropenbox()
        if path != "":
            work = path.split("\\")[-1]
            save_name = "_".join(work.split()) + "_printready"
            content = get_content(path)
            n = len(content)
            nums = [1]*n
            
            for i in range(n):
                nums[i] = get_num(content[i], work)
                #nums[i] = get_num_2(content, i, work)


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


    def set_save_directory():
        save_path = diropenbox("Velg mappen hvor du vil lagre utskriftfilen.", "Velg målmappe")


    def set_save_name():
        new = input("Lagre som (Tomt felt for å beholde filnavnet {}: ".format(save_name))
        if new != "":
            save_name = new


    def prompt_continue(content, nums, n, save_path):
        print("Valgte filer:")
        [print(content[i].ljust(30) + "Antall: {:3}".format(nums[i])) for i in range(n)]
        print("\nLagres som", save_path, "\n")
        sv = input("Fullføre? (tast [N] for å avbryte): ")
        if sv.lower() == "n":
            return False
        return True


    def prompt_overwrite(self, path, name):
        while 1:
            sv = input("Filen " + path + "\\" + name +
                    ".pdf finnes allerede. Er du sikker på at du vil overskrive den? [ja=1/nei=0]: ")
            try:
                if int(sv) == 1:
                    return True
                elif int(sv) == 0:
                    return False
            except Exception: pass


    def numbers(self):
        '''
        Start process to alter numbers for each copy
        '''


    def proceed(self):
        '''
        Proceed with merging
        '''
        if self.prompt_continue(self.content, self.nums, self.n, self.save_path + self.save_name):
            if file_exists(self.path, self.save_name):
                if not prompt_overwrite(self.path, self.save_name): self.save_name = self.prompt_save_name(self.save_name)

            # Merge
            try:
                files = open_files(self.path, self.content)  # Opens files, do this as late as possible
                merge_files(self.out_file, self.files, self.nums, self.n)
                self.out_file.write(self.save_path + "\\" + self.save_name + ".pdf")

                print("Lagring var vellykket!")
                input("Trykk enter for å fortsette...")

                # Create new object for next merging operation
                out_file = PdfFileMerger(strict=False)
            except Exception as err:
                print("Feil i sluttkode:")
                print(err)
                input()


if __name__ == '__main__':

    merger = ScoreMerger()

    while 1:
        alt = input()

        if alt == 0:
            exit(0)
        
        elif alt == 1:
            set_directory()
        
        elif alt == 2:
            set_save_directory()
        
        elif alt == 3:
            set_save_name()
        
        elif alt == 4:
            numbers()
        elif alt == 5:
            proceed()
