from odoo import _, models, fields
from ..enums import SituacaoEstacaoEnum


class EstacaoModel(models.Model):
    _name = 'scheduler-core.estacao'
    _description = 'Estação principal alvo do agendamento'

    name = fields.Char(string='Nome', required=True)
    active = fields.Boolean(string='Ativo', default=True)
    situacao = fields.Selection([(item.value, item.display_name) for item in SituacaoEstacaoEnum], _("Situação"), tracking=True)
