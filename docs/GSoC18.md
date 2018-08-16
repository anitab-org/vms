# GSoC18 Features Implementation
## Migration to Python 3.6 and Django 1.11
VMS is migrated from Python 3.6 and Django 1.11 from Django 1.8 and Python 2.7.

## Portal API Communication
The meetup data is fetched from the Portal API, and the administrators can create events in VMS from the same, which will be occuring in future.

## Reporting Functionality
The volunteers can generate reports of logged shifts based on event, job, start date and end date.
Once a report is generated for a shift, another can't be generated unless the admin rejects the report. If the admins approve the report, the volunteer gets an email notifyting him/her the same along with the PDF of the report.

## Vola API
The event information can be provided to [Vola](https://github.com/systers/volunteers-android) which can be used by volunteers.
Users can send in a GET or a POST request to https://localhost/event/api/v1/request_event_data/ to access the event data.
In case of a GET request, a list containing the details of all events in the ascending order of their start dates will be returned.
In case of a POST request,a list containing the details of all events starting after the date value sent in the request object will be returned.

## Validation of Organization
If a volunteer signs up with an unlisted organisation then the admins would be notified about it and they can either approve/reject/edit this org and thereafter the volunteer would be notified about this.

## Edit Request Manager for Logged shifts
The volunteers can log hours only once for a shift, and that too after it has started. Once logged, they can request for editing the hours to the admin that too within one week's time. They need to fill up a form with new start time and new end time. The admins get an email providing the link to the same form in which the volunteer has filled the timings to edit. The admins can save the hours upon editing in case, he/she feels the need to do so or reject the request and the volunteer also gets notified about the same.

## Shift Filters and the Functionalities Proivided
**1. Upcoming shifts**<br>
Shift can be cancelled<br>
**2. Unlogged shifts**<br>
The shift hours can be logged<br>
**3. Logged shifts**<br>
Volunteers can make an Edit Request within one week.<br>
Admins can clear as well as edit the hours of the logged shifts<br>
**4. Reported Shifts**<br>
No functionality provided to volunteers

## Volunteer Search Implementation for administrators on the basis of event and job
The volunteers related to that event or job gets filtered.

## Search Filters for events and jobs for admins and volunteers
The jobs/events can be searched on the basis of name, start date, end date, location.

## UI upgradation
The UI of VMS is upgraded following Anita Borg Guidelines.

## Location validation
Dependent dropdown list of states, city and country is shown in event, sign up forms etc.

## Other Enhancements
1. Password Reset
2. Password change Functionality
3. Email Authentication
4. Password Regex Checks in sign up
5. Added description field for events
6. Event Detail View
7. Password Authentication while sign-up
8. Notification for volunteers
9. Past events set to non editable
10. Hide textbox for resume link when file is uploaded

## Coding Standards
1. Update JavaScript according to standards
2. Improvement in CSS coding standards by replacing nbsp with padding

## Bug Fixes
Volunteer/Administrator registration allowed with empty organization database.

## Documentation
1. Wiki SideBar update
2. Home Page updation with removal of broken links
3. Database models doc updation

