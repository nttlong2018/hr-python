# -*- coding: utf-8 -*-
from quicky import layout_view
from . import category
import quicky
import models.hrm.categories
app=quicky.applications.get_app_by_file(__file__)
layout=layout_view.create(app.name,"districts")
layout.create(dict(
    collection=models.hrm.categories.districts().name,
    lookups=[
        dict(
            source=models.hrm.categories.provinces().name,
            local_field="ProvinceCode",
            foreign_field="Code",
            alias="Province"
        )
    ],
    columns=layout_view.extend_columns(
        category.basic_columns,
        [dict(
            caption="Province Code",
            name="Province.Code",
        ),
        dict(
            caption="Province Name",
            name="Province.Name"

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
                    dict(name="ProvinceCode",
                         type="select",
                         source=models.hrm.categories.provinces().name,
                         lookup_field="Code",
                         display_field="Name")

                ]
            ),
            dict(
                col_md=[2,10],
                col_sm=[4, 8],
                col_xs=[4, 8],
                fields=[
                    dict(name="Description",
                         type="html-editor")
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