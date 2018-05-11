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
                col_md=[2,4],
                col_sm=[4,8],
                col_xs=[4,8],
                fields=[
                    dict(name="username")
                ]
            ),
            dict(
                col_md=[2, 4,2,4],
                col_sm=[4, 8],
                col_xs=[4, 8],
                fields=[
                    dict(name="first_name"),
                    dict(name="last_name")
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
    ),
    action_list="admin.api.users/get_list",
    action_item="admin.api.users/get_item",
    keys=["username"]

))