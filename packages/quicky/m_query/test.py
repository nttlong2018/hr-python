import expr
x=expr.get_tree("(employee_code=={0} and "
                "employee_name=={2} and "
                "department=='001') or "
                "contains(name,{2})",
                    "test cai coi","a","b")
y=expr.get_expr(x,"a","b","c")
print(y)