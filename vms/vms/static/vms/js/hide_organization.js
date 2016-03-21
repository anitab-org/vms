function hide_organization(){
    var value= $('#select').val();
    if(value != '0'){
      $("#div_id_unlisted_organization").hide();}
      else
      {$("#div_id_unlisted_organization").show();}
}
hide_organization();
