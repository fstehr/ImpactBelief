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
import itertools    # allows to balance treatments
from otree.db.models import ForeignKey

doc = """
This is a pilot snippet testing the parameters of the donation task. Half the subjects get a lower endowment to see 
how much this affects donation behavior. All currency veriables are in US Dollars. Pilot is with full impact information.
"""


class Constants(BaseConstants):
    name_in_url = 'study'
    players_per_group = None

    # Get experimental parameters from csv file
    with open('pilot_donations/static/Parameters.csv', encoding='utf-8-sig') as parameters:
        paras = list(csv.DictReader(parameters, dialect='excel'))

    num_rounds = len(paras)

    # timing parameters for display
    duration_min = 10
    endowment_lo = 40
    endowment_hi = 50

    min_price = 12.75
    max_price = 157.25


class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize parameter order on subject level
        if self.round_number == 1:
            for p in self.session.get_participants():
                paras = Constants.paras.copy()
                random.shuffle(paras)

                p.vars['parameters'] = paras  # store shuffled list of parameters in participant vars, then access each element by round number
                # print(p.vars['parameters'])  # prints participant vars to double check randomization

                # assign one payment round
                rounds = range(1, Constants.num_rounds + 1)
                p.vars['payment_round'] = random.choice(rounds)
                print("Payment round is", p.vars['payment_round'])

        # assign hi and lo endowment to half the sample
        endowments = itertools.cycle([Constants.endowment_lo, Constants.endowment_hi])

        for p in self.get_players():
            p.endowment = next(endowments)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # background vars
    starting_time = models.LongStringField(doc="Time at which Informed Consent is given and experiment starts")
    finishing_time = models.LongStringField(doc="Time at which last page is reached")
    is_mobile = models.BooleanField(doc="Automatic check through JS whether gadget is phone or not")
    window_width = models.IntegerField(blank=True, doc="Documents the respondent's browser window's width.")
    window_height = models.IntegerField(blank=True, doc="Documents the respondent's browser window's height.")
    attention_check = models.StringField(blank=True, doc="Filter question for attention.",
                                          label="To make sure you have read the instructions, we ask you to answer 'apple' in the field below.")

    endowment = models.IntegerField()

    # Characteristics of Project A
    num_doses_A = models.IntegerField()
    price_A = models.IntegerField()
    efficiency_A = models.FloatField()
    donation_A = models.BooleanField(widget=widgets.RadioSelectHorizontal,
                                     choices=[
                                         [True, 'Yes'],
                                         [False, 'No'],
                                     ]
                                     )
    current_payoff = models.IntegerField()

    # # Characteristics of Project B
    # num_doses_B = models.IntegerField()
    # price_B = models.IntegerField()
    # efficiency_B = models.IntegerField()
    # donation_B = models.BooleanField(widget=widgets.RadioSelectHorizontal,
    #                                  choices=[
    #                                      [True, 'Yes'],
    #                                      [False, 'No'],
    #                                  ]
    #                                  )

    # Feedback
    altruism = models.IntegerField(
        choices=range(0, 11),
        widget=widgets.RadioSelectHorizontal,
        label='How do you assess your willingness to share with others without expecting anything in '
              'return when it comes to charity? Please click on the slider to indicate where you fall on the scale.')

    giving_type = models.IntegerField(
        label="Think about the last time you gave to charity before today. What was most important to you when you decided to donate?",
        widget=widgets.RadioSelect,
        choices=[
            [1, 'the cause the charity supported'],
            [2, 'feeling good about myself for donating'],
            [3, 'maximizing the societal impact of my donation'],
            [4, 'being able to tell/show others that I donated'],
            [5, 'some other aspect of giving']
        ]
        )

# TO DO
# - check whether parameters make sense for a pilot
# - write instructions
# - make screen design for decision screen nicer (See sketch ppt)
# - fix slider altruism question (OBS use lars' change slider class snippet to make slider mandatory without anchoring)
# - fix layout of radio buttons on questionnaire site

# - randomize order of project A & B (i.e. from csv file to html)
# - include pictures in instructions -> donation impact
# - emphasize that there is no (immediate) feedback on belief accuracy!
# - code belief etc. data s.t. the data is called proj low and proj hi ?
# --> randomization of order of display is done on html level
# - include warm glow survey item from Carpenter (2021) JEBO "Think about the last time you gave to charity before today. What was most important to you (i) the total amount given by everyone, (ii) the amount that you personally gave or (iii) some other aspect of giving?”

# The form field page_loaded has errors, but its error message is not being displayed, possibly because you did not include the field in the page. There are 2 ways to fix this:
#
# Include the field with the formfield tag, e.g. {% formfield player.page_loaded %}
# If you are not using formfield but are instead writing the raw HTML for the form input, remember to include {{ form.page_loaded.errors }} somewhere in your page's HTML.