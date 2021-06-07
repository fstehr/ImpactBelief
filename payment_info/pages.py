from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Terminated(Page):
    form_model = 'player'
    form_fields = ['finishing_time']

    def is_displayed(self):
        return self.participant.vars['trial_timeout_counter'] == 3 or self.participant.vars['timeout_counter'] == 2 \
               or self.participant.vars['attention_check_failed'] == True

    def vars_for_template(self):
        participant = self.participant
        if participant.vars['trial_timeout_counter'] == 3 or participant.vars['timeout_counter'] == 2:
            timeout = True
            attention_fail = False
        elif participant.vars['attention_check_failed'] == True:
            timeout = False
            attention_fail = True
        return {'timeout': timeout, 'attention_check_failed': attention_fail}
        # dict(redemption_code=participant.label or participant.code)


class PaymentInfo(Page):
    form_model = 'player'
    form_fields = ['finishing_time']

    def vars_for_template(self):
        participant = self.participant
        timeout_in_payment_round = participant.vars['timeout_in_payment_round']

        final_payoff = participant.payoff
        final_payoff_plus_part_fee = participant.payoff_plus_participation_fee()

        return {'timeout_in_payment_round': timeout_in_payment_round,
                'final_payoff_display': final_payoff,
                'final_payoff_plus_part_fee_display': final_payoff_plus_part_fee}
        # dict(redemption_code=participant.label or participant.code)


page_sequence = [Terminated, PaymentInfo]
