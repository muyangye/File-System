import typing

#Click `Run` in the top left corner to run the command line program. Output will appear in the "Program Output" tab in the right pane.

class File:
    def __init__(self, name, file_type, parent_id):
        self.name = name
        self.file_type = file_type
        # parent_id is the file_id of the folder the current file is in
        self.parent_id = parent_id
        # sub is solely for get_files() and print_files() complexity and runtime
        self.sub = []
        

class SigmaFileSystem:
    
    def __init__(self):
        # self.id can be understood as an auto-increment key just to keep file id unique
        self.id = 0
        # self.documents[file_id] <==> File(name, file_type, parent_id, sub)
        self.documents = {}
        # Create MyDocuments folder
        self.documents[self.id] = File("MyDocuments", "folder", None)
    
    # Feel free to modify the parameter/return types of these functions
    # as you see fit. Please add comments to indicate your changes with a 
    # brief explanation. We care more about your thought process than your
    # adherence to a rigid structure.
    
    # For runtime, n is the number of files in self.documents
    
    # @functionality: Get the total # of dashboards in the file system
    # @return: int <==> the total # of dashboards in the file system
    # @runtime: n
    def get_total_dashboards(self) -> int:
        res = 0
        for file_id, file in self.documents.items():
            if (file.file_type == "dashboard"):
                res += 1
        return res
    
    
    # @functionality: Get the total # of worksheets in the file system
    # @return: int <==> the total # of worksheets in the file system
    # @runtime: n
    def get_total_worksheets(self) -> int:
        res = 0
        for file_id, file in self.documents.items():
            if (file.file_type == "worksheet"):
                res += 1
        return res
    
    
    # @functionality: Given a file name, file type, and a folder’s unique id, add a new                         file of that type to the given folder
    # @return: None
    # @runtime: constant
    def add_new_file(self, fileName: str, fileType: str, folderId: int) -> None:
        # Check for errors
        if (folderId not in self.documents):
            print("The given folder doesn't exist in the file system")
            return -1
        if (self.documents[folderId].file_type != "folder"):
            print("The second parameter is not a folder")
            return -1
        
        # First increment self.id by 1 so that this new file has a unique file_id
        self.id += 1
        new_file = File(fileName, fileType, folderId)
        self.documents[self.id] = new_file
        # Also add that file to the sub of its folder
        self.documents[folderId].sub.append(new_file)

        
    # @funcitonality: Given the name of a file and the id of the folder it’s in, return                         the file’s id
    # @return: int <==> the file's id, if not found return -1
    # @runtime: n
    def get_file_id(self, fileName: str, folderId: int) -> int:
        # Check for errors
        if (folderId != None):
            if (folderId not in self.documents):
                print("The given folder doesn't exist in the file system")
                return -1
            if (self.documents[folderId].file_type != "folder"):
                print("The second parameter is not a folder")
                return -1
        
        for file_id, file in self.documents.items():
            if (file.name == fileName and file.parent_id == folderId):
                return file_id
        # If we reach this line it means the given file is not in the given folder
        print("Couldn't find the given file in the given folder")
        return -1

    
    # @functionality: Given a file id and a folder id, move the file into the folder with                       the given id
    # @return: None
    # @runtime: # of files in the original folder <==> remove_sub()
    def move_file(self, fileId: int, newFolderId: int) -> None:
        # Check for errors
        if (fileId not in self.documents):
            print("The file you want to move doesn't exist in the file system")
            return
        if (newFolderId not in self.documents):
            print("The destination folder doesn't exist in the file system")
            return
        if (self.documents[newFolderId].file_type != "folder"):
            print("The destination is not a folder")
            return
        
        file = self.documents[fileId]
        original_parent_id = file.parent_id
        # Remove the file from its original folder
        self.documents[original_parent_id].sub.remove(file)
        # Also add it to the sub of the new folder
        self.documents[newFolderId].sub.append(file)
        # Change its parent_id to the file_id of the new folder
        file.parent_id = newFolderId
        # Discovered by test_swap in line 219. Need to re-establish the relationship                 between current file, destination, and the current file's parent when the                 destination's parent is current file
        if (fileId == self.documents[newFolderId].parent_id):
            self.documents[newFolderId].parent_id = original_parent_id
            self.documents[original_parent_id].sub.append(self.documents[newFolderId])
            file.sub.remove(self.documents[newFolderId])

    
    # @functionality: Given a folder, return all the names of all files in that folder
    # @return: List[str] <==> all the names of all files in that folder
    # @runtime: # of files in the given folder
    def get_files(self, folderId: int) -> typing.List[str]:
        # Check for errors
        if (folderId not in self.documents):
            print("The given folder doesn't exist in the file system")
            return []
        
        res = []
        for file in self.documents[folderId].sub:
            res.append(file.name)
        return res
            
    
    # @functionality: Print out each file in the file system, showing the nested structure
    # @return: None
    # @runtime: n <==> print_files_helper()
    def print_files(self) -> None:
        # Start from MyDocuments
        self.print_files_helper(0, self.documents[0])
        
      
    # @functionality: Print the current file's name, then recursively go to the deeper                           files and print them using a wider indent until there are no files
    # @runtime: n
    def print_files_helper(self, count, file):
        # count is the # of spaces as indent
        print(count * "  " + file.name)
        for sub_file in file.sub:
            self.print_files_helper(count+1, sub_file)
    
    
    
