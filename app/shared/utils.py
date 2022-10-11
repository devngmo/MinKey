from datetime import date, datetime
import json, re, yaml
import os, socket, colorama
from colorama import Fore, Style

def custom_json_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError (f"Type '{obj}' not serializable")

def clearScreen():
    try:
        os.system('cls')
    except:
        os.system('clear')

def e(x):
    if isinstance(x, str):
        print(Fore.RED + x)
    elif isinstance(x, dict) or isinstance(x, list):
        print(Fore.RED + json.dumps(x, indent=2, default=custom_json_serializer))
    else:
        print(Fore.RED + str(x))
    print(Fore.WHITE)

def hl(x):
    if isinstance(x, str):
        print(Fore.YELLOW + x)
    elif isinstance(x, dict) or isinstance(x, list):
        print(Fore.YELLOW + json.dumps(x, indent=2, default=custom_json_serializer))
    else:
        print(Fore.YELLOW + str(x))
    
    print(Fore.WHITE)

def i(x):
    if isinstance(x, str):
        print(Style.DIM + x)
    elif isinstance(x, dict) or isinstance(x, list):
        print(Style.DIM + json.dumps(x, indent=2, default=custom_json_serializer))
    else:
        print(Style.DIM + str(x))
    print(Style.NORMAL)

def getEnvBool(key, defaultValue):
    if key in os.environ:
        v = ('%s' % os.environ[key]).lower()
        return v == '1' or v == 'true'
    return defaultValue

def getEnvValue(key, defaultValue):
    if key in os.environ:
        return os.environ[key]
    return defaultValue


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def ymd2date(ymd:str):
    dateFormat = '%Y%m%d'
    if len(ymd) > 8:
        dateFormat = '%Y%m%d_%H%M'
    return datetime.strptime(ymd, dateFormat)



def dictGetStr(src:dict, key, defaultValue):
    if key in src:
        if src[key] == None or src[key] == '':
            return defaultValue
        return src[key]
    return defaultValue

def dictGetInt(src:dict, key, defaultValue):
    if key in src:
        if src[key] == None:
            return defaultValue
        return src[key]
    return defaultValue

def loadYaml(fp):
    with open(fp, encoding='utf8') as f:
        text = f.read()
        return yaml.load(text, yaml.SafeLoader)

def writeYaml(model, fp):
    with open(fp, 'w', encoding='utf8') as f:
        yaml.dump(model, f)

def loadText(fp):
    with open(fp, encoding='utf8') as f:
        return f.read()

def writeText(fp, text):
    with open(fp, 'w', encoding='utf8') as f:
        f.write(text)
        f.close()

regexEmailAddress = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
def isValidEmailAddress(text):
    return re.search(regexEmailAddress, text)        