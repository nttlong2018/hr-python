import quicky
from quicky import layout_view
layout=layout_view.create("hrm","views")
# "_id": ObjectId("5ad4250d927e004ab36cc2bc"),
# "Name": "index",
# "Create": false,
# "Delete": false,
# "Description": "",
# "Extend": {
#
#           },
# "Read": false,
# "App": "admin",
# "Update": false,
# "Path": "index",
# "IsPulic": false
layout.create(dict(
    collection="sys_views",
    columns=[
        dict(
            caption="Application",
            name="App",
            display_index=50

        ),
        dict(
            caption="ID",
            name="Path",
            display_index=100
        ),
        dict(
            caption="Name",
            name="Name",
            display_index=200
        ),
        dict(
            caption="Is Pulic",
            name="IsPulic",
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
                    dict(name="App"),
                    dict(name="Path")
                ]
            ),
            dict(
                col_md=[2, 10],
                col_sm=[4, 8],
                col_xs=[4, 8],
                fields=[
                    dict(name="Name"),
                    dict(name="Name")
                ]
            ),
            dict(
                col_md=[2, 10],
                col_sm=[4, 8],
                col_xs=[4, 8],
                fields=[
                    dict(name="Description",
                         type="text-area")
                ]
            )
        ]
    ),
    keys=["App","Path"]


))