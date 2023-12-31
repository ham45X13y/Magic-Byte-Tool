import argparse
from os.path import exists, realpath, dirname, basename
from os import rename
import filetype

"""
Note: requires python 3.9+
"""

filetypelist={
    'heic':b'\x00\x00\x00\x20\x66\x74\x79\x70\x68\x65\x69\x63',
    'bmp':b'\x42\x4d',
    'fits':b'\x53\x49\x4d\x50\x4c\x45',
    'gif':b'\x47\x49\x46\x38',
    'gks':b'\x47\x4b\x53\x4d',
    'jpeg':b'\xff\xd8\xff\xe0',
    'jpg':b'\xff\xd8\xff\xe0',
    'nif':b'\x49\x49\x4e\x31',
    'png':b'\x89\x50\x4e\x47',
    'sol':b'\x00\xBF',
    'xlsx':b'\x09\x08\x10\x00\x00\x06\x05\x00',
    'xls':b'\x09\x08\x10\x00\x00\x06\x05\x00',
    'pdf':b'\x25\x50\x44\x46',
    '7z':b'\x37\x7A\xBC\xAF\x27\x1C',
    'pm':b'\x56\x49\x45\x57',
    'xcf':b'\x67\x69\x6d\x70\x20\x78\x63\x66\x20\x76',
    'xpm':b'\x2f\x2a\x20\x58\x50\x4d\x20\x2a\x2f',
    'bzip':b'\x42\x5a',
    'gz':b'\x1f\x8b',
    'zip':b'\x50\x4b\x03\x04',
    'tar':b'\x75\x73\x74\x61\x72',
    'elf':b'\x7f\x45\x4c\x46',
}

exceptiontype_list=['jpg','xls','7z','xcf']
# MIME Type is different written than in the extension table above


def verify_file(file,file_type) -> bool:
    print("[-] Starting verification process")
    level=0
    match=False

    with open(file,"rb") as f:
        file_content=f.read()
    firstline_hex=list([i for i in file_content])

    if check_match(filetypelist[file_type], firstline_hex):
        match=True
        print('[+] Verification: first bytes are correct')
        level+=1

    def check_multilayer_match(bytestream_filetype,firstline_file):
        for i in filetypelist:
            if check_match(firstline_file[len(bytestream_filetype):],filetypelist[i]):
                return True
            else:
                continue
        return False

    if match:
        if check_multilayer_match(filetypelist[file_type], firstline_hex):
            print("[-] Verification: Found overhead of magic_bytes in file")
        else:
            level +=1
            print("[+] Verification: No other magic bytes found at filestart")

    kind=filetype.guess(str(file))

    if not kind:
        print("[-] Information: The Filetype seems to supported by this tool but not the python library used to detect the MIME-Type and extension")
        return level >=2

    if str(kind.extension) == str(file_type):
        print('[+] Verification: extension is correct (this has no impact on the verification process)')
    

    if file_type not in exceptiontype_list:
        if str(kind.mime).split("/")[len(str(kind.mime).split("/"))-1] == str(file_type):
            level +=1
            print('[+] Verification: MIME Type found is correct')
        else:
            print(f"[-] MIME type found ({kind.mime}) doesnt seem to match with the given type")
        return level>=3
    
    return level >=2


def print_supported_extensions():
    c=0
    print("Supported File Types: ")
    print("-"*22)
    for key in filetypelist:
        print((f"{c}".ljust(4)+f"| {key}".ljust(7) + f"| {filetypelist[key]}"))
        c+=1


def get_bytes(args):
    if args.list:
        print_supported_extensions()
        exit(0)

    if not args.file:
        print("[!] Error: Missing parameters")
        exit(1)

    if args.remove:
        remove_bytes_from_file(args.file)
        exit(0)

    if not args.type:
        print("[!] Error: Missing parameters")
        exit(1)

    try:
        appendbytes=filetypelist[args.type]
    except KeyError as e:
        print("[!] Error: Filetype not found or not supported")
        exit(1)
    
    return appendbytes


def check_match(list_1:list,list_2:list) -> bool:
    c=0
    if len(list_1) < len(list_2):
        for i in list_1:
            if i == list_2[c]:
                c+=1
                continue
            else:
                return False
    else:
        for i in list_2:
            if i == list_1[c]:
                c+=1
                continue
            else:
                return False
    
    return True


def remove_bytes_from_file(file:str):
    f_type=""
    file_content=None
    with open(file,'rb') as f:
        f.seek(0)
        file_content=f.readlines()

        firstline_hex=list([i for i in file_content][0])
        
        for i in filetypelist:
            if check_match(firstline_hex,list(filetypelist[i])):
                f_type=i
                break

        if f_type == "":
            print(f"[-] Status: Magic Bytes at start could not be found in {file}")
            return
        
    f = open(file, 'rb')
    a=len(filetypelist[f_type])
    f.seek(a) 

    remainder = f.read()
    with open(file,'wb') as f:
        f.write(remainder)
    print("[+] Successfully removed bytes from file")


def main():

    parser = argparse.ArgumentParser(prog='Magic Byte Appender', description='Select File, select type and get your file in that type as output', epilog='Further Information: https://en.wikipedia.org/wiki/List_of_file_signatures')
    
    parser.add_argument('-f','--file',type=str, help="The File that should be changed")
    parser.add_argument('-t','--type',type=str, help="Type to convert into")
    parser.add_argument('-e','--extension',action=argparse.BooleanOptionalAction, help="Set if you want to also overwrite the extension of your file")
    parser.add_argument('-v','--verify',action=argparse.BooleanOptionalAction, help="Set if you want to verify that the convertion worked correctly as intented. Checks with TODO")
    parser.add_argument('-l','--list',action=argparse.BooleanOptionalAction, help='Get a detailed list of all supported file types')
    parser.add_argument('-r','--remove', action=argparse.BooleanOptionalAction, help='removes existing magic-bytes from file if they exist')
    args=parser.parse_args()
    
    appendbytes=get_bytes(args)
    
    file=args.file
    if not exists(file):
        print("[!] Error: File provided could not be found or does not exist")
        exit(1)

    # write 
    with open(file,'rb') as f:
        content=f.read()
    
    # check if magic_bytes exists
    found=False
    for i in filetypelist:
        if check_match(list(content),list(filetypelist[i])):
            found=True
            rm_bool=str(input(f'Magic bytes of type {i} found. Remove them? [Y/n]  ')).strip()
            if rm_bool in ['Y','y','']:
                remove_bytes_from_file(file)
            break
    
    if not found:
        print('[-] No existing Magic Bytes found at the beginning of the file')
    else:
        with open(file,'rb') as f:
            content=f.read()

    with open(file,'+bw') as f:        
        f.write(appendbytes)
        f.write(content)
        print(f"[+] Successfully written to {file}")

    new_file=file

    # change extension
    if args.extension:
        file=basename(realpath(file))
        new_filename=(str(file).split('.')[0])+"."+str(args.type)
        directory=str(dirname(realpath(file)))+'/'
        new_file=directory+new_filename
        rename(directory+file,new_file)
        print(f"[+] Successfully changed extension")

     # verify
    if args.verify:
        if verify_file(new_file,str(args.type)):
            print("[+] Successfully verified. Magic bytes seem correct")
        else:
            print("[-] Verificationcheck did not pass")


if __name__ == '__main__':
    main()
    exit(0)
