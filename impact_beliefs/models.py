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
import random
import csv
from otree.db.models import ForeignKey
from slider_task.models import BaseSlider, SliderPlayer

author = 'Frauke Stehr'

doc = """
Experiment on motivated beliefs of impact of other-regarding behavior"""


class Constants(BaseConstants):
    name_in_url = 'impact_beliefs'
    players_per_group = None

    # Get experimental parameters from csv file
    with open('impact_beliefs/Parameters.csv', encoding='utf-8-sig') as parameters:
        paras = list(csv.DictReader(parameters, dialect='excel'))

    num_work_rounds = 1
    num_decision_rounds = len(paras) * 4
    num_rounds = num_decision_rounds + num_work_rounds
    endowment = 280
    beliefs_fixed_payment = 150
    beliefs_max_payment = 2 * beliefs_fixed_payment

    # slider_columns = 3  # uncomment this if you want sliders in the slider task to be displayed in multiple columns
    num_sliders = 1

    real_world_kg_co2_per_x = 0.5
    car_km_per_kg_co2 = 6  # source: atmosfair.de


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.session.get_participants():
                paras = Constants.paras.copy()

                # generate participant varlist for beliefs by part, to store beliefs using project_id
                p.vars['beliefs_part1'] = [0] * len(paras)
                p.vars['beliefs_part3'] = [0] * len(paras)

                # randomize the order of projects on participant level, but within part and store as participant varlist
                random.shuffle(paras)
                new_paras = Constants.paras.copy()  # defines a helplist of parameters, which is shuffled then appended to original paras list
                for i in [0, 1, 2]:  # repeat three times to get four parts (original + 3 times shuffled)
                    random.shuffle(new_paras)  # shuffles helplist
                    paras = paras + new_paras  # appends shuffled helplist to list of parameters
                p.vars[
                    'parameters'] = paras  # store shuffled list of parameters in participant vars, then access each element by round number
                # print(p.vars['parameters'])  # prints participant vars to double check randomization

                # randomly assign treatment order to participants
                orders = ["NeutralMotivated", "MotivatedInfo"]
                p.vars['order'] = random.choice(orders)

                # randomly assign payment round
                rounds = range(1, Constants.num_rounds + 1)
                p.vars['payment_round'] = random.choice(rounds)
                print("Payment round is", p.vars['payment_round'])

            for p in self.get_players():
                p.prepare_sliders(num=Constants.num_sliders, min=0, max=100)

        for p in self.get_players():
            # Define "part" variable in the beginning of the experiment
            if self.round_number == 1:
                p.part = 0
                p.round_type = "effort"
            elif self.round_number <= len(Constants.paras) + 1:
                p.part = 1  # belief rounds 1
                p.round_type = "belief"
            elif self.round_number <= len(Constants.paras) * 2 + 1:
                p.part = 2  # donation rounds 1
                p.round_type = "donation"
            elif self.round_number <= len(Constants.paras) * 3 + 1:
                p.part = 3  # belief rounds 2
                p.round_type = "belief"
            else:
                p.part = 4  # donation rounds 2
                p.round_type = "donation"

            # Assign treatment to players in all rounds using treatment order assigned in first round
            if p.participant.vars['order'] == "NeutralMotivated":
                p.order = "NeutralMotivated"
                if p.part == 0:
                    p.treatment = ""
                elif p.part == 1 or p.part == 2:
                    p.treatment = "Neutral"
                else:
                    p.treatment = "Motivated"
            elif p.participant.vars['order'] == "MotivatedInfo":
                p.order = "MotivatedInfo"
                if p.part == 0:
                    p.treatment = ""
                elif p.part == 1 or p.part == 2:
                    p.treatment = "Motivated"
                else:
                    p.treatment = "Info"


class Group(BaseGroup):
    pass


class Player(SliderPlayer):
    part = models.IntegerField()
    round_type = models.StringField()
    order = models.StringField()
    treatment = models.StringField()

    gif_clicked = models.BooleanField(blank=True,)

    num_x_belief = models.IntegerField(min=0, max=400)
    donation = models.BooleanField(
        choices=[
            [False, 'No'],
            [True, 'Yes'],
        ]
    )
    project_id = models.IntegerField()
    num_x_true = models.IntegerField()
    price = models.FloatField()

    current_payoff = models.FloatField()

    co2_belief_car = models.FloatField(label="Live car-free",)
    co2_belief_plane = models.FloatField(label="Avoid one transatlantic round-trip flight",)
    co2_belief_renewables = models.FloatField(label="Use renewable energy at home",)
    co2_belief_hybrid = models.FloatField(label="Replace a typical car with hybrid",)
    co2_belief_vegan = models.FloatField(label="Adopt a plant-based diet",)
    co2_belief_laundry = models.FloatField(label="Wash clothes in cold water",)
    co2_belief_recycle = models.FloatField(label="Recycle your waste",)
    co2_belief_dryer = models.FloatField(label="Air-dry clothes",)
    co2_belief_led = models.FloatField(label="Use LED-bulbs at home",)

    cost_belief_car = models.FloatField(label="Live car-free",)
    cost_belief_plane = models.FloatField(label="Avoid one transatlantic round-trip flight",)
    cost_belief_renewables = models.FloatField(label="Use renewable energy at home",)
    cost_belief_hybrid = models.FloatField(label="Replace a typical car with hybrid",)
    cost_belief_vegan = models.FloatField(label="Adopt a plant-based diet",)
    cost_belief_laundry = models.FloatField(label="Wash clothes in cold water",)
    cost_belief_recycle = models.FloatField(label="Recycle your waste",)
    cost_belief_dryer = models.FloatField(label="Air-dry clothes",)
    cost_belief_led = models.FloatField(label="Use LED-bulbs at home",)


class Slider(BaseSlider):  # Class that is needed for the slider task
    player = ForeignKey(Player,
                        on_delete=models.CASCADE,
                        )
