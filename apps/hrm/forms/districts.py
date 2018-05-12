# -*- coding: utf-8 -*-
from quicky import layout_view
from . import category
import quicky
app=quicky.applications.get_app_by_file(__file__)
layout=layout_view.create(app.name,"districts")
layout.create(dict(
    collection="list.districts",
    columns=layout_view.extend_columns(
        category.basic_columns,
        [dict(
            caption="Province",
            name="ProvinceCode",
            display_index=2010,
            lookup=dict(
                source="list.provinces",
                field="Code",
                alias="Province"
            )
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
                    dict(name="ProvinceId",
                         type="select",
                         source="list.provinces",
                         lookup_field="_id",
                         display_field="Name")

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