from .. import models

def get_job_working_group():
    ret=models.HCSLS_JobWorkingGroup().aggregate()
    ret.sort(dict(
        ordinal = 1
    ))
    return ret

