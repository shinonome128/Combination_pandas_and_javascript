function buttonClick(){
  var str= '';
  for (var i = 0, rowlen = $("table tbody  tr").length; i < rowlen; i++) {
      str += $("table tbody tr")[i].cells[1].innerHTML
      str += "\t"
      var select = $("table tbody tr")[i].cells[4].children[0];
      str += $(select).val();
      str += "\n"
  }
 $("textarea").val(str)
}
$(function(){
  for (var i = 0, rowlen = $("table tbody  tr").length; i < rowlen; i++) {
    var select = $("table tbody tr")[i].cells[4].children[0];
    var init = $("table tbody tr")[i].cells[2].innerHTML
    if(getFileName() == "OTHER.html"){
      init = "OTHER"
    }
    $(select).val(init);
  }
})

function getFileName() {
  return window.location.href.split('/').pop();
}
