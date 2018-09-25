The tests which are needed by POM app have already been tested thus following _DRY_ approach, the tests which are needed by POM app have been documented below. 

#### Administrator Report Page

| App                | File name         | Test name                            |
|:------------------:|:-----------------:|:------------------------------------:|
| Administrator      | test_report.py    | test_null_values_with_dataset        |
| Administrator      | test_report.py    | test_null_values_with_empty_dataset  |

#### Administrator Registration Page

| App                | File name                  | Test name                                                         |
|:------------------:|:--------------------------:|:-----------------------------------------------------------------:|
| Registration       | test_functional_admin.py   | test_null_values                                                  |
| Registration       | test_functional_admin.py   | test_field_value_retention_in_first_name_state_phone_organization |
| Registration       | test_functional_admin.py   | test_user_registration_with_same_username                         |
| Registration       | test_functional_admin.py   | test_numeric_characters_in_first_and_last_name                    |
| Registration       | test_functional_admin.py   | test_special_characters_in_location                               |
| Registration       | test_functional_admin.py   | test_email_field                                                  |
| Registration       | test_functional_admin.py   | test_phone_in_different_country                                   |
| Registration       | test_functional_admin.py   | test_organization_with_invalid_characters                         |

#### Authentication Page

| App                | File name         | Test name                            |
|:------------------:|:-----------------:|:------------------------------------:|
| Authentication     | test_login.py     | test_correct_admin_credentials       |
| Authentication     | test_login.py     | test_incorrect_admin_credentials     |

#### Completed Shifts Page

| App                | File name              | Test name                             |
|:------------------:|:----------------------:|:-------------------------------------:|
| Shift              | test_shiftHours.py     | test_end_hours_less_than_start_hours  |
| Shift              | test_shiftHours.py     | test_view_with_unlogged_shift         |
| Shift              | test_shiftHours.py     | test_view_with_logged_shift           |
| Shift              | test_shiftHours.py     | test_cancel_hours                     |

#### Event Sign Up Page

| App                | File name              | Test name                                  |
|:------------------:|:----------------------:|:------------------------------------------:|
| Event              | test_shiftSignUp.py    | test_search_event_both_date_present        |
| Event              | test_shiftSignUp.py    | test_signup_shifts_with_registered_shifts  |
| Event              | test_shiftSignUp.py    | test_signup_for_same_shift_again           |
| Event              | test_shiftSignUp.py    | test_shift_sign_up_with_outdated_shifts    |

#### Events Page

| App                | File name            | Test name                                    |
|:------------------:|:--------------------:|:--------------------------------------------:|
| Administrator      | test_formFields.py   | test_null_values_in_create_job               |
| Administrator      | test_formFields.py   | test_null_values_in_create_event             |
| Administrator      | test_formFields.py   | test_null_values_in_create_shift             |
| Organization       | test_organization.py | test_create_valid_organization               |
| Administrator      | test_formFields.py   | test_null_values_in_edit_event               |
| Administrator      | test_formFields.py   | test_null_values_in_edit_job                 |
| Administrator      | test_formFields.py   | test_null_values_in_edit_shift               |
| Organization       | test_organization.py | test_edit_organization_with_invalid_value    |
| Organization       | test_organization.py | delete_organization_from_list                |
| Administrator      | test_formFields.py   | test_field_value_retention_for_event         |
| Administrator      | test_formFields.py   | test_field_value_retention_for_job           |
| Administrator      | test_formFields.py   | test_field_value_retention_for_shift         |
| Administrator      | test_formFields.py   | test_max_volunteer_field                     |
| Administrator      | test_formFields.py   | test_simplify_shift                          |
| Administrator      | test_formFields.py   | test_simplify_job                            |

#### Job Details Page

