There are several tests/parts of tests which have been commented out currently to avoid travis build failure:

|File               |Tests            |Reason/Related issue           |
|------------------------------|:------------------:|:------------------------: |
| test_formFields.py |  test_null_values_in_edit_event| [345](https://github.com/systers/vms/issues/345)|
| test_formFields.py |  test_field_value_retention_for_event, test_field_value_retention_for_job, test_field_value_retention_for_shift| [#350](https://github.com/systers/vms/issues/350)|
| test_formFields.py |  test_simplify_job|Cause of failure is still unclear|
| test_report.py | test_null_values_with_dataset, test_check_intersection_of_fields| [#327](https://github.com/systers/vms/issues/327)|
| test_settings.py |  test_duplicate_event, test_duplicate_job|[#329](https://github.com/systers/vms/issues/329), [#330](https://github.com/systers/vms/issues/330)|
| test_shiftSignUp.py | test_search_event| [#337](https://github.com/systers/vms/issues/337)|
| test_functional.py | test_admin_cannot_access_volunteer_urls, test_volunteer_cannot_access_admin_urls| [#325](https://github.com/systers/vms/issues/325)|
| test_functional_volunteer.py | test_location_fields|[#336](https://github.com/systers/vms/issues/336)|
| test_viewVolunteerShift.py | test_access_another_existing_volunteer_view| [#326](https://github.com/systers/vms/issues/326)|
| test_volunteerProfile.py |test_upload_resume, test_invalid_resume_format| [#305](https://github.com/systers/vms/issues/305) |
| test_volunteerReport.py |test_report_with_empty_fields, test_date_field, test_event_field, test_job_field, test_intersection_of_fields| [#327](https://github.com/systers/vms/issues/327) |
