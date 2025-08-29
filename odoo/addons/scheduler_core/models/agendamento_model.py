from odoo import _, fields, models, api


class Agendamento(models.Model):
    _name = 'scheduler_core.agendamento'
    _description = 'Model para registros dos agendamentos de serviços'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    data_agendamento = fields.Datetime(string='Data de Agendamento', required=True, tracking=True)
    estacao_id = fields.Many2one('scheduler_core.estacao', string='Estação', required=True, tracking=True)
    responsavel_id = fields.Many2one('res.partner', string='Responsavel', tracking=True, related='estacao_id.responsavel_id', store=True)
    cliente_id = fields.Many2one('res.partner', string='Cliente', tracking=True, required=True)
    procedimento_ids = fields.Many2many('scheduler_core.procedimento', 'agendamento_procedimento_rel', 'agendamento_id', 'procedimento_id', string='Procedimentos', tracking=True)
    valor_total = fields.Monetary(string='Valor Total', compute='_compute_valor_total', tracking=True, store=True, required=True, readonly=False)
    valor_pago = fields.Monetary(string='Valor Pago', tracking=True)
    valor_desconto = fields.Monetary(string='Desconto', tracking=True, compute='_compute_valor_desconto', store=True, readonly=True)

    @api.depends('procedimento_ids')
    def _compute_valor_total(self):
        for record in self:
            if record.procedimento_ids:
                record.valor_total = sum(procedimento.valor for procedimento in record.procedimento_ids)

    @api.depends('valor_pago')
    def _compute_valor_desconto(self):
        for record in self:
            record.valor_desconto = record.valor_total - record.valor_pago
