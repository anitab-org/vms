/** Shows start and end dates of selected event while creating/editing jobs */
function updateEventDates() {
  var eventList = document.getElementById("events");
  var selectedEvent = eventList.options[eventList.selectedIndex];
  var startDate = selectedEvent.getAttribute("start_date");
  var endDate = selectedEvent.getAttribute("end_date");
  document.getElementById("start_date_here").innerHTML = startDate;
  document.getElementById("end_date_here").innerHTML = endDate;
}
updateEventDates();
