from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import csv

author = 'Your name here'

doc = """
Carbon Footprint Calculator
"""


class Constants(BaseConstants):
    name_in_url = 'carbon_footprint'
    players_per_group = None
    num_rounds = 1

    # Import Country List
    with open('carbon_footprint/nationality.csv') as f:
        next(f, None)  # Skip the first line
        countries = list(csv.reader(f))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Fields for UK Average Emissions
    avg_ele_co2 = models.FloatField()
    avg_gas_co2 = models.FloatField()
    avg_fossil_fuels_co2 = models.FloatField()
    avg_car_co2 = models.FloatField()
    avg_bus_co2 = models.FloatField()
    avg_train_co2 = models.FloatField()
    avg_plane_co2 = models.FloatField()
    avg_food_sum_co2 = models.FloatField()
    avg_mis_sum_co2 = models.FloatField()


    # Demographics
    nationality = models.StringField(
        label="Please specify your nationality",
        choices=Constants.countries)

    age = models.IntegerField(
        label="Please specify your age (e.g. 24):",
        min=18,
        max=99,
    )

    # CO2 Emission fields.
    ele_co2 = models.FloatField(initial=0)
    gas_co2 = models.FloatField(initial=0)
    fossil_fuels_co2 = models.FloatField(initial=0)
    car_co2 = models.FloatField(initial=0)
    food_sum_co2 = models.FloatField(initial=0)
    bus_co2 = models.FloatField(initial=0)
    train_co2 = models.FloatField(initial=0)
    plane_co2 = models.FloatField(initial=0)
    mis_sum_co2 = models.FloatField(initial=0)
    total_footprint_co2 = models.FloatField(initial=0)

    def set_ele_co2(self):
        # EXPLANATIONS
        # - There is a reduction of 25% in CO2 emissions, if the electricity comes from a renewable energy tariff
        # -> ele_ren changes from 1 to 0.75, if the green_electricity check box is clicked.
        # - CO2 factor for electricity = 0.309 kg / kWh -> 0.000309 tonnes / kwH.

        # CONSTANTS
        co2_fac_ele = 0.000309
        avg_ele_kwh = 4800

        ele_ren = 1
        if self.green_electricity:
            ele_ren = 0.75
        avg_ele_ren = 0.75 # this reflects energy mix

        # CALCULATION
        self.ele_co2 = round(self.electricity_kwh * ele_ren * co2_fac_ele * 100) / 100
        self.avg_ele_co2 = round(avg_ele_kwh * avg_ele_ren * co2_fac_ele * 100) / 100


    def set_gas_co2(self):
        # EXPLANATIONS
        # - CO2 factor for natural gas is 0.203 kg / kWh -> 0.000203 tonnes / kwH

        # CONSTANTS
        co2_fac_gas = 0.000203
        avg_gas_kwh=16000

        # CALCULATION
        self.gas_co2 = round(self.gas_kwh * co2_fac_gas * 100) / 100
        self.avg_gas_co2 = round(avg_gas_kwh * co2_fac_gas * 100) / 100


    def set_fossil_fuels_co2(self):
        # EXPLANATIONS
        # - The following Co2 factors are used:
        # - Oil: 2.96 kg / litre -> 0.00296 tonnes / litre
        # - Coal: 3.26 kg / kg -> 0.00326 tonnes / kg
        # - Wood: 0.10 kg / kg -> 0.0001 tonnes / kg
        # - Bottled gas: 3.68 kg / kg -> 0.00368 tonnes / kg

        # CONSTANTS
        co2_fac_oil = 0.00296
        co2_fac_coal = 0.00326
        co2_fac_wood = 0.0001
        co2_fac_bg = 0.00368

        avg_oil = 0   # Check whether you can find values for this
        avg_coal = 0
        avg_wood = 0
        avg_bg = 0

        # CALCULATION
        if self.fossil_fuels: # == if oil, coal, wood or gas is used
            self.fossil_fuels_co2 = round(self.fossil_fuels_oil * co2_fac_oil * 100 +
                                          self.fossil_fuels_coal * co2_fac_coal * 100 +
                                          self.fossil_fuels_wood * co2_fac_wood * 100 +
                                          self.fossil_fuels_gas * co2_fac_bg * 100) / 100
        else:
            self.fossil_fuels_co2 = 0

        self.avg_fossil_fuels_co2 = round(avg_oil * co2_fac_oil * 100 +
                                          avg_coal * co2_fac_coal * 100 +
                                          avg_wood * co2_fac_wood * 100 +
                                          avg_bg * co2_fac_bg * 100) / 100

    def set_car_co2(self):
        # EXPLANATIONS
        # - Emissions are taken to be 14.3 kg CO2 per gallon. --> 0.0143 tonnes per gallon

        # CONSTANTS
        co2_fac_car = 0.0143
        avg_mileage_priv_car = 9000
        avg_car_mpg = 52 # assume avg car is city car

        # CALCULATION
        if self.car_miles > 0: # if any option except "I never travel by car" is clicked
            self.car_co2 = round(100 * self.car_miles * co2_fac_car / self.car_size_mpg) / 100
        else:
            self.car_co2 = 0
        self.avg_car_co2 = round(100 * avg_mileage_priv_car * co2_fac_car / avg_car_mpg) / 100


    def set_food_sum_co2(self):
        # EXPLANATION
        # - The rotting of unused food in landfill sites releases gases (methane + CO2) that amounts to ~ 0.2 tonnes per person
        # --> Composting or re-using food residues could save most of this i.e. 0.2 tonnes per person.
        #     This amount would be more or less depending on how much edible food is wasted.
        # - food_com = factor that is composted -> 0 = ALL, 0.5 = SOME; 1 = NONE
        # --> The more is composted the smaller the CO2 impact
        # - Average amount of co2 that is "saved" due to composting = 0.2 tonnes / per person
        # - (food_was + 0.25) = ?? Not quite sure yet


        #CONSTANTS:
        ave_co2_sav = 0.2
        self.avg_food_sum_co2 = 2.2   # found on website

        food_com_co2 = self.food_com * ave_co2_sav * (self.food_was + 0.25) / 0.5

        # This factor depends on the amount of food that is wasted. The factor can have the following values:
        # Above average (50% more) -> 1.1
        # Average -> 1
        # Below average (50% less) -> 0.9
        # Very little (90% less) -> 0.82

        food_use_fac = (1 + self.food_was) / 1.25

        # Food sum calculation / 0.2 is hard to avoid
        self.food_sum_co2 = round((0.2 + self.food_org + self.food_meat + self.food_miles +
                                  self.food_pac + food_com_co2) * food_use_fac * 100) / 100


    def set_bus_co2(self):
        # EXPLANATIONS
        # - The CO2 emission factor for bus travel is taken to be 100 g/mile --> 0.0001 tonnes / mile
        # - Number of weeks in a year minus vacation is approximately 48.

        # CONSTANTS
        co2_fac_bus = 0.0001
        weeks_in_year = 48

        # CALCULATION
        bus_miles_year = self.bus_miles * weeks_in_year
        avg_bus_miles_year = 48 * 10**3 / 66 # = total passenger km/ population size in millions
        self.bus_co2 = round(bus_miles_year * co2_fac_bus * 100) / 100
        self.avg_bus_co2 = round(avg_bus_miles_year * co2_fac_bus * 100) / 100


    def set_train_co2(self):
        # EXPLANATIONS
        # - The CO2 emission factor for train travel is taken to be 100 g/mile --> 0.0001 tonnes / mile
        # - Number of weeks in a year minus vacation is approximately 48.

        # CONSTANTS
        co2_fac_train = 0.0001
        weeks_in_year = 48
        avg_train_miles_year = 68.6 * 10**3 / 66 # = total passenger km/ population size in millions. Source: http://dataportal.orr.gov.uk/statistics/usage/passenger-rail-usage/table-1230-passenger-kilometres/

        # CALCULATION
        train_miles_year = self.train_miles * weeks_in_year
        self.train_co2 = round(train_miles_year * co2_fac_train * 100) / 100
        self.avg_train_co2 = round(avg_train_miles_year * co2_fac_train * 100) / 100

    def set_plane_co2(self):
        # EXPLANATION
        # CO2 emission factor is taken to be of 0.25 tonnes / per hour flying.

        # CONSTANTS
        co2_fac_plane = 0.25
        avg_plane_hours = 3.99

        # CALCULATION
        self.plane_co2 = self.plane_hours * co2_fac_plane
        self.avg_plane_co2 = avg_plane_hours * co2_fac_plane


    def set_mis_sum_co2(self):
        # EXPLANATION
        # - Average miscellaneous spendings is estimated to produce 3.4 tonnes of CO2.
        # --> Above-average = 5 tonnes CO2, Below-average = 2.4 tonnes CO2), Much below-average = 1.4 tonnes CO2
        # - This number is influenced by the amount of spending plus recycling behavior
        # - Recycling paper, glass and metal reduces CO2 amount by 0.07 tonnes
        # - Recycling plastic apart from bags reduces CO2 amount by 0.14 tonnes
        # - These amounts are subtracted if the corresponding check boxes are clicked.

        # CONSTANTS
        res1_reduction = 0.07
        res2_reduction = 0.14
        avg_mis_spending = 3.4
        avg_recycling_rate = 0.45  # Source: https://www.gov.uk/government/statistical-data-sets/env23-uk-waste-data-and-management

        # CALCULATION
        self.mis_sum_co2 = self.mis_spending - res1_reduction * self.mis_res1 - res2_reduction * self.mis_res2
        self.mis_sum_co2 = round(self.mis_sum_co2 * 100) / 100

        self.avg_mis_sum_co2 = avg_mis_spending - avg_recycling_rate * ( res1_reduction + res2_reduction)
        self.avg_mis_sum_co2 = round(self.avg_mis_sum_co2 * 100) / 100


    def set_total_footprint(self):
        # EXPLANATION
        # - The CO2 emissions produced by electricity, gas and fossil fuels are added and
        #   shared among all household members. --> The more hh members, the smaller the individual
        #   CO2 impact.
        # - All CO2 emission fields are added up.

        # CALCULATION
        hpp_co2 = (self.ele_co2 + self.gas_co2 + self.fossil_fuels_co2) / self.hh_members

        self.total_footprint_co2 = round((hpp_co2 + self.car_co2 + self.food_sum_co2 +
                                          self.mis_sum_co2 + self.gov_co2 + self.bus_co2
                                          + self.train_co2 + self.plane_co2) * 100) / 100




    # Calculator questions
    hh_members = models.FloatField(label="How many people are there in your household?",
                             min=1.0,
                             max=10.0)

    electricity_kwh = models.IntegerField(widget=widgets.RadioSelect,
                               label="How much electricity is used in your household?",
                               min=0)

    green_electricity = models.BooleanField(widget=widgets.CheckboxInput,
                                    label="Tick the box if your electricity comes from a renewable energy tariff",
                                    blank=True)


    gas_kwh = models.IntegerField(widget=widgets.RadioSelect,
                               label="How much gas is used in your household?",
                               min=0)


    fossil_fuels = models.BooleanField(widget=widgets.RadioSelectHorizontal,
                             label="Is heating oil, coal, wood or bottled gas used in your household?",
                             choices=[
                                 [False, 'No'],
                                 [True, 'Yes'],
                             ])

    fossil_fuels_oil = models.IntegerField(label="The number of litres of heating oil:",
                                           blank=True,
                                           min=0,
                                           initial=0
                                           )

    fossil_fuels_coal = models.IntegerField(label="The number of kilograms of coal:",
                                            blank=True,
                                            min=0,
                                            initial=0
                                            )

    fossil_fuels_wood = models.IntegerField(label="The number of kilograms of wood:",
                                            blank=True,
                                            min=0,
                                            initial=0
                                            )

    fossil_fuels_gas = models.IntegerField(label="The number of kilograms of bottled gas:",
                                           blank=True,
                                           min=0,
                                           initial=0
                                           )



    car_miles = models.IntegerField(widget=widgets.RadioSelect,
                               label="How many miles have you travelled by car in the past 12 months"
                                     " (as driver or passenger)?",
                               min=0) # Fragenformulierung von WWF Rechner Schweiz


    car_size_mpg = models.IntegerField(widget=widgets.RadioSelect,
                                       label="Select the size of your most used car:",
                                       blank=True,
                                       initial=-99, # Average if subject forgets to click. Improve this!
                                       choices=[
                                           [35, "Sports car or large SUV"],
                                           [46, "Small or medium SUV, or MPV"],
                                           [52, "City, small, medium, large or estate car"],
                                       ]
                                       )

    food_org = models.FloatField(widget=widgets.RadioSelect,
                               label="How much of the food that you eat is organic?",
                               choices=[
                                   [0.7, "None"],
                                   [0.5, "Some"],
                                   [0.2, "Most"],
                                   [0.0, "All"]
                               ])

    food_meat = models.FloatField(widget=widgets.RadioSelect,
                               label="Compared to others in your country, how much meat/dairy do you eat personally?",
                               choices=[
                                   [0.6, "Above-average meat/dairy"],
                                   [0.4, "Average meat/dairy"],
                                   [0.25, "Below-average meat/dairy"],
                                   [0.1, "Lacto-vegetarian"],
                                   [0.0, "Vegan"]
                               ])

    food_miles = models.FloatField(widget=widgets.RadioSelect,
                               label="Compared to others in your country, how much of your food is produced locally?",
                               choices=[
                                   [0.5, "Very little (much foreign / out of season food)"],
                                   [0.3, "Average"],
                                   [0.2, "Above average"],
                                   [0.1, "Almost all"]
                               ])

    food_pac = models.FloatField(widget=widgets.RadioSelect,
                               label="Compared to others in your country, how much of your food is packaged / processed (e.g. 'ready meals', tins)?",
                               choices=[
                                   [0.6, "Above average"],
                                   [0.4, "Average"],
                                   [0.2, "Below average"],
                                   [0.05, "Very little"]
                               ])

    food_com = models.FloatField(widget=widgets.RadioSelect,
                               label="How much of your unused food (potato peelings, leftovers, etc.) do you compost?",
                               choices=[
                                   [1.0, "None"], #NOT CO2 values
                                   [0.5, "Some"],
                                   [0.0, "All"]
                               ])

    food_was = models.FloatField(widget=widgets.RadioSelect,
                               label="How much food do you waste? (On average, over one fifth of edible food is thrown away)",
                               choices=[
                                   [0.375, "Above average"], #NOT CO2 values
                                   [0.25, "Average"],
                                   [0.125, "Below average"],
                                   [0.025, "Very little"]
                               ])

    # Public Sector Emissions (unavoidable)
    gov_co2 = models.FloatField(initial=1.1)


    bus_miles = models.FloatField(label="How many miles do you travel by bus each weak?",
                                  min=0)

    train_miles = models.FloatField(label="How many miles do you travel by train each weak?",
                                    min=0)

    plane_hours = models.FloatField(label="How many hours have you travelled by plane in an average year before the pandemic?",
                                    min=0)


    mis_spending = models.FloatField(widget=widgets.RadioSelect,
                                   label="How would you classify the level of your miscellaneous spending (e.g., on clothing, recreating, hygiene)?",
                                   choices=[
                                       [5, "Above-average"],
                                       [3.4, "Average"],
                                       [2.4, "Below-average"],
                                       [1.4, "Much below-average"],
                                   ])

    mis_res1 = models.IntegerField(widget=widgets.RadioSelect,
                                   label="Do you recycle paper, glass and metal?",
                                   choices=[
                                       [0, "No"],
                                       [1, "Yes"],
                                   ])

    mis_res2 = models.IntegerField(widget=widgets.RadioSelect,
                                   label="Do you recycle plastic apart from bags?",
                                   choices=[
                                       [0, "No"],
                                       [1, "Yes"],
                                   ])



