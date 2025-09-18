from odoo import models, fields, api


class WizardGerarOSMaterial(models.TransientModel):
    _name = "wizard.gerar.os.material"
    _description = "Materiais no Wizard de OS"

    wizard_id = fields.Many2one("wizard.gerar.os", string="Wizard", ondelete="cascade")
    material_id = fields.Many2one("scheduler_core.material", string="Material", required=True)
    quantidade = fields.Float(string="Quantidade", required=True, default=1)
    valor_unitario = fields.Float(string="Valor Unitário", related="material_id.valor_unitario", readonly=True)
    valor_total = fields.Float(string="Valor Total", compute="_compute_valor_total", store=False)

    @api.onchange("material_id")
    def _onchange_material_id(self):
        if self.material_id:
            self.valor_unitario = self.material_id.valor_unitario

    @api.depends("quantidade", "valor_unitario", "material_id")
    def _compute_valor_total(self):
        for rec in self:
            unit = rec.valor_unitario or (rec.material_id.valor_unitario if rec.material_id else 0.0)
            rec.valor_total = float(rec.quantidade or 0.0) * float(unit or 0.0)
