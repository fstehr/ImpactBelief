// ELECTRICITY FIELD FUNCTIONS
function show_hide_elec(x) {
    if (x == 5)
        document.getElementById("elec").style.display = "block";
    else
        document.getElementById("elec").style.display = "none";
}

function calculate_elec(){
    if(document.getElementById("electricity_kwh_5").checked){
        let x = (document.getElementById("kWh_field").value);
        document.getElementById("electricity_kwh_5").value = x;
    }
    else // "Deletes" value in open field, when another radio button is clicked.
        document.getElementById("kWh_field").value = null;



}


// GAS FIELD FUNCTIONS
function show_hide_gas(x) {
    if (x == 5)
        document.getElementById("gas").style.display = "block";
    else
        document.getElementById("gas").style.display = "none";
}

function calculate_gas(){
    if (document.getElementById("id_gas_kwh_5").checked){
        let x = (document.getElementById("gas_kWh_field").value);
        document.getElementById("id_gas_kwh_5").value = x;
    }
    else // "Deletes" value in open field, when another radio button is clicked.
        document.getElementById("gas_kWh_field").value = null;

}


// FOSSIL FUEL FUNCTIONS
function show_hide_oil(x) {
    if (x == 1) {
        document.getElementById("fossilfuel").style.display = "none";
        document.getElementById("fossil_fuels_oil").value = null;
        document.getElementById("fossil_fuels_coal").value = null;
        document.getElementById("fossil_fuels_wood").value = null;
        document.getElementById("fossil_fuels_gas").value = null;
    }
    if (x == 2)
        document.getElementById("fossilfuel").style.display = "block";
}

function calculate_fossilfuels() {
    if (document.getElementById("id_fossil_fuels_1").checked){
            let x = (document.getElementById("gas_kWh_field").value);
            document.getElementById("id_gas_kwh_5").value = x;
        }
        else // "Deletes" value in open field, when another radio button is clicked.
            document.getElementById("gas_kWh_field").value = null;



}

// CAR FIELD FUNCTIONS
function show_hide_car(x){
    switch(x) {
        case 1:
            document.getElementById("car").style.display = "none";
            document.getElementById("miles").style.display = "none";
            break;
        case 5:
            document.getElementById("car").style.display = "block";
            document.getElementById("miles").style.display = "block";
            break;
        default:
            document.getElementById("car").style.display = "block";
            document.getElementById("miles").style.display = "none";
    }
}

function calculate_car_miles(){
    if (document.getElementById("id_car_miles_5").checked){
        let x = (document.getElementById("miles_field").value);
        document.getElementById("id_car_miles_5").value = x;
        }
    else // "Deletes" value in open field, when another radio button is clicked.
        document.getElementById("miles_field").value = null;

    // if "I never travel by car is clicked, the mpg fields are reset
    if (document.getElementById("id_car_miles_1").checked){
        document.getElementById("id_car_mpg_1").checked = false;
        document.getElementById("id_car_mpg_2").checked = false;
        document.getElementById("id_car_mpg_3").checked = false;
    }

}


function validate_energy(){
    // Electricity box check
    if(document.getElementById("electricity_kwh_5").checked){
        document.getElementById("kWh_field").required = true;
    }
    else{
        document.getElementById("kWh_field").required = false;
    }

    // Gas box check
    if (document.getElementById("id_gas_kwh_5").checked){
        document.getElementById("gas_kWh_field").required = true;
    }
    else{
        document.getElementById("gas_kWh_field").required = false;
    }

    // Fossil fuels check
    if (document.getElementById("id_fossil_fuels_1").checked){
        document.getElementById("fossil_fuels_oil").required = true;
        document.getElementById("fossil_fuels_coal").required = true;
        document.getElementById("fossil_fuels_wood").required = true;
        document.getElementById("fossil_fuels_gas").required = true;
    }
    else{
        document.getElementById("fossil_fuels_oil").required = false;
        document.getElementById("fossil_fuels_coal").required = false;
        document.getElementById("fossil_fuels_wood").required = false;
        document.getElementById("fossil_fuels_gas").required = false;
    }


}


function validate_mobility(){
    // Car mile value check
    if(document.getElementById("id_car_miles_5").checked){
        document.getElementById("miles_field").required = true;
    }
    else {
        document.getElementById("miles_field").required = false;
    }

    // MPG check
    if(document.getElementById("id_car_miles_1").checked == false){
        document.getElementById("id_car_mpg_1").required = true;
        document.getElementById("id_car_mpg_2").required = true;
        document.getElementById("id_car_mpg_3").required = true;
    }
    else{
        document.getElementById("id_car_mpg_1").required = false;
        document.getElementById("id_car_mpg_2").required = false;
        document.getElementById("id_car_mpg_3").required = false;
    }
}