# /////////////////////////////////////////////////////////
# /////////////////////   MY TESTS   //////////////////////
# /////////////////////////////////////////////////////////

# All "Check for errors" tests are performed by ask_question()
# Below are the actual funtionality tests

def test_nested():
    fs = SigmaFileSystem()
    root_id = fs.get_file_id("MyDocuments", None)
    fs.add_new_file("level1", "folder", root_id)
    level1_id = fs.get_file_id("level1", root_id)
    fs.add_new_file("level2", "folder", level1_id)
    level2_id = fs.get_file_id("level2", level1_id)
    fs.add_new_file("level3", "folder", level2_id)
    level3_id = fs.get_file_id("level3", level2_id)
    fs.add_new_file("level4", "folder", level3_id)
    level4_id = fs.get_file_id("level4", level3_id)
    fs.add_new_file("level5", "folder", level4_id)
    level5_id = fs.get_file_id("level5", level4_id)
    fs.move_file(level4_id, level2_id)
    fs.print_files()

    
def test_same_name_in_different_folder():
    fs = SigmaFileSystem()
    root_id = fs.get_file_id("MyDocuments", None)
    fs.add_new_file("folder1", "folder", root_id)
    fs.add_new_file("folder2", "folder", root_id)
    folder1_id = fs.get_file_id("folder1", root_id)
    folder2_id = fs.get_file_id("folder2", root_id)
    fs.add_new_file("samename", "worksheet", folder1_id)
    fs.add_new_file("samename", "dashboard", folder2_id)
    # Make sure they have different file_id
    print(fs.get_file_id("samename", folder1_id))
    print(fs.get_file_id("samename", folder2_id))
    

def test_swap():
    fs = SigmaFileSystem()
    root_id = fs.get_file_id("MyDocuments", None)
    fs.add_new_file("folder1", "folder", root_id)
    fs.add_new_file("folder2", "folder", root_id)
    folder1_id = fs.get_file_id("folder1", root_id)
    folder2_id = fs.get_file_id("folder2", root_id)
    fs.add_new_file("folder1_1", "worksheet", folder1_id)
    fs.add_new_file("folder1_2", "worksheet", folder1_id)
    fs.add_new_file("folder2_1", "dashboard", folder2_id)
    fs.move_file(folder1_id, folder2_id)
    fs.move_file(folder2_id, folder1_id)
    fs.print_files()
    
    
# There are many other valuable tests to do such as test_stress, but I don't want to spend   excessive amount of time in this assignment because I think the example is pretty         exhaustive and the file system is usable


    
# /////////////////////////////////////////////////////////
# // YOU DO NOT NEED TO MAKE CHANGES BELOW UNLESS NECESSARY
# /////////////////////////////////////////////////////////
    
