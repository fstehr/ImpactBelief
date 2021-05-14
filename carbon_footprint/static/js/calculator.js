// taken from https://carbonindependent.org/calculator.js


//for version 4 - started 27.1.19

var ele_kWh = 0
var ele_co2 = 0

var gas_fac = 11.2
var gas_kWh = 0
var gas_co2 = 0

var oil_lit = 0
var oil_co2 = 0

var car01_mil = 0
var car02_mil = 0
var car03_mil = 0
var car04_mil = 0

var car01_co2 = 0
var car02_co2 = 0
var car03_co2 = 0
var car04_co2 = 0

var foo_co2 = 0
var mis_co2 = 0

var foo_org = 0 //organic food
var foo_mea = 0 // meat
var foo_tra = 0.1 //
var foo_pac = 0 // packaged and processed
var foo_com = 0 // proportion composted
var foo_was = 0.25 // food wasted as proportion of eaten

var mis_factor = 1 //misc spending
var com_factor = 0 //composting?
var re1_factor = 0 //recycling 1 ?
var re2_factor = 0

var gov_co2 = 1.1

var bus_mil = 0
var bus_co2 = 0
var tra_mil = 0
var tra_co2 = 0
var fli_hrs = 0
var fli_co2 = 0
//---------------------------------------------------------------------------------------------
function LoadEvents() {

    document.getElementById("eleCalTable").style.display = "none";
    document.getElementById("gasCalTable").style.display = "none";
    document.getElementById("gaskWhTable").style.display = "none";
    document.getElementById("oilCalTable").style.display = "none";

    document.getElementById("carCalTable01").style.display = "none";
    document.getElementById("carCalTable02").style.display = "none";
    document.getElementById("carCalTable03").style.display = "none";
    document.getElementById("carCalTable04").style.display = "none";

    document.form1.mis_co2.value = mis_co2

    document.getElementById("fliCalTableUK").style.display = "none";
    document.getElementById("fliCalTableEur").style.display = "none";
    document.getElementById("fliCalTableAme").style.display = "none";
    document.getElementById("fliCalTableAsi").style.display = "none";

}
//---------------------------------------------------------------------------------------------
function calculate_ele(x) {

    if (x == 3000) {
        ele_kWh = 3000;
        document.getElementById("eleCalTable").style.display = "none";
    }
    if (x == 4800) {
        ele_kWh = 4800;
        document.getElementById("eleCalTable").style.display = "none";
    }
    if (x == 7000) {
        ele_kWh = 7000;
        document.getElementById("eleCalTable").style.display = "none";
    }
    if (x == 2000) {
        ele_kWh = 2000;
        document.getElementById("eleCalTable").style.display = "none";
    }
    if (x == 0) {
        document.getElementById("eleCalTable").style.display = "block";
    } //added 20.7
    if (x == 1) {
        var ele2 = document.form1.ele2.value;
        var ele1 = document.form1.ele1.value;
        ele_kWh = ele2 - ele1;
    }

    document.form1.ele_kWh.value = Math.round(ele_kWh);

    var ele_ren = 1 //proportion of ele renewable
    if (document.form1.ele_ren.checked == true)
        ele_ren = 0.75; //was 0.1

    //ele_co2 = Math.round(ele_kWh * ele_ren * 0.000527 * 100)/100 ; //replaced 28.1.19
    ele_co2 = Math.round(ele_kWh * ele_ren * 0.000309 * 100) / 100; //was 0.000527
    document.form1.ele_co2.value = ele_co2;

    calculate_tot();

}
//---------------------------------------------------------------------------------------------
function calculate_gas(x) {

    var gas_result //final amount in kWh
    if (x == 12000) {
        gas_kWh = 12000; //was 10000
        document.getElementById("gasCalTable").style.display = "none";
        document.getElementById("gaskWhTable").style.display = "none";
    }
    if (x == 18000) {
        gas_kWh = 18000; //was 20000
        document.getElementById("gasCalTable").style.display = "none";
        document.getElementById("gaskWhTable").style.display = "none";
    }
    if (x == 27000) {
        gas_kWh = 27000; //was 28000
        document.getElementById("gasCalTable").style.display = "none";
        document.getElementById("gaskWhTable").style.display = "none";
    }
    if (x == 5000) {
        gas_kWh = 5000;
        document.getElementById("gasCalTable").style.display = "none";
        document.getElementById("gaskWhTable").style.display = "none";
    }
    if (x == 0) {
        document.getElementById("gaskWhTable").style.display = "none";
        document.getElementById("gasCalTable").style.display = "block"; //i.e. show calc. table
    }
    if (x == 1) {
        var gas2 = document.form1.gas2.value;
        var gas1 = document.form1.gas1.value;
        var gas_diff = gas2 - gas1;
        document.form1.gas_diff.value = gas_diff;
        gas_kWh = Math.round(gas_diff * gas_fac); // default gas_fac is defined at the top for metric meters and updated by code in radio buttons
        document.form1.gas_kWh_box.value = gas_kWh
    }
    if (x == 2) {
        document.getElementById("gasCalTable").style.display = "none";
        document.getElementById("gaskWhTable").style.display = "block";
    }
    if (x == 3) {
        var gas3 = document.form1.gas3.value;
        gas_kWh = gas3;
    }

    document.form1.gas_kWh.value = gas_kWh;

    gas_co2 = Math.round(gas_kWh * 0.000203 * 100) / 100; //was 0.00019
    document.form1.gas_co2.value = gas_co2;

    calculate_tot();

}
//---------------------------------------------------------------------------------------------
function show_hide_oil(x) {
    //also calculates coal, wood and bottled gas (from December 2013)

    if (x == 1)
        document.getElementById("oilCalTable").style.display = "none";
    document.form1.oil.value = "";
    document.form1.col.value = "";
    document.form1.woo.value = "";
    document.form1.bot.value = "";
    calculate_oil();
    if (x == 2)
        document.getElementById("oilCalTable").style.display = "block";

    calculate_tot();
}

