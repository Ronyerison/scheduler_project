from odoo import _, fields, models, api


class Procedimento(models.Model):
    _name = 'scheduler_core.procedimento'
    _description = 'Model de Procedimentos ou Serviços que são disponibilizados pelo estabelecimento'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(_('Nome'), required=True)
    valor = fields.Monetary(string='Valor', required=True, currency_field="moeda_id")
    moeda_id = fields.Many2one(
        "res.currency",
        string="Moeda",
        default=lambda self: self.env.ref("base.BRL"),
    )
