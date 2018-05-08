from helpers import filter

fx=filter("a==@test",test='12')
fx.And("c>@test",test=12).Or("c==11")

print fx.get_json()

