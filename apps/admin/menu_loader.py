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
                    "page":"pages/roles",
                    "caption":"Roles"
                },{
                    "page":"pages/views",
                    "caption":"Views"
                }
            ]

         },{
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
    }

]

def load_menu_items():
    # global __menu_items__
    # dir= os.path.dirname(__file__)
    # with open(dir+"/menu.json") as json_data:
    #     __menu_items__ = json.load(json_data)["items"]

    return __menu_items__
