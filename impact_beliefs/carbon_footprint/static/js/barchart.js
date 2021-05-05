AmCharts.makeChart("chartdiv",

{
	"type": "serial",
	"categoryField": "category",
	"columnSpacing": 100,
	"marginLeft": 61,
	"startDuration": 1,
	"accessibleTitle": "yourcarbonfootprint",
	"precision": 2,
	"theme": "default",
	"categoryAxis": {
		"gridPosition": "start",
		"autoGridCount": false,
		"gridAlpha": 0
	},
	"trendLines": [],
    	"graphs": [
		{
			"balloonText": "[[title]]: [[value]]",
			"fillAlphas": 1,
			"fillColors": "#EBCD52",
			"id": "AmGraph-1",
			"lineColor": "#EBCD52",
			"title": "Public Sector",
			"type": "column",
			"valueField": "Public Sector"
		},
		{
			"balloonText": "[[title]]: [[value]]",
			"fillAlphas": 1,
			"fillColors": "#E16149",
			"id": "AmGraph-2",
			"lineColor": "#E16149",
			"title": "Electricity & Heating",
			"type": "column",
			"valueField": "Electricity & Heating"
		},
		{
			"balloonText": "[[title]]: [[value]]",
			"fillAlphas": 1,
			"fillColors": "#9ADCC9",
			"id": "AmGraph-3",
			"lineColor": "#9ADCC9",
			"title": "Transportation",
			"type": "column",
			"valueField": "Transportation"
		},
		{
			"balloonText": "[[title]]: [[value]]",
			"fillAlphas": 1,
			"fillColors": "#473147",
			"id": "AmGraph-4",
			"lineColor": "#473147",
			"title": "Food",
			"type": "column",
			"valueField": "Food"
		},
		{
			"balloonText": "[[title]]: [[value]]",
			"fillAlphas": 1,
			"fillColors": "#BAB19E",
			"id": "AmGraph-5",
			"lineColor": "#BAB19E",
			"title": "Other Consumption",
			"type": "column",
			"valueField": "Other Consumption"
		}
	],
	"guides": [],
	"valueAxes": [
		{
			"id": "ValueAxis-1",
			"minimum": 0,
			"stackType": "regular",
			"axisColor": "#515151",
			"gridAlpha": 0,
			"title": "Tonnes of CO2 (per year)",
			"titleBold": false,
			"titleRotation": -90
		},
		{
			"id": "ValueAxis-4",
			"precision": -1,
			"synchronizationMultiplier": -1
		}
	],
	"allLabels": [],
	"balloon": {},
	"legend": {
		"enabled": true,
		"useGraphSettings": true
	},
	"titles": [
		{
			"id": "Title-1",
			"size": 15,
			"text": "Your Carbon Footprint"
		}
	],
	"dataProvider": [
		{
			"category": "Average Household",
			"Public Sector": js_vars.public_sector,
			"Electricity & Heating": js_vars.avg_elec_heat,
			"Transportation": js_vars.avg_transportation,
			"Food": js_vars.avg_food,
			"Other Consumption": js_vars.avg_mis_cons,
		},
		{
			"category": "You",
			"Public Sector": js_vars.public_sector,
			"Electricity & Heating": js_vars.elec_heat_i,
			"Transportation": js_vars.transportation_i,
			"Food": js_vars.food_i,
			"Other Consumption": js_vars.mis_cons_i,
		}
	]
}

);


