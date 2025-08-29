from odoo import _, models, fields, api
from ..enums import SituacaoEstacaoEnum, TipoResPartnerEnum


class EstacaoModel(models.Model):
    _name = 'scheduler_core.estacao'
    _description = 'Estação principal alvo do agendamento'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nome', required=True)
    active = fields.Boolean(string='Ativo', default=True)
    situacao = fields.Selection([(item.value, item.display_name) for item in SituacaoEstacaoEnum], _("Situação"), tracking=True)
    configuracao_funcionamento_id = fields.Many2one('scheduler_core.configuracao_funcionamento', "Configuração Funcionamento", required=True)
    responsavel_id = fields.Many2one('res.partner', string='Responsavel', required=False, domain=[('tipo', '=', TipoResPartnerEnum.RESPONSAVEL_ESTACAO)])
