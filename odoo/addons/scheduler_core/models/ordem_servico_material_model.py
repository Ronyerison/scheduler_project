from odoo import fields, models, api


class OrdemServicoMaterial(models.Model):
    _name = "scheduler_core.ordem_servico_material"
    _description = "Materiais Utilizados na OS"

    ordem_servico_id = fields.Many2one("scheduler_core.ordem_servico", string="Ordem de Serviço", required=True, ondelete="cascade")
    material_id = fields.Many2one("scheduler_core.material", string="Material", required=True)
    unidade_id = fields.Many2one(related="material_id.unidade_id", string="Unidade", store=True, readonly=True)
    valor_unitario = fields.Float(related="material_id.valor_unitario", string="Valor Unitário", store=True, readonly=True)

    quantidade = fields.Float("Quantidade", required=True, default=1.0)
    valor_total = fields.Float("Valor Total", compute="_compute_valor_total", store=True)

    @api.depends("quantidade", "valor_unitario")
    def _compute_valor_total(self):
        for rec in self:
            rec.valor_total = rec.quantidade * rec.valor_unitario