//---------------------------------------------------------------------------------------------
function calculate_oil() {
    //and coal, wood and bottled gas from Dec 2013, using "oil" to denote the total of these

    oil_lit = document.form1.oil.value;
    col = document.form1.col.value;
    woo = document.form1.woo.value;
    bot = document.form1.bot.value;
    oil_co2 = Math.round(oil_lit * 0.00296 * 100 + col * 0.00326 * 100 + woo * 0.0001 * 100 + bot * 0.00368 * 100) / 100;
    document.form1.oil_co2.value = oil_co2;

    calculate_tot();
}

//---------------------------------------------------------------------------------------------
function display_car_questions(x) {

    if (x > 0)
        document.getElementById("carCalTable01").style.display = "block";
    if (x < 1) {
        document.getElementById("carCalTable01").style.display = "none";
        car01_co2 = 0;
    }
    if (x > 1)
        document.getElementById("carCalTable02").style.display = "block";
    if (x < 2) {
        document.getElementById("carCalTable02").style.display = "none";
        car02_co2 = 0;
    }
    if (x > 2)
        document.getElementById("carCalTable03").style.display = "block";
    if (x < 3) {
        document.getElementById("carCalTable03").style.display = "none";
        car03_co2 = 0;
    }
    if (x > 3)
        document.getElementById("carCalTable04").style.display = "block";
    if (x < 4) {
        document.getElementById("carCalTable04").style.display = "none";
        car04_co2 = 0;
    }

}

