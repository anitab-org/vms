/** Hides textbox for unlisted organization if a listed organization is selected */
function hideOrganization(){
  var value = $('#select').val();
  if (value !== '0') {
    $("#div_id_unlisted_organization").hide();
  } else {
    $("#div_id_unlisted_organization").show();
  }
}
hideOrganization();
