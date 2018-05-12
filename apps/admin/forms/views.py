import quicky
from quicky import layout_view
app=quicky.applications.get_app_by_file(__file__)
layout=layout_view.create(app.name,"views")
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