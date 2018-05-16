# -*- coding: utf-8 -*-
from helpers import validators
validators.create_model("test",
                        {
                            "Code":"text",
                            "Name":"text",
                            "Gender":"bool",
                            "WorkingInfo.DepartmentCode":"text",
                            "WorkingInfo.LoginList":"list"

                        })
ret=validators.validate_type_of_data("test",{
    "WorkingInfo":{
        "DepartmentCode":"tffghj",
        "LoginList":[
            {
                "LoginTime":"dasda"
            }
        ]

    }

})
print(ret)