/** Fetches cities belonging to selected state and country */
$(document).ready(function() {
    $("#select_state").change(function() {
        var countryId = $("#select_country").val();
        var stateId = $(this).val();
        $.ajax({
            url: CityUrl,
            data: {
                "country": countryId,
                "state": stateId
            },
            success: function(cities) {
                $("#select_city").html(cities);
            }
        });
    });
});
