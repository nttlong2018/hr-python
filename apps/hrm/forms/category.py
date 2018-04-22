# -*- coding: utf-8 -*-
from quicky import layout_view
basic_columns=[
    dict(
        caption="Mã",
        name="Code",
        display_index=100,
        display_in_table=True,
        display_in_form=True
    ),
    dict(
        caption="Tên",
        name="Name",
        display_index=200,
        display_in_table=True,
        display_in_form=True
    ),
    dict(
        caption="Ghi chú",
        name="Description",
        display_index=300,
        display_in_table=True,
        display_in_form=True
    )
]
layout=layout_view.create("hrm","category")
layout.create(dict(
    collection="list.provinces",
    columns=layout_view.extend_columns(
        basic_columns,
        [dict(
            caption="Postal Code",
            name="PostalCode"
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