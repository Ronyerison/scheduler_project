from odoo import models, fields, api
from odoo.exceptions import UserError
from ..enums import TipoResPartnerEnum


class WizardGerarOS(models.TransientModel):
    _name = "wizard.gerar.os"
    _description = "Wizard para Gerar Ordem de Serviço"

    agendamento_id = fields.Many2one(
        "scheduler_core.agendamento", string="Agendamento", required=True
    )
    cliente_id = fields.Many2one(related="agendamento_id.cliente_id", readonly=True)
    recurso_id = fields.Many2one(related="agendamento_id.recurso_id", readonly=True)
    responsavel_execucao_id = fields.Many2one(
        "res.partner", string="Responsável pela Execução", required=True,
        default=lambda self: self.agendamento_id.responsavel_id,
        domain=[('tipo', '=', TipoResPartnerEnum.RESPONSAVEL_RECURSO.value)]
    )
    data_inicio = fields.Datetime(string="Data de Início", default=fields.Datetime.now, required=True)
    descricao_execucao = fields.Text(string="Descrição da Execução")
    materiais_utilizados = fields.Text(string="Materiais Utilizados")
    procedimento_ids = fields.Many2many(
        "scheduler_core.procedimento",
        string="Procedimentos",
    )
    valor_total = fields.Float(string='Valor Total', compute='_compute_valor_total')
    valor_pago = fields.Float(string='Valor Pago', tracking=True)
    valor_desconto = fields.Float(string='Desconto', tracking=True)
    valor_final = fields.Float(string='Valor Final', tracking=True, compute='_compute_valor_final')

    @api.model
    def default_get(self, fields_list):
        """Preencher procedimentos automaticamente com os do agendamento"""
        res = super().default_get(fields_list)
        agendamento_id = self.env.context.get("default_agendamento_id")
        if agendamento_id:
            agendamento = self.env["scheduler_core.agendamento"].browse(agendamento_id)
            res["agendamento_id"] = agendamento.id
            res["responsavel_execucao_id"] = agendamento.responsavel_id.id
            res["procedimento_ids"] = [(6, 0, agendamento.procedimento_ids.ids)]
        return res

    def action_confirmar_os(self):
        self.ensure_one()
        agendamento = self.agendamento_id
        if agendamento.status != "CONFIRMADO":
            raise UserError("O agendamento deve estar CONFIRMADO antes de gerar a OS.")

        os = self.env["scheduler_core.ordem_servico"].create({
            "agendamento_id": agendamento.id,
            "cliente_id": agendamento.cliente_id.id,
            "recurso_id": agendamento.recurso_id.id,
            "responsavel_execucao_id": self.responsavel_execucao_id.id,
            "data_inicio": self.data_inicio,
            "procedimento_ids": [(6, 0, self.procedimento_ids.ids)],
            "descricao_execucao": self.descricao_execucao,
            "materiais_utilizados": self.materiais_utilizados,
            "status": "EM_EXECUCAO",
        })

        agendamento.status = "EM_ANDAMENTO"
        return {
            "type": "ir.actions.act_window",
            "res_model": "scheduler_core.ordem_servico",
            "view_mode": "form",
            "res_id": os.id,
            "target": "current",
        }

    @api.depends('procedimento_ids')
    def _compute_valor_total(self):
        for record in self:
            record.valor_total = sum(record.procedimento_ids.mapped('valor')) if record.procedimento_ids else 0.0

    @api.depends('valor_pago', 'valor_total')
    def _compute_valor_final(self):
        for record in self:
            record.valor_final = record.valor_pago + (record.valor_desconto or 0.0)