//---------------------------------------------------------------------------------------------
function calculate_car01(x) {

    //Updating Jan 2020 with factors from Which? magazine:
    //if (x == 1)  document.form1.mpg01.value = 37 ;
    //if (x == 2)  document.form1.mpg01.value = 33 ;
    //if (x == 3)  document.form1.mpg01.value = 24 ;
    if (x == 1)
        document.form1.mpg01.value = 52;
    if (x == 2)
        document.form1.mpg01.value = 46;
    if (x == 3)
        document.form1.mpg01.value = 35;
    mpg01 = document.form1.mpg01.value

    if (x == 5)
        document.form1.mil01.value = 6000;
    if (x == 6)
        document.form1.mil01.value = 9000;
    if (x == 7)
        document.form1.mil01.value = 12000;
    car01_mil = document.form1.mil01.value

    car01_co2 = Math.round(100 * car01_mil * 0.0143 / mpg01) / 100; //was 0.0105
    if (mpg01 == 0)
        car01_co2 = "";
    document.form1.car01_co2.value = car01_co2;

    calculate_tot();

}
//---------------------------------------------------------------------------------------------
function calculate_car02(x) {

    //Ditto as above, etc
    //if (x == 1)  document.form1.mpg02.value = 37 ;
    //if (x == 2)  document.form1.mpg02.value = 33 ;
    //if (x == 3)  document.form1.mpg02.value = 24 ;
    if (x == 1)
        document.form1.mpg02.value = 52;
    if (x == 2)
        document.form1.mpg02.value = 46;
    if (x == 3)
        document.form1.mpg02.value = 35;
    mpg02 = document.form1.mpg02.value

    if (x == 5)
        document.form1.mil02.value = 6000;
    if (x == 6)
        document.form1.mil02.value = 9000;
    if (x == 7)
        document.form1.mil02.value = 12000;
    car02_mil = document.form1.mil02.value

    car02_co2 = Math.round(100 * car02_mil * 0.0143 / mpg02) / 100;
    if (mpg02 == 0)
        car02_co2 = "";
    document.form1.car02_co2.value = car02_co2;

    calculate_tot();

}
//---------------------------------------------------------------------------------------------
function calculate_car03(x) {

    if (x == 1)
        document.form1.mpg03.value = 52;
    if (x == 2)
        document.form1.mpg03.value = 46;
    if (x == 3)
        document.form1.mpg03.value = 35;
    mpg03 = document.form1.mpg03.value

    if (x == 5)
        document.form1.mil03.value = 6000;
    if (x == 6)
        document.form1.mil03.value = 9000;
    if (x == 7)
        document.form1.mil03.value = 12000;
    car03_mil = document.form1.mil03.value

    car03_co2 = Math.round(100 * car03_mil * 0.0143 / mpg03) / 100;
    if (mpg03 == 0)
        car03_co2 = "";
    document.form1.car03_co2.value = car03_co2;

    calculate_tot();

}
//---------------------------------------------------------------------------------------------
function calculate_car04(x) {

    if (x == 1)
        document.form1.mpg04.value = 52;
    if (x == 2)
        document.form1.mpg04.value = 46;
    if (x == 3)
        document.form1.mpg04.value = 35;
    mpg04 = document.form1.mpg04.value

    if (x == 5)
        document.form1.mil04.value = 6000;
    if (x == 6)
        document.form1.mil04.value = 9000;
    if (x == 7)
        document.form1.mil04.value = 12000;
    car04_mil = document.form1.mil04.value

    car04_co2 = Math.round(100 * car04_mil * 0.0143 / mpg04) / 100;
    if (mpg04 == 0)
        car04_co2 = "";
    document.form1.car04_co2.value = car04_co2;

    calculate_tot();

}
//---------------------------------------------------------------------------------------------

