from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):
    def vars_for_template(self):
        participant = self.participant

        ## if self.participant.timeout = true: final_payoff = 0, else is participant.payoff
        final_payoff = self.participant.payoff
        final_payoff_plus_part_fee = self.participant.payoff_plus_participation_fee()

        if self.participant.vars['timeout_counter'] == 2:
            timeout = True
        else:
            timeout = False
        return {'timeout': timeout, 'final_payoff_display': final_payoff, 'final_payoff_plus_part_fee_display': final_payoff_plus_part_fee}
        # dict(redemption_code=participant.label or participant.code)


page_sequence = [PaymentInfo]
