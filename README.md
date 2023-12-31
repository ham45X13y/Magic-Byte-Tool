## What is this Tool?

The tool is an easy way to append and/ or remove magic-bytes that determine a filetype in most filetype checks. This can be used to bypass certain file restrictions (e.g. fileupload filtering)


## Features:
- Append magic magic-bytes of different types
- Remove existing magic-bytes
- Overwrite existing magic-bytes
- Change the file-extension 
- Verify that the file is set up correctly

## Usage:

### Example:

- ```python3 magic_byte_tool.py  -f shell.php -t gif -e -v```
- ```python3 magic_byte_tool.py  -l```
- ```python3 magic_byte_tool.py  -r shell.gif```


### Options:   
  ```-h, --help```  show this help message and exit   
  ```-f FILE, --file FILE``` The File that should be changed   
  ```-t TYPE, --type TYPE``` Type to convert into   
  ```-e, --extension``` Set if you want to also overwrite the extension of your file   
  ```-v, --verify``` Set if you want to verify that the convertion worked correctly as intented.Checks with TODO   
  ```-l, --list``` Get a detailed list of all supported file types   
  ```-r, --remove``` removes existing magic-bytes from file if they exist   

Further Information:   
https://en.wikipedia.org/wiki/List_of_file_signatures

## Supported File Types:

|type | magic bytes|
|----------|-------------------------|
|heic      | b'\x00\x00\x00 ftypheic'|
|bmp       | b'BM'|
|fits      | b'SIMPLE'|
|gif       | b'GIF8'|
|gks       | b'GKSM'|
|jpeg/jpg  | b'\xff\xd8\xff\xe0'|
|nif       | b'IIN1'|
|png       | b'\x89PNG'|
|sol       | b'\x00\xbf'|
|xlsx/ xls | b'\t\x08\x10\x00\x00\x06\x05\x00'|
|pdf       | b'%PDF'|
|7z        | b'7z\xbc\xaf'\x1c'|
|pm        | b'\x56\x49\x45\x57'|
|xcf       | b'\x67\x69\x6d\x70\x20\x78\x63\x66\x20\x76'|
|xpm       | b'\x2f\x2a\x20\x58\x50\x4d\x20\x2a\x2f'|
|bzip      | b'\x42\x5a'|
|gz        | b'\x1f\x8b'|
|zip       | b'\x50\x4b\x03\x04'|
|tar       | b'\x75\x73\x74\x61\x72'|
|elf       | b'\x7f\x45\x4c\x46'|