function calculate_foo_sum(v) {

    if (v == 21)
        foo_org = 0.7 // i.e. average
    if (v == 22)
        foo_org = 0.5 // i.e. some
    if (v == 23)
        foo_org = 0.2 // i.e. most
    if (v == 24)
        foo_org = 0 // i.e. all

    document.form1.foo_org.value = foo_org

    if (v == 31)
        foo_mea = 0.6 // i.e. above average
    if (v == 32)
        foo_mea = 0.4 // i.e. average
    if (v == 33)
        foo_mea = 0.25 // i.e. below average
    if (v == 34)
        foo_mea = 0.1 // i.e. veg
    if (v == 35)
        foo_mea = 0 // i.e. vegan

    document.form1.foo_mea.value = foo_mea;

    if (v == 41)
        foo_tra = 0.1 // i.e. minimal
    if (v == 42)
        foo_tra = 0.2 // i.e. below av
    if (v == 43)
        foo_tra = 0.3 // i.e. av
    if (v == 44)
        foo_tra = 0.5 // i.e. above av

    document.form1.foo_tra.value = foo_tra

    if (v == 51)
        foo_pac = 0.05 // i.e. very little - was 0.1
    if (v == 52)
        foo_pac = 0.2 // i.e. below av
    if (v == 53)
        foo_pac = 0.4 // i.e. av
    if (v == 54)
        foo_pac = 0.6 // i.e. above av

    document.form1.foo_pac.value = foo_pac

    if (v == 61)
        foo_com = 1 // i.e. all
    if (v == 62)
        foo_com = 0.5 // i.e. some
    if (v == 63)
        foo_com = 0 // i.e. none

    if (v == 71)
        foo_was = 0.375 // i.e. above average wasted
    if (v == 72)
        foo_was = 0.25 // i.e. average
    if (v == 73)
        foo_was = 0.125 // i.e. below average (50% less)
    if (v == 74)
        foo_was = 0.025 // i.e. very little (90% less)

    foo_com_co2 = (1 - foo_com) * 0.2 * (foo_was + 0.25) / 0.5

    document.form1.foo_com.value = Math.round(foo_com_co2 * 100) / 100

    foo_use_fac = (1 + foo_was) / 1.25 //food use factor = 1 if average, or above or below

    foo_co2 = Math.round((0.2 + foo_org + foo_mea + foo_tra + foo_pac + foo_com_co2) * foo_use_fac * 100) / 100; // (0.2 is hard to avoid)
    document.form1.foo_co2.value = foo_co2;

    calculate_tot();

}

//---------------------------------------------------------------------------------------------

function calculate_mis_sum(v) {


    if (v == 1)
        mis_factor = 1.471 // i.e. above average (5)
    if (v == 2)
        mis_factor = 1.0 // i.e. average (3.4) - was 3.5
    if (v == 3)
        mis_factor = 0.7059 // i.e. below average (2.4) - was 2
    if (v == 4)
        mis_factor = 0.4118 // i.e. much below average (1.4)

    if (v == 21)
        re1_factor = 0 // i.e. no
    if (v == 22)
        re1_factor = 1 // i.e. yes recycle glass, paper and metal

    if (v == 31)
        re2_factor = 0 // i.e. no
    if (v == 32)
        re2_factor = 1 // i.e. yes recycle plastic

    mis_co2 = 3.4 * mis_factor - 0.07 * re1_factor - 0.14 * re2_factor
    mis_co2 = Math.round(mis_co2 * 100) / 100

    document.form1.mis_co2.value = Math.round(mis_co2 * 100) / 100

    calculate_tot();

}
//---------------------------------------------------------------------------------------------
function show_country_mess(cou) {
    alert("This calculator is constructed using values applicable to the UK.  Values for other countries will be roughly the same.  If you would like to help make the calculator more applicable to other countries, please contact us.");
}

