'''
PrintOrch - Programvare for lettere å skrive ut noter til et helt orkester
Andreas Klavenes Berg
09.01.2019
updated: 22.07.2019

Tasks:
- Open directory containing all scores as pdfs
- Read composer and work name from directory name
- Recognize instruments from file names, prompt if there are issues, then learn
- Create a single output file containing correct number of copies from each sheet
'''
try:
    # Imports
    import User
    import Util
    from easygui import diropenbox
    # from UserGUI import Main
except:
    print("Feil i imports")
    input()

# Path to pdf files
path = ""
# Name of the work
work = ""
# Path for save file
save_path = ""
# Name of save file
save_name = ""
# PdfMerger
out_file = Util.PdfFileMerger(strict=False)

alt = -1
n = 0
content = []
# Number of copies for each pdf
nums = []
#main = Main()
#main.run()
#exit()

while 1:
    #Util.system('cls')
    alt = User.display(path, save_path, work, save_name, content, nums, n)

    if alt == 0: # Avlsutt
        out_file.close()
        exit(0)


    elif alt == 1: # Hent mappe
        try:
            path = diropenbox()
        except Exception as e:
            ##print(e)
            input()
        if path != "":
            try: 
                work = path.split("\\")[-1]
                save_name = "_".join(work.split()) + "_printready"
                content = Util.get_content(path)
                n = len(content)
                nums = [1]*n
            except Exception as e:
                ##print(e)
                input()
            #for i in range(n):
            #    nums[i] = Util.get_num(content[i], work)


    elif alt == 2: # Lagringsmappe
        save_path = User.prompt_save_dir()


    elif alt == 3:
        save_name = User.prompt_save_name(save_name)


    elif alt == 4: # Endre antall
        print("Angi tomt felt for å ikke endre verdi.")
        for i in range(n):
            nums[i] = User.prompt_num(Util.get_instrument(content[i], work), nums[i])
    
    
    elif alt == 5: # Fullføre
        if User.prompt_continue(content, nums, n, save_path + save_name):
            if Util.file_exists(path, save_name):
                if not User.prompt_overwrite(path, save_name): save_name = User.prompt_save_name(save_name)
            # Merge
            try:
                files = Util.open_files(path, content)  # Opens files, do this as late as possible
                Util.merge_files(out_file, files, nums, n)
                out_file.write(save_path + "\\" + save_name + ".pdf")
                User.msg_complete()

                # Create new object for next merging operation
                out_file = Util.PdfFileMerger(strict=False)
            except Exception as err:
                print("Feil i sluttkode:")
                print(err)
                input()

