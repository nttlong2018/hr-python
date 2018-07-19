import django
import quicky
import authorization
import qmongo
from qmongo import database, helpers
app=quicky.applications.get_app_by_file(__file__)
db_context=database.connect(app.settings.Database)
from SYS_FunctionList import SYS_FunctionList
from HCSSYS_DataDomain import HCSSYS_DataDomain
from HCSSYS_Departments import HCSSYS_Departments
from SYS_ValueList import SYS_ValueList
from HCSSYS_SystemConfig import HCSSYS_SystemConfig
from auth_user import auth_user
from auth_user_info import auth_user_info
from AD_Roles import AD_Roles
from HCSSYS_ComboboxList import HCSSYS_ComboboxList
from HCSLANG_CollectionInfo import HCSLANG_CollectionInfo
from HCSSYS_CollectionInfo import HCSSYS_CollectionInfo
from HCSSYS_ExcelTemplate import HCSSYS_ExcelTemplate
from HCSLS_EmployeeType import HCSLS_EmployeeType
from HCSLS_Nation import HCSLS_Nation
from HCSLS_Region import HCSLS_Region
from HCSLS_Ethnic import HCSLS_Ethnic
from HCSLS_Marital import HCSLS_Marital
from HCSLS_Religion import HCSLS_Religion
from HCSLS_QuitJob import HCSLS_QuitJob
from HCSLS_Certificate import HCSLS_Certificate
from HCSLS_GroupCertificate import HCSLS_GroupCertificate
from HCSLS_TrainTypeDetail import HCSLS_TrainTypeDetail
from HCSLS_TrainSupplier import HCSLS_TrainSupplier
from HCSLS_TrainCVRG import HCSLS_TrainCVRG
from HCSLS_TrainDomain import HCSLS_TrainDomain
from HCSLS_TrainType import HCSLS_TrainType
from HCSLS_Profession import HCSLS_Profession
from HCSLS_Acadame import HCSLS_Acadame
from HCSLS_Position import HCSLS_Position
from HCSLS_Award import HCSLS_Award
from HCSLS_AwardLevel import HCSLS_AwardLevel
from HCSLS_AwardPlace import HCSLS_AwardPlace
from HCSLS_Province import HCSLS_Province
from HCSLS_District import HCSLS_District
from HCSLS_Ward import HCSLS_Ward
from HCSLS_Hamlet import HCSLS_Hamlet
from HCSLS_Discipline import HCSLS_Discipline
from HCSEM_Employees import HCSEM_Employees
from HCSLS_JobWorkingGroup import HCSLS_JobWorkingGroup
from TMLS_Rank import TMLS_Rank
from tmp_transactions import tmp_transactions