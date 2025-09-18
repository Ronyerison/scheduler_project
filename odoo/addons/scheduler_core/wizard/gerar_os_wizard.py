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
    material_ids = fields.One2many(
        "wizard.gerar.os.material",
        "wizard_id",
        string="Materiais Utilizados"
    )
    procedimento_ids = fields.Many2many(
        "scheduler_core.procedimento",
        string="Procedimentos",
    )
    valor_total = fields.Float(string='Valor Total', compute="_compute_valor_total")
    valor_pago = fields.Float(string='Valor Pago')
    valor_desconto = fields.Float(string='Desconto')

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
            "status": "EM_EXECUCAO",
            "material_ids": [
                (0, 0, {
                    "material_id": mat.material_id.id,
                    "quantidade": mat.quantidade,
                    "valor_unitario": mat.valor_unitario or (mat.material_id.valor_unitario if mat.material_id else 0.0),
                }) for mat in self.material_ids
            ]
        })

        agendamento.status = "EM_ANDAMENTO"
        return {
            "type": "ir.actions.act_window",
            "res_model": "scheduler_core.ordem_servico",
            "view_mode": "form",
            "res_id": os.id,
            "target": "current",
        }

    @api.depends(
        'procedimento_ids', 'procedimento_ids.valor',
        'material_ids.quantidade', 'material_ids.valor_unitario', 'material_ids.material_id'
    )
    def _compute_valor_total(self):
        for record in self:
            # soma procedimentos
            valor_total_procedimentos = 0.0
            if record.procedimento_ids:
                for p in record.procedimento_ids:
                    valor_total_procedimentos += float(p.valor or 0.0)

            # soma materiais: quantidade * valor_unitario (fallback para material.valor_unitario)
            valor_total_materiais = 0.0
            for m in record.material_ids:
                unit = m.valor_unitario or (m.material_id.valor_unitario if m.material_id else 0.0)
                valor_total_materiais += float(m.quantidade or 0.0) * float(unit or 0.0)

            record.valor_total = valor_total_procedimentos + valor_total_materiais