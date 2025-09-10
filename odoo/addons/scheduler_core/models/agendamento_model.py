from odoo import _, fields, models, api
from ..enums import TipoResPartnerEnum


class Agendamento(models.Model):
    _name = 'scheduler_core.agendamento'
    _description = 'Model para registros dos agendamentos de serviços'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'cliente_id'

    data_agendamento = fields.Datetime(string='Data de Agendamento', required=True, tracking=True)
    estacao_id = fields.Many2one('scheduler_core.estacao', string='Estação', required=True, tracking=True, group_expand='_read_group_estacao_id')
    responsavel_id = fields.Many2one('res.partner', string='Responsavel', tracking=True, related='estacao_id.responsavel_id', store=True)
    cliente_id = fields.Many2one('res.partner', string='Cliente', tracking=True, required=True, domain=[('tipo', '=', TipoResPartnerEnum.CLIENTE.value)])
    procedimento_ids = fields.Many2many('scheduler_core.procedimento', 'agendamento_procedimento_rel', 'agendamento_id', 'procedimento_id', string='Procedimentos', tracking=True)
    valor_total = fields.Float(string='Valor Total', compute='_compute_valor_total', tracking=True, store=True)
    valor_pago = fields.Float(string='Valor Pago', tracking=True)
    valor_desconto = fields.Float(string='Desconto', tracking=True, compute='_compute_valor_desconto', store=True, readonly=True)

    @api.depends('procedimento_ids')
    def _compute_valor_total(self):
        for record in self:
            record.valor_total = sum(record.procedimento_ids.mapped('valor')) if record.procedimento_ids else 0.0

    @api.depends('valor_pago', 'valor_total')
    def _compute_valor_desconto(self):
        for record in self:
            record.valor_desconto = record.valor_total - (record.valor_pago or 0.0)

    @api.model
    def _read_group_estacao_id(self, stages, domain, order):
        """Garante que todas as estações apareçam no Kanban, mesmo sem registros."""
        return self.env['scheduler_core.estacao'].search([])
