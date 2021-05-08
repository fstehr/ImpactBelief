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
}

function validate_energy(){
    if(document.getElementById("electricity_kwh_5").checked){
        let x = document.getElementById("electricity_kwh_5").value;
        if (x < 1){
            alert("Please enter a valid electricity kWh value");
            event.preventDefault();
            }
        }

    if (document.getElementById("id_gas_kwh_5").checked){
        let x = document.getElementById("id_gas_kwh_5").value;
        if (x < 1){
            alert("Please enter a valid gas kWh value");
            event.preventDefault()
            }
        }

}


function validate_mobility(){

    // Car mile value check
    if(document.getElementById("id_car_miles_5").checked){
        let x = document.getElementById("id_car_miles_5").value;
        if (x < 1){
            alert("Please enter a valid car mile distance");
            event.preventDefault();
            }
        }

    // MPG check

    if(document.getElementById("id_car_miles_1").checked == false){
        let mpg = document.getElementsByName("car_size_mpg");
        var counter = 0;

        for (i = 0; i < mpg.length; i++){
            if (mpg[i].checked == false)
                counter += 1;
        }

        if (counter == mpg.length) {
            alert("Please check one of the mpg boxes");
            event.preventDefault();

        }

    }
}