# -*- coding: utf-8 -*-
from quicky import layout_view

import quicky
import models.hrm.categories
import category
app=quicky.applications.get_app_by_file(__file__)

layout=layout_view.create(app.name,"provinces")
layout.create(dict(
    collection=models.hrm.categories.provinces().get_name(),
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
                col_md=[4,8],
                col_sm=[4,8],
                col_xs=[4,8],
                fields=[
                    dict(name="Code")
                ]
            ),
            dict(
                col_md=[4,8],
                col_sm=[4,8],
                col_xs=[4,8],
                fields=[
                    dict(name="Name")
                ]
            ),
            dict(
                col_md=[4,8],
                col_sm=[4,8],
                col_xs=[4,8],
                fields=[
                    dict(name="ForeignName")
                ]
            ),
            dict(
                col_md=[4,8],
                col_sm=[4, 8],
                col_xs=[4, 8],
                fields=[
                    dict(name="PostalCode")

                ]
            ),
            dict(
                col_md=[4,8],
                col_sm=[4, 8],
                col_xs=[4, 8],
                fields=[
                    dict(name="Description",
                         type="text-area")
                ]
            ),
            dict(
                col_md=[2,10],
                col_sm=[4, 8],
                col_xs=[4, 8],
                fields=[
                    dict(name="CreatedOn",
                         type="date-picker")
                ]
            )
        ]
    )
))