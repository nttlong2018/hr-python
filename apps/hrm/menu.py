# -*- coding: utf-8 -*-
import argo
menu_items=[
    dict(
        caption="Danh mục",
        items=[
            dict(
                caption="Tỉnh thành",
                page="categories/provinces"
            ),
            dict(
                caption="Quận huyện",
                page="categories/disctricts"
            )
        ]
    )
]
from  . import list_config

list_config.regist_lits("provinces",dict(
    collection="list.provinces",
    columns=list_config.extend_columns(
        list_config.basic_cloumns,
        [dict(
            caption="Postal Code",
            field="PostalCode"
        )]
    )
))
