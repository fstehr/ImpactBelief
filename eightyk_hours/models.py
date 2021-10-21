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

author = 'Your name here'

doc = """
Your app description
"""


def make_likert_field(label):  # create a Likert type field with a 10 point scale form 0 to 10, with the argument 'label'
    choices = range(0, 11)
    return models.IntegerField(
        choices=choices,
        widget=widgets.RadioSelect,
        label=label,
    )



class Constants(BaseConstants):
    name_in_url = 'eightyk_hours'
    players_per_group = None

    # Get items from csv file
    with open('eightyk_hours/static/proposals.csv', encoding='utf-8-sig') as parameters:
        items = list(csv.DictReader(parameters, dialect='excel'))
        # create sub-dictionaries for each topic-based table
        environment = []
        politics = []
        education = []
        decision = []
        society = []
        health = []

        for i in range(len(items)):
            if items[i]['header1'] == "Umwelt":
                environment.append(items[i])
            elif items[i]['header1'] == "Politische Partizipation":
                politics.append(items[i])
            elif items[i]['header1'] == "Bildung":
                education.append(items[i])
            elif items[i]['header1'] == "Qualität von Entscheidungen":
                decision.append(items[i])
            elif items[i]['header1'] == "Gesellschaftlicher Zusammenhalt":
                society.append(items[i])
            elif items[i]['header1'] == "Global Health":
                health.append(items[i])
            print(len(environment), len(politics), len(education), len(decision), len(society), len(health))

    num_rounds = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # generate many fields for each item and question

    # For environmental items
    env1 = make_likert_field(Constants.environment[0]["item"])
    env2 = make_likert_field(Constants.environment[1]["item"])
    env3 = make_likert_field(Constants.environment[2]["item"])
    env4 = make_likert_field(Constants.environment[3]["item"])
    env5 = make_likert_field(Constants.environment[4]["item"])
    env6 = make_likert_field(Constants.environment[5]["item"])
    env7 = make_likert_field(Constants.environment[6]["item"])
    env8 = make_likert_field(Constants.environment[7]["item"])
    env9 = make_likert_field(Constants.environment[8]["item"])
    env10 = make_likert_field(Constants.environment[9]["item"])
    env11 = make_likert_field(Constants.environment[10]["item"])
    env12 = make_likert_field(Constants.environment[11]["item"])
    env13 = make_likert_field(Constants.environment[12]["item"])
    env14 = make_likert_field(Constants.environment[13]["item"])
    env15 = make_likert_field(Constants.environment[14]["item"])
    env16 = make_likert_field(Constants.environment[15]["item"])
    env17 = make_likert_field(Constants.environment[16]["item"])
    env18 = make_likert_field(Constants.environment[17]["item"])
    env19 = make_likert_field(Constants.environment[18]["item"])
    env20 = make_likert_field(Constants.environment[19]["item"])
    env21 = make_likert_field(Constants.environment[20]["item"])
    env22 = make_likert_field(Constants.environment[21]["item"])
    env23 = make_likert_field(Constants.environment[22]["item"])
    env24 = make_likert_field(Constants.environment[23]["item"])
    env25 = make_likert_field(Constants.environment[24]["item"])
    env26 = make_likert_field(Constants.environment[25]["item"])
    env27 = make_likert_field(Constants.environment[26]["item"])
    env28 = make_likert_field(Constants.environment[27]["item"])
    env29 = make_likert_field(Constants.environment[28]["item"])

    # for politics items
    pol1 = make_likert_field(Constants.politics[0]["item"])
    pol2 = make_likert_field(Constants.politics[1]["item"])
    pol3 = make_likert_field(Constants.politics[2]["item"])

    # education items
    edu1 = make_likert_field(Constants.education[0]["item"])
    edu2 = make_likert_field(Constants.education[1]["item"])
    edu3 = make_likert_field(Constants.education[2]["item"])
    edu4 = make_likert_field(Constants.education[3]["item"])

    # quality of decisions items
    dec1 = make_likert_field(Constants.decision[0]["item"])
    dec2 = make_likert_field(Constants.decision[1]["item"])
    dec3 = make_likert_field(Constants.decision[2]["item"])
    dec4 = make_likert_field(Constants.decision[3]["item"])
    dec5 = make_likert_field(Constants.decision[4]["item"])
    dec6 = make_likert_field(Constants.decision[5]["item"])
    dec7 = make_likert_field(Constants.decision[6]["item"])
    dec8 = make_likert_field(Constants.decision[7]["item"])
    dec9 = make_likert_field(Constants.decision[8]["item"])

    # societal connectedness items
    soc1 = make_likert_field(Constants.society[0]["item"])
    soc2 = make_likert_field(Constants.society[1]["item"])
    soc3 = make_likert_field(Constants.society[2]["item"])

    # global health items
    hea1 = make_likert_field(Constants.health[0]["item"])
    hea2 = make_likert_field(Constants.health[1]["item"])

    # Free form comments
    comments = models.LongStringField()

