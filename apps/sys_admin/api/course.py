import lms
def get_list(params):
    return lms.courseware.get_list()
def delete_item(args):
    print(args)
    return lms.courseware.delete_by_id(args["id"])