from sqlalchemy.types import *
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class course_overviews_courseoverview(Base):
    __tablename__ = 'course_overviews_courseoverview'
    created=Column(DateTime)
    modified=Column(DateTime)
    version=Column(Integer,nullable=False)
    id=Column(String,nullable=False,primary_key=True)
    display_name=Column(String)
    _location=Column(String)
    display_number_with_default=Column(String)
    display_org_with_default=Column(String)
    start=Column(DateTime)
    end=Column(DateTime)
    advertised_start=Column(String)
    course_image_url=Column(String)
    social_sharing_url=Column(String)
    end_of_course_survey_url=Column(String)
    certificates_display_behavior=Column(String)
    certificates_show_before_end=Column(SMALLINT)
    cert_html_view_enabled = Column(SMALLINT)
    has_any_active_web_certificate= Column(SMALLINT)
    cert_name_short= Column(String)
    cert_name_long= Column(String)
    lowest_passing_grade=Column(DECIMAL)
    days_early_for_beta=Column(DECIMAL)
    mobile_available=Column(SMALLINT)
    visible_to_staff_only=Column(SMALLINT)
    _pre_requisite_courses_json=Column(String)
    enrollment_start=Column(DateTime)
    enrollment_end=Column(DateTime)
    enrollment_domain=Column(String)
    invitation_only=Column(BOOLEAN)
    max_student_enrollments_allowed=Column(INT)
    announcement=Column(DateTime)
    catalog_visibility=Column(String)
    course_video_url=Column(String)
    effort=Column(String)
    short_description=Column(String)
    org=Column(String)
    self_paced=Column(BOOLEAN)
    marketing_url=Column(String)
    eligible_for_financial_aid=Column(BOOLEAN)
    language=Column(String)


class course_overviews_courseoverviewtab(Base):
    "`id` INT(11) NOT NULL AUTO_INCREMENT,\
    `tab_id` VARCHAR(50) NOT NULL,\
    `course_overview_id` VARCHAR(255) NOT NULL,\
      `idnew_table` INT NOT NULL,"
    __tablename__ = 'course_overviews_courseoverviewtab'
    id=Column(Integer,primary_key=True)
    tab_id=Column(String)
    course_overview_id=Column(String)


