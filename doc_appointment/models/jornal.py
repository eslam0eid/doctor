from odoo import fields, models

class JournalCancelled(models.Model):
    _inherit = 'account.move'
    
    def cancelled(self):
        print("#############################################################################")
        for rec in self:  
            line1 = rec.line_ids[0]
            line2 = rec.line_ids[1]
            # line3 = rec.line_ids[2]
            
            
            rec.write({
                'line_ids': [
                    (1, line1.id, {'credit': -line1.credit, 'debit': -line1.debit, 'amount_currency': -line1.amount_currency}),
                    (1, line2.id, {'credit': -line2.credit, 'debit': -line2.debit, 'amount_currency': -line2.amount_currency}),
                    # (1, line3.id, {'credit': -line3.credit, 'debit': -line3.debit, 'amount_currency': -line3.amount_currency}),
                    
                ]
            })

        return True
    def cancelled_tax(self):
        print("#############################################################################")
        for rec in self:  
            line1 = rec.line_ids[0]
            line2 = rec.line_ids[1]
            line3 = rec.line_ids[2]
            
            
            rec.write({
                'line_ids': [
                    (1, line1.id, {'credit': -line1.credit, 'debit': -line1.debit, 'amount_currency': -line1.amount_currency}),
                    (1, line2.id, {'credit': -line2.credit, 'debit': -line2.debit, 'amount_currency': -line2.amount_currency}),
                    (1, line3.id, {'credit': -line3.credit, 'debit': -line3.debit, 'amount_currency': -line3.amount_currency}),
                    
                ]
            })

        return True

