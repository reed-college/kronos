// Copied almost entirely from http://stackoverflow.com/a/11833377/6118574

function checkfile(sender) {
    var validExts = new Array(".xlsx", ".xls", ".csv", ".ics");
    var fileExt = sender.value;
    fileExt = fileExt.substring(fileExt.lastIndexOf('.'));
    if (validExts.indexOf(fileExt) < 0) {
      alert("Invalid file selected, valid files are of " +
               validExts.toString() + " types.");
      return false;
    }
    else return true;
  }

$(document).ready(function(){
});
