import quicky
from quicky import layout_view
layout=layout_view.create("hrm","users")
layout.create(dict(
    collection="auth_user",
    columns=[
        dict(
            caption="Username",
            name="username",
            display_index=100
        ),
        dict(
            caption="Firstname",
            name="first_name",
            display_index=200
        ),
        dict(
            caption="Lastname",
            name="last_name",
            display_index=300
        )
    ],
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