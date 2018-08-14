There are a few tests which have been commented out currently to avoid Travis CI build failure:

| File                         | App/Model         | Test name                                                           | Reason/Related issue                              |
|:----------------------------:|:-----------------:|:-------------------------------------------------------------------:|:-------------------------------------------------:|
| test_settings.py             | Administrator     | test_duplicate_event                                                | Logic not yet implemented                         |
| test_settings.py             | Administrator     | test_duplicate_job                                                  | Logic not yet implemented                         |
| test_formFields.py           | Administrator     | test_field_value_retention_for_event                                | [#742](https://github.com/systers/vms/issues/742) |
| test_formFields.py           | Administrator     | test_field_value_retention_for_job                                  | [#742](https://github.com/systers/vms/issues/742) |
| test_formFields.py           | Administrator     | test_field_value_retention_for_shift                                | [#742](https://github.com/systers/vms/issues/742) |
| test_report.py               | Administrator     | test_check_intersection_of_fields                                   | Test is giving inconsistent results, probably issue in logic|
| test_volunteerProfile.py     | Volunteer         | test_valid_upload_resume                                            | [#776](https://github.com/systers/vms/issues/776)|
| test_volunteerProfile.py     | Volunteer         | test_corrupt_resume_uploaded                                        | [#776](https://github.com/systers/vms/issues/776)|
| test_functional_admin.py     | Registration      | test_field_value_retention_in_first_name_state_phone_organization   | [#763](https://github.com/systers/vms/issues/763)|
| test_functional_admin.py     | Registration      | test_field_value_retention_in_last_name_address_city_country        | [#763](https://github.com/systers/vms/issues/763)|
| test_functional_volunteer.py | Registration      | test_field_value_retention_in_first_name_state_phone_organization   | [#763](https://github.com/systers/vms/issues/763)|
| test_functional_volunteer.py | Registration      | test_field_value_retention_in_last_name_address_city_country        | [#763](https://github.com/systers/vms/issues/763)|
| test_unit.py                 | Shift             | test_invalid_model_create                                           | [#743](https://github.com/systers/vms/issues/743)|
| test_unit.py                 | VolunteerShift    | test_invalid_model_create                                           | [#743](https://github.com/systers/vms/issues/743)|