# To Do Today:
# - Check if calculations are correct : DONE
# - Make javascript for mpg car question
# - handle the carbon factors -> include them in the calculation functions: DONE
# - improve calculations where needed: DONE

# STILL TO DO:
# - Explain (and maybe improve) food calculation
# - figure out how to keep current answers on page re-load to display error-messages
# --> https://stackoverflow.com/questions/38930144/keep-input-value-after-refresh-page

# IDEAS:
# - From otree doc: After the field has been set, you can access the human-readable name using get_FIELD_display, like this: player.get_level_display() # returns e.g. 'Medium'.
# - Make multiple functions for calculations fot better overview. -> One for electricity, one for gas etc.
# - blank = True --> adjust dynamically if possible. --> if certain option is chosen a field should be mandatory
#   (e.g. subject chose number of cars = 3 --> All subsequent fields must be filled out)
# - make tooltips using bootstrap pop-over https://www.w3schools.com/bootstrap/bootstrap_popover.asp
# - Make 2 versions, one that gives immediate feedback of the CO2 values that are calculated and without feedback


# PROBLEMS:


# TO DO:
# - Abgleichen ob der Rechner das gleiche ausspuckt wie der https://carbonindependent.org/
# - Logik bei dynamischen Feldern anpassen
# - miles per gallon in liters per km umrechnen
# - Währungen & Maßeinheiten (miles, gallons, etc) dynamisch anpassen. --> zu Beginn statische Struktur für GB
#  -->background emissions UK: https://carbonindependent.org/#more%20notes q7.
# - Dropout Spieler handeln.
# - Should we add the notes from the calculator as info for the subjects?
# - Q8: Nur pro Jahr oder Woche nicht alle drei Möglichkeiten/ aufsplitten in Öv und Fernbus
# - Q10: Flüge: Frage in Flugstunden stellen. Evt. noch aufsplitten in Kurz und Langstrecke falls wir zahlen kennen
# - Q6: Check how food calculations works the values depend on each other

