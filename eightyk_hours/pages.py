from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

from django.shortcuts import render


class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1


class Evaluation(Page):
    form_model = 'player'
    form_fields = ['env{}'.format(i) for i in range(1, 30)] + \
                  ['pol{}'.format(i) for i in range(1, 4)] + \
                  ['edu{}'.format(i) for i in range(1, 5)] + \
                  ['dec{}'.format(i) for i in range(1, 10)] + \
                  ['soc{}'.format(i) for i in range(1, 4)] + \
                  ['hea{}'.format(i) for i in range(1, 3)]


class Comments(Page):
    form_model = 'player'
    form_fields = ['comments']

    def is_displayed(self):
        return self.round_number == 5


class Danke(Page):
    def is_displayed(self):
        return self.round_number == 5


page_sequence = [Welcome, Evaluation, Comments, Danke]