//---------------------------------------------------------------------------------------------
function calculate_bus() {

    var bus_wee = document.form1.bus_wee.value * 1;
    var bus_mon = document.form1.bus_mon.value * 1;
    var bus_yea = document.form1.bus_yea.value * 1;

    bus_mil = bus_wee * 48 + bus_mon * 12 + bus_yea;
    bus_co2 = Math.round(bus_mil * 0.0001 * 100) / 100;

    document.form1.bus_mil.value = bus_mil;
    document.form1.bus_co2.value = bus_co2;

    calculate_tot();
}
//---------------------------------------------------------------------------------------------
function calculate_tra() {

    var tra_wee = document.form1.tra_wee.value * 1;
    var tra_mon = document.form1.tra_mon.value * 1;
    var tra_yea = document.form1.tra_yea.value * 1;

    tra_mil = tra_wee * 48 + tra_mon * 12 + tra_yea;
    tra_co2 = Math.round(tra_mil * 0.0001 * 100) / 100;

    document.form1.tra_mil.value = tra_mil;
    document.form1.tra_co2.value = tra_co2;

    calculate_tot();

}
//---------------------------------------------------------------------------------------------
function show_hide_UK(x) {

    if (x == 1) {
        //'no', so hide and reset to zero
        document.getElementById("fliCalTableUK").style.display = "none";
        document.form1.fli_UK.value = "";
        calculate_fli_tot();
    }

    if (x == 2)
        document.getElementById("fliCalTableUK").style.display = "block";

}

//---------------------------------------------------------------------------------------------
function show_hide_eur(x) {

    if (x == 1) {
        document.getElementById("fliCalTableEur").style.display = "none";
        document.form1.fli_eur.value = "";
        calculate_fli_tot();
    }

    if (x == 2)
        document.getElementById("fliCalTableEur").style.display = "block";

}
//---------------------------------------------------------------------------------------------
function calculate_fli_eur() {

    var e2 = document.form1.e2.value;
    var e3 = document.form1.e3.value;
    var e4 = document.form1.e4.value;
    var e5 = document.form1.e5.value;
    var e6 = document.form1.e6.value;
    var e8 = document.form1.e8.value;
    var e10 = document.form1.e10.value;
    var e18 = document.form1.e18.value;
    var e20 = document.form1.e20.value;
    var e24 = document.form1.e24.value;

    var tot = e2 * 2 + e3 * 3 + e4 * 4 + e5 * 5 + e6 * 6 + e8 * 8 + e10 * 10 + e18 * 18 + e20 * 20 + e24 * 24;

    document.form1.fli_eur.value = tot;

    calculate_fli_tot();

}
//---------------------------------------------------------------------------------------------
function show_hide_ame(x) {

    if (x == 1) {
        //'no', so hide and reset to zero
        document.getElementById("fliCalTableAme").style.display = "none";
        document.form1.fli_ame.value = "";
        calculate_fli_tot();
    }

    if (x == 2)
        document.getElementById("fliCalTableAme").style.display = "block";

}

//---------------------------------------------------------------------------------------------
function calculate_fli_ame() {

    var a16 = document.form1.a16.value;
    var a18 = document.form1.a18.value;
    var a20 = document.form1.a20.value;
    var a24 = document.form1.a24.value;
    var a32 = document.form1.a32.value;

    var tot = a16 * 16 + a18 * 18 + a20 * 20 + a24 * 24 + a32 * 32

    document.form1.fli_ame.value = tot;

    calculate_fli_tot();

}
//---------------------------------------------------------------------------------------------
function show_hide_asi(x) {

    if (x == 1) {
        document.getElementById("fliCalTableAsi").style.display = "none";
        document.form1.fli_asi.value = "";
        calculate_fli_tot();
    }

    if (x == 2)
        document.getElementById("fliCalTableAsi").style.display = "block";

}
//---------------------------------------------------------------------------------------------
function calculate_fli_asi() {

    var s8 = document.form1.s8.value;
    var s10 = document.form1.s10.value;
    var s16 = document.form1.s16.value;
    var s18 = document.form1.s18.value;
    var s20 = document.form1.s20.value;
    var s24 = document.form1.s24.value;
    var s48 = document.form1.s48.value;

    var tot = s8 * 8 + s10 * 10 + s16 * 16 + s18 * 18 + s20 * 20 + s24 * 24 + s48 * 48

    document.form1.fli_asi.value = tot;

    calculate_fli_tot();

}

