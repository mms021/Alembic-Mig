import os 
import io
import codecs


dropAllFunctions = "Sql/drop_all_functions.sql"
storedProcedure = "Sql/StoredProcedure"
table = "Sql/Table"
view = "Sql/View"
initData = "Sql/InitData"



def clean_bd(context , path = dropAllFunctions):
    bytes = min(32, os.path.getsize(path))
    raw = io.open(path, 'rb').read(bytes)

    if raw.startswith(codecs.BOM_UTF8):
        encoding = 'utf-8-sig'
    elif raw.startswith(codecs.BOM_LE):
        encoding = 'utf-16'
    else:
        encoding = 'utf-8'

    infile = io.open(path, 'r', encoding=encoding)
    data = infile.read()
    infile.close()
    #context.execute(data.replace(':', '\:'))
    context.execute(data)

def pload_plain_sql(context):
    
    n = os.listdir(path="Sql") 
    def filework(n):
        for root, dirs, files in os.walk(n):
            for file in files:
                if file.endswith(".sql"):
                    try:
                        clean_bd(context , os.path.join(root, file) )
                        print(os.path.join(root, file))
                    except Exception as f:
                        print(f'ERROR____ {file} {f}')
                    
   
    if 'StoredProcedure' in n:
        print(f'1========================={storedProcedure}')
        filework(storedProcedure)
    if 'Table' in n:
        print(f'2========================={table}')
        filework(table)
    if 'View' in n:
        print(f'3========================={view}')
        filework(view)
    if 'initData' in n:
        filework(initData)
        print(f'4========================={initData}')







