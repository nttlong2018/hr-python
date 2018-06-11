from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
def HCSSYS_SystemConfig():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSSYS_SystemConfig",
            "base",
            [],
            is_has_number=helpers.create_field("bool"),
            num_of_number=helpers.create_field("numeric"),
            is_has_upper_char=helpers.create_field("bool"),
            num_of_upper=helpers.create_field("numeric"),
            is_has_lower_char=helpers.create_field("bool"),
            num_of_lower=helpers.create_field("numeric"),
            is_has_symbols=helpers.create_field("bool"),
            num_of_symbol=helpers.create_field("numeric"),

            is_ad_aut=helpers.create_field("bool"),
            session_timeOut=helpers.create_field("numeric"),
            time_out_expand=helpers.create_field("numeric"),
            minimum_age=helpers.create_field("numeric"),
            password_expiration=helpers.create_field("numeric"),
            will_expire=helpers.create_field("bool"),
            change_after=helpers.create_field("numeric"),
            apply_minimum_age=helpers.create_field("bool"),

            apply_history=helpers.create_field("bool"),
            history=helpers.create_field("numeric"),
            apply_minLength=helpers.create_field("bool"),
            min_len=helpers.create_field("numeric"),
            apply_maxLength=helpers.create_field("bool"),
            max_len=helpers.create_field("numeric"),
            lock_on_failed=helpers.create_field("bool"),
            threshold_to_lock=helpers.create_field("numeric"),
            time_lock=helpers.create_field("numeric"),

            alert_before=helpers.create_field("numeric"),
            is_first_change=helpers.create_field("bool"),
            not_user_in_password=helpers.create_field("bool"),
            date_format=helpers.create_field("text"),
            dec_place_separator=helpers.create_field("text"),
            dec_place_currency=helpers.create_field("numeric"),
            default_language=helpers.create_field("text")
        )

        _hasCreated=True
    ret = db_context.collection("HCSSYS_SystemConfig")

    return ret