from odoo import _, fields, models, api
from ..enums import TipoResPartnerEnum
import logging

logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    tipo = fields.Selection([(item.value, item.display_name) for item in TipoResPartnerEnum], _("Tipo"), tracking=True)

    l10n_br_legal_name = fields.Char(string="Razão Social",tracking=True)
    l10n_br_cnpj_cpf = fields.Char(string="CNPJ/CPF", tracking=True)
    l10n_br_number = fields.Char(string="Número")  # Número da residência/empresa
    l10n_br_district = fields.Char(string="Bairro")  # Bairro
    street = fields.Char(string="Endereço")
    street2 = fields.Char(string="Complemento")
    city_id = fields.Many2one('res.city', string="Cidade")
    state_id = fields.Many2one('res.country.state', string="Estado")
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.br'))
    zip = fields.Char(string="CEP")
    whatsapp = fields.Char(string="WhatsApp")

    agendamento_ids = fields.One2many('scheduler_core.agendamento', 'cliente_id', string="Histórico de Agendamentos")

