from odoo import _, fields, models, api


class Procedimento(models.Model):
    _name = 'scheduler_core.procedimento'
    _description = 'Model de Procedimentos ou Serviços que são disponibilizados pelo estabelecimento'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(_('Nome'), required=True)
    valor = fields.Float(string='Valor', required=True, currency_field="moeda_id")
