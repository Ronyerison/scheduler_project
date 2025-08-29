from odoo import _, fields, models, api
from ..enums import TipoResPartnerEnum


class ResPartner(models.Model):
    """
    """
    _name = 'res.partner'
    _inherit = ['res.partner']

    tipo = fields.Selection([(item.value, item.display_name) for item in TipoResPartnerEnum], _("Tipo"), tracking=True)
