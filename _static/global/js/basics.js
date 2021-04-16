console.log("basics ready!")

// variables from python
let template = js_vars.template || 0;
let endowments = js_vars.endowments || 0;
let current_round  = js_vars.current_round || 0;
let timeout  = js_vars.timeout || 999999999999;

// tooltip
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

// popover
$(function () {
  $('[data-toggle="popover"]').popover()
})

// reverse the table's order
$(function(){
if (template == "results" || template == "final"){
    $("tbody").each(function(elem,index){
      var arr = $.makeArray($("tr",this).detach());
      arr.reverse();
        $(this).append(arr);
    });
}
});

// submit in case you don't use buttons
function submitPage() {
    document.forms[0].submit()
}

// timer & alert
setTimeout(
    function () {
        if (template == "decision"){
            document.getElementById("timeoutModal").classList.add("show")
        }
    },
    (timeout - 0.5) * 60 * 1000
);