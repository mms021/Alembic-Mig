import os
import io
import codecs



def clean_bd(context , path):
    bytes = min(32, os.path.getsize(path))
    raw = io.open(path, 'rb').read(bytes)

    if raw.startswith(codecs.BOM_UTF8):
        encoding = 'utf-8-sig'
    elif raw.startswith(codecs.BOM_LE):
        encoding = 'utf-16'
    else:
        encoding = 'utf-8'
    #context.execute(os.system(open(dropAllFunctions, 'r').read()))
    infile = io.open(path, 'r', encoding=encoding)
    data = infile.read()
    infile.close()
    #context.execute(data.replace(':', '\:'))
    context.execute(data)

 
def Post_InitData_cont(context):
    root = "PostInitDatas"
    n = os.listdir(path=root) 
    for file in n:
        if file.endswith(".sql"):
            try:
                clean_bd(context , os.path.join(root, file) )
                print(  os.path.join(root, file))
            except Exception as f:
                print(f'ERROR____ {file} {f}')
            
                  