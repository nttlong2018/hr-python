import qmongo_static
qmongo_static.set_config(
    host="localhost",
    port=27017,
    user="root",
    password="123456",
    name="hrm",
    collection="sys_settings"
)
qmongo_static.set_data(
    global_config=dict(
        short_date_format="dd/MM/yyyy"
    )
)
fx=qmongo_static.get_data()
print(fx)