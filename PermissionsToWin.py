import subprocess as sp

from SyncsFoldersV1 import MFolders


def LetPerForDir(Path):
    _data = sp.run(fr"icacls {Path}  /t /grant {MFolders().Name}:F",
                   stdin=sp.PIPE,
                   stdout=sp.PIPE,
                   stderr=sp.PIPE)

    if _data.stderr.decode():
        return _data.stderr.decode()

    return "OK."


def LetPerForApp(AppExe):
    _data = sp.run(f"powershell.exe start-Process {AppExe} -Verb runas",
                   stdin=sp.PIPE,
                   stdout=sp.PIPE,
                   stderr=sp.PIPE)

    if _data.stderr.decode():
        return "NO."

    return "OK."



