from odoo import _, models, fields, api
from ..enums import TipoResPartnerEnum


class RecursoModel(models.Model):
    _name = 'scheduler_core.recurso'
    _description = 'Recurso utilizado no agendamento do serviço'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nome', required=True)
    active = fields.Boolean(string='Ativo', default=True)
    configuracao_funcionamento_id = fields.Many2one('scheduler_core.configuracao_funcionamento', "Configuração Funcionamento", required=False)
    responsavel_id = fields.Many2one('res.partner', string='Responsavel', required=False, domain=[('tipo', '=', TipoResPartnerEnum.RESPONSAVEL_RECURSO.value)])