def run_example():
    fs = SigmaFileSystem()
    
    rootId = fs.get_file_id("MyDocuments", None)
    fs.add_new_file("draft", "folder", rootId)
    fs.add_new_file("complete", "folder", rootId)
    draftId = fs.get_file_id("draft", rootId)
    completeId = fs.get_file_id("complete", rootId)
    fs.add_new_file("foo", "worksheet", draftId)
    fs.add_new_file("bar", "dashboard", completeId)
    fooId = fs.get_file_id("foo", draftId)
    fs.move_file(fooId, completeId)
    
    print(", ".join(fs.get_files(rootId)))
    print(", ".join(fs.get_files(draftId)))
    print(", ".join(fs.get_files(completeId)))
          
    fs.add_new_file("project", "folder", draftId)
    projectId = fs.get_file_id("project", draftId)
    for filename in ["page1", "page2", "page3"]:
        fs.add_new_file(filename, "worksheet", projectId)
    fs.add_new_file("cover", "dashboard", projectId)
    fs.move_file(projectId, completeId)
    projectId = fs.get_file_id("project", completeId)
    coverId = fs.get_file_id("cover", projectId)
    fs.move_file(coverId, rootId)
    
    print(", ".join(fs.get_files(rootId)))
    print(", ".join(fs.get_files(draftId)))
    print(", ".join(fs.get_files(completeId)))
    print(", ".join(fs.get_files(projectId)))

    print(fs.get_total_dashboards())
    print(fs.get_total_worksheets())
    fs.print_files()

def ask_for_int(question: str) -> int:
    val = input(question)
    try:
        return int(val)
    except:
        print('Please enter a valid integer value\n')
        return ask_for_int(question)
    
def ask_question():
    fs = SigmaFileSystem()
    running = True
    while(running):
        command = ask_for_int("\nEnter an integer to indicate a command: \n[1] get_total_dashboards\n[2] get_total_worksheets\n[3] add_new_folder\n[4] get_file_id\n[5] move_file\n[6] get_files \n[7] print_files\n[8] exit\n")
        if command == 1:
            totalDashboards = fs.get_total_dashboards()
            print("There are {0} dashboards in the file system.".format(totalDashboards));
        elif command == 2:
            totalWorksheets = fs.get_total_worksheets()
            print("There are {0} worksheets in the file system.".format(totalWorksheets));
        elif command == 3:
            fileName = input("Enter a new file name: ")
            fileType = input("Enter a file type (worksheet, dashboard, or folder): ")
            folderId = ask_for_int("Enter a folder id where you'd like to put this file: ")
            fs.add_new_file(fileName, fileType, folderId);
            print("{0} has been added to folder {1}".format(fileName, folderId))
        elif command == 4:
            fileName = input("Enter the file name: ")
            folderId = ask_for_int("Enter the folder id: ")
            fileId = fs.get_file_id(fileName, folderId)
            print("{0} is file {1}".format(fileName, fileId));
        elif command == 5:
            fileId = ask_for_int("Enter a file id:")
            newFileId = ask_for_int("Enter the folder id where you'd like to move this file: ")
            fs.move_file(fileId, newFileId);
            print("Successfully moved file {0} to folder {1}".format(fileId, newFileId))
        elif command == 6:
            folderId = ask_for_int("Enter a folderId:")
            fileNames = fs.get_files(folderId)
            if (len(fileNames) == 0):
                print("There are no files in folder {0}".format(folderId))
            else:
                print("The following files are in folder {0}: ".format(folderId))
                for fileName in fileNames:
                    print("\t{0}".format(fileName))
        elif command == 7:
            fs.print_files()
        elif command == 8:
            print("Exiting program.")
            running = False
        else:
            print("Invalid command: {0}. Please try again.\n".format(command))
              
ask_question()
# run_example()
# test_nested()
# test_same_name_in_different_folder()
# test_swap()