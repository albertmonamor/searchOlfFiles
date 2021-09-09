import os
import threading
from time import sleep
from shutil import copy2
from time import time


def chType(obj):
    """
        Aggressive  checking !
    """
    if os.path.isfile(obj):
        return True
    elif os.path.isdir(obj):
        return False
    else:
        try:
            File = open(obj)
            File.close()
            return True

        except PermissionError and OSError:
            return False
        except FileNotFoundError:
            # IDK ? maybe need True
            return False


############################
#   ~  MAIN CLASS #########
class MFolders(object):
    """
        class FOR Mapping Tree of Files And Folder that Into specific folder; using os.walk for recursion
            ...
            RETURN
                self.TREE = list Contains All
                    self.lisOfFiles = list Contains dict 2 value 'folder'=str, 'files'=list > contain Dict[6 values]
                        self.li = list Contains dict 6 values [see in code]

    """

    def __init__(self):
        self.Name = os.getlogin()
        self.lisOfFiles = []
        self.li = []
        self.TREE = []

        # for obj
        self.SMapping_f = 0
        self.SMapping_d = 0

    def __GetFolder(self, Folder):

        _xFile = 0
        _xFolder = 0
        self.li = []
        self.lisOfFiles = []
        for folder in os.walk(Folder):
            self.li = []

            # For info()
            self.SMapping_d += 1
            #
            for _file in os.listdir(folder[0]):
                # For info()
                self.SMapping_f += 1
                #
                try:
                    fPath = fr"{folder[0]}\{_file}"
                    self.li.append({"name": _file,
                                    "size": os.path.getsize(fPath),
                                    "time_cr": os.path.getctime(fPath),
                                    "time_ch": os.path.getmtime(fPath),
                                    "time_opn": os.path.getatime(fPath),
                                    "type": chType(fPath),
                                    "sub": fPath[
                                           fPath.rfind(os.path.basename(Folder)) + len(os.path.basename(Folder)) + 1:],
                                    "parent": _xFile})
                except FileNotFoundError as e:
                    f"{e}"
                    pass
            else:
                pass

            self.lisOfFiles.append({"folder": folder[0], "files": self.li})
            _xFolder += 1

        self.lisOfFiles.append({"num_F1": _xFolder, "num_F2": _xFile})
        return self.lisOfFiles

    def GetFolders(self, *folders):

        """
            Folders { tuple, list }
        """
        self.TREE = []
        for folder in folders:
            self.TREE.append(MFolders.__GetFolder(self, folder))

        return self.TREE


class SyncFolders(MFolders):
    """
        work with class MFolder

    """

    def __init__(self, obj=None):
        MFolders.__init__(self)
        self.liFilesMain = []
        self.slash = os.altsep
        self.OBJ = obj
        self.SCopy = 0
        self.XNum = 0

    def Sync(self, folder, RSL=True):
        """
            RSL => Index OF -R_oot- folder in List Of parameter `folder`;
                   Index OF -S_ub Folder- [..];
                   Index OF -(for) L_oop- [..]
        """
        if RSL:
            indexR = 0
            indexS = 1
            indexL = 1

        else:
            indexR = 1
            indexS = 0
            indexL = 0

        Root = folder[indexR]
        FolderTS = folder[indexS][0]['folder']
        for __ in folder[indexL][0]:

            for _ in Root:

                if "files" not in _.keys():
                    break
                # [+] for debug
                # LENS = len(folder[indexL][self.XNum]['files']) == len(_['files'])
                # print(LENS, len(_['files']), len(folder[indexL][self.XNum]['files']))

                for create in _['files']:

                    c_s = create['sub']
                    Path = rf"{FolderTS}\{c_s}"

                    if not create['type']:
                        if not os.path.exists(Path):
                            os.mkdir(Path)
                    else:
                        if os.path.exists(Path) and create['type']:
                            if not create['size'] == os.path.getsize(Path):
                                os.system(rf"del {Path}")

                        if not os.path.exists(Path):
                            self.SCopy += 1
                            copy2(f"{_['folder']}\\{create['name']}",
                                  f"{FolderTS}\\{c_s[:c_s.rfind(self.slash) + 1]}")

            break

    def Info(self):
        """
            ## FOR GUI ##
                return str; can to split By " | "
        """
        threading.Thread(target=self.ClearInfo).start()
        return f"{self.SMapping_f:,}|{self.SMapping_d:,}|{self.SCopy}"

    def ClearInfo(self):
        sleep(2)
        self.SMapping_d = 0
        self.SMapping_f = 0
        self.SCopy = 0


