import psutil
import ctypes
import os
import sys
import requests

def banner():
    print(' _____ _____ _____ _____ _       _         _   ')
    print('|     |     | __  |   __|_|___  |_|___ ___| |_ ')
    print('| | | |   --| __ -|   __| |   | | | -_|  _|  _|')
    print('|_|_|_|_____|_____|_____|_|_|_|_| |___|___|_|  ')
    print('    by roooot.dev             |___|            ')
    print('')

def getpid(name: str) -> int:
    for proc in psutil.process_iter():
        if proc.name() == name:
            return proc.pid
            
    return None

def isdll(path: str) -> bool:
    if not path.endswith(".dll"):
        return False
    try:
        with open(path, 'rb') as bytesfile:
            signature = bytesfile.read(2)
            return signature == b'MZ'
    except:
        print(f'[ - ] [ {path} ] cant read file')
        sys.exit(1)

def inject(path: str, name: str) -> None:
    if not path:
        print('[ - ] no path specified')
        sys.exit(1)
    if not os.path.exists(path):
        print(f'[ - ] [ {path} ] path doesnt exist')
        sys.exit(1)
    if not isdll(path):
        print(f'[ - ] [ {path} ] not a dll file')
        sys.exit(1)

    pid = getpid(name)
    if pid is None:
        print(f'[ - ] [ {name} ] process doesnt exist')
        sys.exit(1)

    DLL_INJECTOR = ctypes.WinDLL((os.path.dirname(__file__) + '/libs/dll_injector.dll').replace("\\", "/"))
    DLL_INJECTOR.InjectDLL.argtypes = [ctypes.c_char_p, ctypes.c_int]
    DLL_INJECTOR.restype = ctypes.c_int
    DLL_INJECTOR.InjectDLL(path.encode(), pid)

def main():
    os.system('cls' if os.name=='nt' else 'clear')
    banner()
    name = "Minecraft.Windows.exe"
    path = input(f'[ ! ] [ {getpid(name)} ] input dll path: ')
    
    print(f'[ i ] [ {getpid(name)} ] targeting {name}')

    inject(path, name)
    print(f'[ i ] [ {getpid(name)} ] injected with {path}')

if __name__ == "__main__":
    main()
