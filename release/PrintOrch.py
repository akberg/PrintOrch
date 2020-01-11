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

import os
while 1:
    alt = User.display(path, save_path, work, save_name, content, nums, n)

    if alt == 0: # Exit
        out_file.close()
        exit(0)


    elif alt == 1: # Fetch folder
        try:
            path = diropenbox()
        except Exception as e:
            input()
        if path != "":  # Make sure a valid folder was chosen
                        # Read and interpret available meta-info
            try: 
                work = os.path.basename(path)                       # Determine work name based on folder name
                save_name = "_".join(work.split()) + "_printready"  # Generic name for save file
                content = Util.get_content(path)                    # Get the folder's content
                n = len(content)
                nums = [1]*n                                        # Initialize array for num copies
                                                                    # TODO: Save numbers relatied to instruments in settings and reload as guess next time
            except Exception as e:
                input()


    elif alt == 2:  # Saving directory
        save_path = User.prompt_save_dir()


    elif alt == 3:  # Save file name
        save_name = User.prompt_save_name(save_name)


    elif alt == 4: # Change number of copies
        # TODO: Enable better navigation for convenience
        print("Angi tomt felt for å ikke endre verdi.")
        for i in range(n):
            nums[i] = User.prompt_num(Util.get_instrument(content[i], work), nums[i])   # For each loaded file, prompt num copies
    
    
    elif alt == 5: # Fullføre
        if User.prompt_continue(content, nums, n, save_path + save_name):
            if Util.file_exists(path, save_name):
                if not User.prompt_overwrite(path, save_name): save_name = User.prompt_save_name(save_name)
            # Merge
            try:
                files = Util.open_files(path, content)  # Opens files, do this as late as possible
                Util.merge_files(out_file, files, nums, n)
                out_file.write(os.path.join(save_path, save_name + ".pdf"))     # Write PDF file to chosen path with chosen name
                User.msg_complete()
                out_file = Util.PdfFileMerger(strict=False)                     # Create new object for next merging operation
            except Exception as err:
                # TODO: Make better error handling
                print("Feil i sluttkode:")  
                print(err)
                input()