//---------------------------------------------------------------------------------------------
function calculate_fli_tot() {

    var fli_UK = document.form1.fli_UK.value;
    var fli_eur = document.form1.fli_eur.value;
    var fli_ame = document.form1.fli_ame.value;
    var fli_asi = document.form1.fli_asi.value;
    fli_hrs = fli_UK * 1 + fli_eur * 1 + fli_ame * 1 + fli_asi * 1;

    document.form1.fli_hrs.value = fli_hrs;

    fli_co2 = fli_hrs * 0.25;
    document.form1.fli_co2.value = Math.round(fli_co2 * 100) / 100;

    calculate_tot();
}

//---------------------------------------------------------------------------------------------
function calculate_tot() {

    var peo = document.form1.peo.value

    if (peo == 0) {
        alert("You have not entered how many people there are in your household (q.1).  The calculator will assume a value of 1.  You can amend this if necessary");
        peo = 1;
        document.form1.peo.value = peo;
    }

    //household per person (hpp):
    var hpp_co2 = (ele_co2 + gas_co2 + oil_co2 + car01_co2 + car02_co2 + car03_co2 + car04_co2) / peo

    var tot_co2 = hpp_co2 + foo_co2 + mis_co2 + gov_co2 + bus_co2 + tra_co2 + fli_co2
    tot_co2 = Math.round(tot_co2 * 100) / 100
    document.form1.tot_co2.value = tot_co2;

    Show_total_vs_world(tot_co2)
    //saving data via cookie:

    d = new Date();
    d.setFullYear(d.getFullYear() + 10); //i.e. in 10 years time
    expires = "expires=" + d.toGMTString();

    var st = "data=" + peo + "," + ele_kWh + "," + ele_co2 + "," + gas_kWh + "," + gas_co2 + ",";
    st = st + oil_lit + "," + oil_co2 + ",";
    st = st + car01_mil + "," + car01_co2 + "," + car02_mil + "," + car02_co2 + ",";
    st = st + car03_mil + "," + car03_co2 + "," + car04_mil + "," + car04_co2 + ",";
    st = st + foo_co2 + "," + mis_co2 + "," + gov_co2 + ",";
    st = st + bus_mil + "," + bus_co2 + "," + tra_mil + "," + tra_co2 + ","
    st = st + fli_hrs + "," + fli_co2 + "," + tot_co2 + ",";
    //st = st + ",; " + expires ;

    document.cookie = st

}

//---------------------------------------------------------------------------------------------
function Show_total_vs_world(tot) {
    //compared to rest of the world

    document.form1.tot_co2_versus_world.value = tot;

    var max = Math.max(18, tot); // as 18 is the largest of the places shown
    var scale = 300 / max //was 400 until 12.3

    bar = scale * tot;
    if (bar < 1) {
        bar = 1;
    }
    ;
    document.getElementById("your_total").style.width = bar;
    bar = scale * 14.1;
    if (bar < 1) {
        bar = 1;
    }
    ;
    document.getElementById("UK").style.width = bar; //was 10.7
    bar = scale * 4.4;
    if (bar < 1) {
        bar = 1;
    }
    ;
    document.getElementById("World").style.width = bar;
    bar = scale * 17.6;
    if (bar < 1) {
        bar = 1;
    }
    ;
    document.getElementById("USA").style.width = bar;
    bar = scale * 6.2;
    if (bar < 1) {
        bar = 1;
    }
    ;
    document.getElementById("China").style.width = bar;
    bar = scale * 1.8;
    if (bar < 1) {
        bar = 1;
    }
    ;
    document.getElementById("India").style.width = bar;
    bar = scale * 0.3;
    if (bar < 1) {
        bar = 1;
    }
    ;
    document.getElementById("Mozambique").style.width = bar;

}