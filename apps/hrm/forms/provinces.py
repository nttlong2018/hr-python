# -*- coding: utf-8 -*-
from quicky import layout_view
from . import category

layout=layout_view.create("hrm","provinces")
layout.create(dict(
    collection="list.provinces",
    columns=layout_view.extend_columns(
        category.basic_columns,
        [dict(
            caption="Postal Code",
            name="PostalCode",
            display_index=2010
        )]
    ),
    form=dict(
        rows=[
            dict(
                col_md=[2,4,2,4],
                col_sm=[4,8],
                col_xs=[4,8],
                fields=[
                    dict(name="Code"),
                    dict(name="Name")
                ]
            ),
            dict(
                col_md=[2, 10],
                col_sm=[4, 8],
                col_xs=[4, 8],
                fields=[
                    dict(name="PostalCode")
                ]
            ),
            dict(
                col_md=[2,10],
                col_sm=[4, 8],
                col_xs=[4, 8],
                fields=[
                    dict(name="Description",
                         type="text-area")
                ]
            )
        ]
    )
))