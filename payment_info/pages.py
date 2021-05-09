from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):
    form_model = 'player'
    form_fields = ['finishing_time']

    def vars_for_template(self):
        participant = self.participant

        final_payoff = participant.payoff
        final_payoff_plus_part_fee = participant.payoff_plus_participation_fee()

        if participant.vars['trial_timeout_counter'] == 3 or participant.vars['timeout_counter'] == 2:
            timeout = True
        else:
            timeout = False
        return {'timeout': timeout, 'final_payoff_display': final_payoff,
                'final_payoff_plus_part_fee_display': final_payoff_plus_part_fee}
        # dict(redemption_code=participant.label or participant.code)


page_sequence = [PaymentInfo]
