from .. models import sys_customers
from .. import query
def get_list(args):
    params=dict(
        page_size=0,
        page_index=50,
        search_text="",
        sort=dict(
            code=1
        )
    )
    params.update(args.get("data",{}))
    qr= query.qr_customers()
    qr.sort(params["sort"])
    ret=qr.get_page(params["page_size"],params["page_index"])
    return ret

