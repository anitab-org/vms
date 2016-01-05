function update_event_dates(){
	var event_list = document.getElementById("events");
	var selected_event = event_list.options[event_list.selectedIndex];
	var start_date = selected_event.getAttribute("start_date");
	var end_date = selected_event.getAttribute("end_date");
	document.getElementById("start_date_here").innerHTML = start_date;
	document.getElementById("end_date_here").innerHTML = end_date;
}
update_event_dates();
