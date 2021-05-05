// ELECTRICITY FIELD FUNCTIONS
function show_hide_elec(x) {
    if (x == 5)
        document.getElementById("elec").style.display = "block";
    else
        document.getElementById("elec").style.display = "none";
}

function calculate_elec(){
    let x = (document.getElementById("kWh_field").value);
    document.getElementById("electricity_kwh_5").value = x;
}


// GAS FIELD FUNCTIONS
function show_hide_gas(x) {
    if (x == 5)
        document.getElementById("gas").style.display = "block";
    else
        document.getElementById("gas").style.display = "none";
}

function calculate_gas(){
    let x = (document.getElementById("gas_kWh_field").value);
    document.getElementById("id_gas_kwh_5").value = x;
}


// FOSSIL FUEL FUNCTIONS
function show_hide_oil(x) {
    if (x == 1)
        document.getElementById("fossilfuel").style.display = "none";
    if (x == 2)
        document.getElementById("fossilfuel").style.display = "block";
}


// CAR FIELD FUNCTIONS
function show_hide_car(x){
    switch(x) {
        case 1:
            document.getElementById("car").style.display = "none";
            document.getElementById("miles").style.display = "none";
            document.getElementsByName("car_size_mpg").required = false;
            break;
        case 5:
            document.getElementById("car").style.display = "block";
            document.getElementById("miles").style.display = "block";
            document.getElementsByName("car_size_mpg").required = true;
            break;
        default:
            document.getElementById("car").style.display = "block";
            document.getElementById("miles").style.display = "none";
            document.getElementsByName("car_size_mpg").required = true;
    }
}

function calculate_car_miles(){
    let x = (document.getElementById("miles_field").value);
    document.getElementById("id_car_miles_5").value = x;
}

