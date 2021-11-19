import os , json , io , codecs
os.system("python3 -m  Sql.sql_upload")
os.system("python3 -m  PostInitDatas.PostInitData")
os.system("python3 -m  PreInitDatas.PreInitData")
os.system("python3 -m  Policy.Policy_instal")


from Sql.sql_upload import clean_bd , pload_plain_sql
from PostInitDatas.PostInitData import Post_InitData_cont
from PreInitDatas.PreInitData import Pre_InitData_cont
from Policy.Policy_instal import Pol_instal


config_dir = os.path.dirname(__file__)
def get_config_file():
    if os.path.exists("appsettings.local.json"):
        json_file = os.path.join(config_dir, 'appsettings.json')
        with open(json_file) as f:
            return [i.split('=')  for i in json.load(f)["ConnectionStrings"]['DefaultConnection'].split(';')]
    else: 
        json_file = os.path.join(config_dir, 'appsettings.json')
        with open(json_file) as f:
            return [i.split('=')  for i in json.load(f)["ConnectionStrings"]['DefaultConnection'].split(';')]



def script_bd(context , path ):
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
    context.execute(data)


def include_name(name, type_, parent_names):
    if type_ == "schema":
        # this **will* include the default schema
        return name in [None, "base", "conf_lc", 'refbook' ]
    else:
        return True