# ----------------------------------------------------------------------------
# HARD CODED NUMBERS FOR CALCULATIONS - Think about what to do with those
#
# ELECTRICITY
# - CO2 factor for electricity = 0.309 kg / kWh
# - There is a reduction of 25% (ele_ren = 0.75 or 1) in CO2 emissions for the green tariffs listed.
#   --> ele_ren changes depending on whether or not the green_electricity field was checked.
#
# GAS
# - CO2 factor for natural gas is 0.203 kg / kWh
#
# FOSSIL FUELS
# - For oil: 2.96 kg / litre
# - For coal: 3.26 kg / kg
# - For wood: 0.10 kg / kg
# - For bottled gas: 3.68 kg / kg
#
# FOOD
# - It's a bit complicated for food check set_food_sum_co2 function
#
# BUS / TRAIN JOURNEYS
# - 100 g CO2 per mile.
#
# PLANE JOURNEYS
# - The calculator assumes greenhouse gas emissions of 1/4 tonne CO2 equivalent per hour flying.
#
# MISCELLANEOUS
# - Average miscellaneous spendings is estimated to produce 3.4 tonnes of CO2.
# - This number is influenced by the amount of spending plus recycling behavior
# - Recycling paper, glass and metal reduces CO2 amount by 0.07 tonnes
# - Recycling plastic apart from bags reduces CO2 amount by 0.14 tonnes
#
# ----------------------------------------------------------------------------