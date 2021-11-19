import os , io
import json
from psycopg2.extras import Json
import codecs
import psycopg2

maps = {
    "base.module_install":
        ["Policy/api_base.json",
	    "Policy/api_lifecycle.json",
		"Policy/api_refbook.json"
        ],
    "base.application_install":[
        "Policy/application.json"
    ],
    "base.gp_install":[
        #//========gp_base=======================
		"Policy/gp_base_base.json",
		#//========gp_read_nsi===================
		"Policy/gp_read_nsi_base.json",
		"Policy/gp_read_nsi_lifecycle.json",
		"Policy/gp_read_nsi_refbook.json",
		#//========gp_cmd_xxx====================
		"Policy/gp_cmd_base.json",
		"Policy/gp_cmd_participants.json",
		"Policy/gp_cmd_object_settings.json",
		"Policy/gp_cmd_statuses.json",
		"Policy/gp_cmd_life_cycles.json",
		"Policy/gp_cmd_refbook.json",
    ],
    "base.organization_install":[
        'Policy/organization.json'
    ],
} 

def Pol_instal(cursor):
    for key, value in maps.items():
        for vs in value:
            try:
                f  = json.load(codecs.open(vs, 'r', 'utf-8-sig'))
                cursor.execute(f'select * from {key} (%s::json)', ( Json(f),))
                print(f'{vs}     PR:{key}')
            except Exception as f:
                print(f'ERROR____ {key} {f}')

