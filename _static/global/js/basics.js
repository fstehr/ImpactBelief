console.log("basics ready!")

let timeout  = js_vars.timeout || 999999999999;

// tooltip
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

// popover
$(function () {
  $('[data-toggle="popover"]').popover()
})

// submit in case you don't use buttons
function submitPage() {
    document.forms[0].submit()
}

