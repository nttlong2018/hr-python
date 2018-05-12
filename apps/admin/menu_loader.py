import json
import os
__menu_items__=[

    {
        "caption":"Privileges",
        "items":[
            {
                "page":"categories/users",
                "caption":"Users"
            },{
                "page":"categories/roles",
                "caption":"Roles"
            },{
                "page":"categories/views",
                "caption":"Pages"
            }
        ]

     },
    {
        "caption":"content",
        "items":[
            {
                "page":"Course",
                "caption":"Course ware"
            },{
                "page":"Wiki",
                "caption":"wiki"
            }
        ]
    },{
        "caption":"Settings",
        "items":[
            dict(
                page="form/config",
                caption="Settings"
            )
        ]
    }

]

def load_menu_items():
    # global __menu_items__
    # dir= os.path.dirname(__file__)
    # with open(dir+"/menu.json") as json_data:
    #     __menu_items__ = json.load(json_data)["items"]

    return __menu_items__
