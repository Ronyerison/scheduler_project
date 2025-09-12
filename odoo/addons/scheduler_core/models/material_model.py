from odoo import fields, models, api


class Material(models.Model):
    _name = "scheduler_core.material"
    _description = "Material"

    name = fields.Char("Descrição do Material", required=True)
    unidade_id = fields.Many2one("uom.uom", string="Unidade de Medida", required=True)
    valor_unitario = fields.Float("Valor Unitário", required=True)
    observacao = fields.Text("Observação")