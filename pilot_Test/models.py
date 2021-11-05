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


doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""


class Constants(BaseConstants):
    name_in_url = 'study'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # background vars
    starting_time = models.LongStringField(doc="Time at which Informed Consent is given and experiment starts")
    finishing_time = models.LongStringField(doc="Time at which last page is reached")
    is_mobile = models.BooleanField(doc="Automatic check through JS whether gadget is phone or not")
    window_width = models.IntegerField(blank=True, doc="Documents the respondent's browser window's width.")
    window_height = models.IntegerField(blank=True, doc="Documents the respondent's browser window's height.")

    # Characteristics of Project A
    project_id_A = models.IntegerField()
    price_A = models.FloatField()
    num_x_true_A = models.IntegerField()
    num_x_belief_A = models.IntegerField(min=0, max=400, doc="records belief on number of Xs in matrix")
    num_x_belief_min_A = models.IntegerField(min=0, max=400, doc="records min belief on number of Xs in matrix")
    num_x_belief_max_A = models.IntegerField(min=0, max=400, doc="records max belief on number of Xs in matrix")

    # Characteristics of Project B
    project_id_B = models.IntegerField()
    price_B = models.FloatField()
    num_x_true_B = models.IntegerField()
    num_x_belief_B = models.IntegerField(min=0, max=400, doc="records belief on number of Xs in matrix")
    num_x_belief_min_B = models.IntegerField(min=0, max=400, doc="records belief on number of Xs in matrix")
    num_x_belief_max_B = models.IntegerField(min=0, max=400, doc="records belief on number of Xs in matrix")

    # Feedback
    fun = models.IntegerField(min=0, max=10, label="How much did you enjoy the estimation task?",
                              widget = widgets.RadioSelectHorizontal, choices = range(0, 11))
    difficult = models.IntegerField(min=0, max=10, label="How difficult did you find the estimation task?",
                              widget = widgets.RadioSelectHorizontal, choices = range(0, 11))
    comments = models.LongStringField(blank=True, label="Do you have any additional feedback for us?")
