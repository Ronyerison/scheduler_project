from odoo import _, fields, models, api
from ..enums import TipoResPartnerEnum


class OrdemServico(models.Model):
    _name = "scheduler_core.ordem_servico"
    _description = "Ordem de Serviço"

    name = fields.Char(string="Número OS", required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('ordem.servico'))

    agendamento_id = fields.Many2one("scheduler_core.agendamento", string="Agendamento", required=True,
                                     ondelete="cascade")
    cliente_id = fields.Many2one(related="agendamento_id.cliente_id", store=True, readonly=True)
    recurso_id = fields.Many2one(related="agendamento_id.recurso_id", store=True, readonly=True)

    data_inicio = fields.Datetime(string="Início Execução")
    data_fim = fields.Datetime(string="Fim Execução")

    responsavel_execucao_id = fields.Many2one("res.partner", string="Responsável Execução", domain=[('tipo', '=', TipoResPartnerEnum.RESPONSAVEL_RECURSO.value)])

    descricao_execucao = fields.Text(string="Descrição da Execução")
    material_ids = fields.One2many(
        "scheduler_core.ordem_servico_material",
        "ordem_servico_id",
        string="Materiais Utilizados"
    )

    status = fields.Selection([
        ("PENDENTE", "Pendente"),
        ("EM_EXECUCAO", "Em Execução"),
        ("FINALIZADA", "Finalizada"),
        ("CANCELADA", "Cancelada"),
    ], string="Status", default="PENDENTE")
    procedimento_ids = fields.Many2many(
        "scheduler_core.procedimento",
        "ordem_servico_procedimento_rel",  # nome da tabela relacional
        "ordem_servico_id",
        "procedimento_id",
        string="Procedimentos",
    )
    valor_total = fields.Float(string='Valor Total', compute='_compute_valor_total', tracking=True, store=True)
    valor_pago = fields.Float(string='Valor Pago', tracking=True)
    valor_desconto = fields.Float(string='Desconto', tracking=True)
    valor_final = fields.Float(string='Valor Final', tracking=True, compute='_compute_valor_final', store=True,
                               readonly=True)

    @api.model
    def create(self, vals):
        record = super().create(vals)
        # Atualiza o agendamento para "EM_ANDAMENTO"
        if record.agendamento_id:
            record.agendamento_id.status = "EM_ANDAMENTO"
        return record

    def action_finalizar(self):
        for rec in self:
            rec.status = "FINALIZADA"
            rec.data_fim = fields.Datetime.now()
            # Atualiza o agendamento para concluído
            rec.agendamento_id.status = "CONCLUIDO"

    @api.depends('valor_pago', 'valor_total')
    def _compute_valor_final(self):
        for record in self:
            record.valor_final = record.valor_pago + (record.valor_desconto or 0.0)

    @api.depends('procedimento_ids')
    def _compute_valor_total(self):
        for record in self:
            record.valor_total = sum(record.procedimento_ids.mapped('valor')) if record.procedimento_ids else 0.0