| App               | File name             | Test name                    |
|:-----------------:|:---------------------:|:----------------------------:|
| Job               | test_jobDetails.py    | test_invalid_job_edit        |
| Job               | test_jobDetails.py    | test_valid_job_edit          |
| Job               | test_jobDetails.py    | test_job_delete              |
| Job               | test_jobDetails.py    | test_job_details_view        |

#### Manage Shift Page

| App               | File name                      | Test name                                     |
|:-----------------:|:------------------------------:|:---------------------------------------------:|
| Shift             | test_manageVolunteerShift.py   | test_table_layout                             |
| Shift             | test_manageVolunteerShift.py   | test_landing_page_with_registered_volunteers  |
| Shift             | test_manageVolunteerShift.py   | test_cancel_assigned_shift                 |

#### Shift Details Page

| App               | File name                | Test name                                   |
|:-----------------:|:------------------------:|:-------------------------------------------:|
| Shift             | test_shiftDetails.py     | test_view_with_unregistered_volunteers      |
| Shift             | test_shiftDetails.py     | test_view_with_logged_hours                 |
| Shift             | test_shiftDetails.py     | test_view_with_only_registered_volunteers   |


#### Upcoming Shifts Page

| App               | File name                    | Test name                                                              |
|:-----------------:|:----------------------------:|:----------------------------------------------------------------------:|
| Shift             | test_viewVolunteerShift.py   | test_access_another_existing_volunteer_view                            |
| Shift             | test_viewVolunteerShift.py   | test_log_hours_and_logged_shift_does_not_appear_in_upcoming_shifts     |
| Shift             | test_viewVolunteerShift.py   | test_view_with_assigned_and_unlogged_shift                             |
| Shift             | test_viewVolunteerShift.py   | test_cancel_shift_registration                                         |

#### Volunteer Profile Page

| App               | File name                  | Test name                      |
|:-----------------:|:--------------------------:|:------------------------------:|
| Volunteer         | test_volunteerProfile.py   | test_edit_profile              |
| Volunteer         | test_volunteerProfile.py   | test_invalid_resume_format     |
| Volunteer         | test_volunteerProfile.py   | test_valid_upload_resume       |

#### Volunteer Registration Page

| App               | File name                     | Test name                                                         |
|:-----------------:|:-----------------------------:|:-----------------------------------------------------------------:|
| Registration      | test_functional_volunteer.py  | test_field_value_retention_in_first_name_state_phone_organization |
| Registration      | test_functional_volunteer.py  | test_null_values                                                  |
| Registration      | test_functional_volunteer.py  | test_user_registration_with_same_username                         |
| Registration      | test_functional_volunteer.py  | test_numeric_characters_in_first_and_last_name                    |
| Registration      | test_functional_volunteer.py  | test_special_characters_in_location                               |
| Registration      | test_functional_volunteer.py  | test_email_field                                                  |
| Registration      | test_functional_volunteer.py  | test_phone_in_different_country                                   |
| Registration      | test_functional_volunteer.py  | test_organization_with_invalid_characters                         |

#### Volunteer Report Page

| App               | File name                | Test name                       |
|:-----------------:|:------------------------:|:-------------------------------:|
| Volunteer         | test_volunteerReport.py  | test_event_field                |
| Volunteer         | test_volunteerReport.py  | test_intersection_of_fields     |
| Volunteer         | test_volunteerReport.py  | test_report_with_empty_fields   |


#### Volunteer Search Page

| App               | File name                | Test name                                 |
|:-----------------:|:------------------------:|:-----------------------------------------:|
| Volunteer         | test_searchVolunteer.py  | test_volunteer_first_name_field           |
| Volunteer         | test_searchVolunteer.py  | test_volunteer_last_name_field            |
| Volunteer         | test_searchVolunteer.py  | test_volunteer_city_field                 |
| Volunteer         | test_searchVolunteer.py  | test_volunteer_state_field                |
| Volunteer         | test_searchVolunteer.py  | test_volunteer_country_field              |
| Volunteer         | test_searchVolunteer.py  | test_volunteer_valid_organization_field   |
