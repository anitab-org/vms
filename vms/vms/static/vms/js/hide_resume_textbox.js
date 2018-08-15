function hide_resume_textbox() {
var fileLength = $("#id_vol-resume_file")[0].files.length;
if (fileLength!==0){
$("#div_id_resume").hide();}
else
{$("div_id_resume").show();}
}