class SyncPictureIOS(MFolders):

    def __init__(self, RM=True):
        """
            types of extends {3}
        """
        # // base64-encode of changes with specific picture
        # // video
        # // picture

        # self.var
        MFolders.__init__(self)
        self.slash = "\\"
        self.FilesType = {}
        self.Dirs = {}
        self.Files = 0
        self.RM = RM
        self.mf = None

    def FilterOfTypes(self, folder: list):
        self.mf = folder[0][0]['folder']
        self.__paths(self.mf)
        for _list in folder:  # // 0 is key of files and folders. 1 is num of file and folder
            x = 0
            for _dict in _list:
                self.Files = _list[-1]['num_F2']  # maybe length list is > 2

                if "files" not in str(_dict.keys()):
                    break

                for _ in _dict['files']:
                    x += 1  # // just for math
                    print(f"{int(x * 100 / self.Files)}.0 %")

                    # short variable
                    Path = fr"{self.mf}\{_['sub'][:_['sub'].rfind(self.slash) + 1]}{_['name']}"
                    # >> == 1). {folder} c:\Users\..
                    #       2). {sub} \
                    #       3). {name} file.ending

                    # file.AAE remove + copy
                    _['name'] = _['name'].upper()
                    if _['name'].endswith(self.FilesType['aae']) and _['type']:
                        self._ClearFileAndCheck(Path, self.Dirs['AAE_ios'], _)

                    # file.MOV
                    elif _['name'].endswith(self.FilesType['mov']) and _['type']:
                        self._ClearFileAndCheck(Path, self.Dirs['MOV_ios'], _)

                    # file.JPG
                    elif _['name'].endswith(self.FilesType['jpg']) or \
                            "JPEG" in str(_['name']) or "PNG" in str(_['name']) and _['type']:
                        self._ClearFileAndCheck(Path, self.Dirs['JPG_ios'], _)

                    # file.MP4
                    elif _['name'].endswith(self.FilesType['mp4']) and _['type']:
                        self._ClearFileAndCheck(Path, self.Dirs['MP4_ios'], _)

                    else:
                        print(_['name'])

    def _ClearFileAndCheck(self, P, TP, v):

        # **
        # copy with high-level {permissions + metadata + dst} and removed\
        if not os.path.exists(f"{TP}{v['name']}") or os.path.exists(f"{P}") and self.RM:
            if v['size'] > 0:
                copy2(f"{P}", TP)

                if self.RM:
                    os.remove(f"{P}")

                print(fr"[INFO] copied "+"and remove" if self.RM else ""+f" > {P} {TP}")

    def __paths(self, mf):
        xPath = os.path.dirname(mf)
        for ty, Dir in zip(['.AAE', '.MOV',
                            '.JPG', '.MP4'],
                           [fr'{xPath}\AAE_ios',
                            rf"{xPath}\MOV_ios",
                            rf"{xPath}\JPG_ios",
                            rf"{xPath}\MP4_ios"]):

            self.FilesType[ty[1:].lower()] = ty
            self.Dirs[os.path.basename(Dir).lower()] = Dir
            if not os.path.exists(Dir):
                os.mkdir(Dir)


# API
def SearchOldFile(Path):
    # HALF_MONTH = 1264500.0
    # ~
    MONTH = 2592000
    # ~
    HALF_YEAR = MONTH * 6
    # ~
    YEAR = MONTH * 12
    # -
    x = 0
    AllMap = MFolders().GetFolders(Path)
    for _list in AllMap:
        for _dict in _list:
            x += 1
            if "files" not in _dict.keys():
                break

            if x == 1:
                yield _list[-1]['num_F2']

            for _ in _dict['files']:

                if time()-MONTH < _['time_ch'] or time()-MONTH < _['time_opn']:
                    yield {"status": "used in last", "path": f"{_dict['folder']}\\{_['name']}",
                           "size": _['size'], "level": 0}

                elif time()-HALF_YEAR < _['time_opn'] < time()-MONTH or time()-HALF_YEAR < _['time_ch'] < time()-MONTH:
                    yield {"status": "Proper", "path": f"{_dict['folder']}\\{_['name']}",
                           "size": _['size'], "level": 1}

                elif time()-YEAR < _['time_opn'] < time()-HALF_YEAR or time()-YEAR < _['time_ch'] < time()-HALF_YEAR:
                    yield {"status": "Invalid", "path": f"{_dict['folder']}\\{_['name']}",
                           "size": _['size'], "level": 2}

                elif time()-YEAR > _['time_opn'] or time()-YEAR > _['time_ch']:
                    yield {"status": "Garbage", "path": f"{_dict['folder']}\\{_['name']}",
                           "size": _['size'], "level": 3}


if __name__ == "__main__":
    if input("::>") == "S":
        s = SyncFolders()
        a = s.GetFolders(rf"c:\Users\{s.Name}\Desktop\_new",)
        print(a)
    else:
        pass

"""for i in a:
    for q in i:
        print(q)
        if "files" in q:
            for _ in q['files']:
                print(_)"""