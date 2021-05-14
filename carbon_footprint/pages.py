from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Demographics(Page):
    form_model = 'player'
    form_fields = ['nationality']

class Energy(Page):
    form_model = 'player'
    #form_fields = ['cf_{}'.format(i) for i in range(1, 4)]
    form_fields = ['hh_members', 'electricity_kwh', 'green_electricity','gas_kwh',
                   'fossil_fuels','fossil_fuels_oil', 'fossil_fuels_coal', 'fossil_fuels_wood', 'fossil_fuels_gas']


    def before_next_page(self):
        # self.player.set_footprint()
        self.player.set_ele_co2()
        self.player.set_gas_co2()
        self.player.set_fossil_fuels_co2()


class Mobility(Page):
    form_model = 'player'
    form_fields = ['car_miles', 'car_size_mpg', 'bus_miles_commute', 'bus_miles_travel',
                   'train_miles_commute', 'train_miles_travel', 'plane_hours']

    def before_next_page(self):
        # self.player.set_footprint()
        self.player.set_car_co2()
        self.player.set_bus_co2()
        self.player.set_train_co2()
        self.player.set_plane_co2()



class Food(Page):
    form_model = 'player'
    form_fields = ['food_org', 'food_meat', 'food_miles', 'food_fresh', 'food_com', 'food_was']

    def before_next_page(self):
        # self.player.set_footprint()
        self.player.set_food_sum_co2()


class Miscellaneous(Page):
    form_model = 'player'
    form_fields = ['mis_spending','mis_res1','mis_res2']

    def before_next_page(self):
        # self.player.set_footprint()
        self.player.set_mis_sum_co2()
        self.player.set_total_footprint()



class Results(Page):
    pass

    def js_vars(self):
        player = self.player
        public_sector = player.gov_co2

        # average values for graph
        avg_elec_heat = player.avg_ele_co2 + player.avg_gas_co2 + player.avg_fossil_fuels_co2
        avg_transportation = player.avg_car_co2 + player.avg_bus_co2 + player.avg_train_co2 + player.avg_plane_co2
        avg_food = player.avg_food_sum_co2
        avg_mis_cons = player.avg_mis_sum_co2

        # personal values for graph
        elec_heat = (player.ele_co2 + player.gas_co2 + player.fossil_fuels_co2) / player.hh_members
        transportation = player.car_co2 + player.bus_co2 + player.train_co2 + player.plane_co2
        food = player.food_sum_co2
        mis_cons = player.mis_sum_co2
        return dict(
            public_sector= public_sector,
            avg_elec_heat=avg_elec_heat,
            avg_transportation=avg_transportation,
            avg_food=avg_food,
            avg_mis_cons=avg_mis_cons,
            elec_heat_i= elec_heat,
            transportation_i= transportation,
            food_i=food,
            mis_cons_i=mis_cons,
        )


page_sequence = [Energy, Mobility, Food, Miscellaneous, Results]
