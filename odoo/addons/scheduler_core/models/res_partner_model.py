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
    is_cliente_ctx = fields.Boolean(compute='_compute_ctx_flags')
    is_responsavel_ctx = fields.Boolean(compute='_compute_ctx_flags')

    @api.model
    def default_get(self, fields_list):
        logger.info("Default values for fields_list: %s", fields_list)
        res = super().default_get(fields_list)
        ctx_tipo = self.env.context.get('default_tipo')
        # só aplica se a chave existir no selection
        selection_keys = dict(self._fields['tipo']._description_selection(self.env))
        if ctx_tipo and ctx_tipo in selection_keys and 'tipo' in fields_list:
            res['tipo'] = ctx_tipo
        return res

    @api.depends('tipo')
    def _compute_tipo_flags(self):
        for rec in self:
            rec.is_cliente_ctx = (rec.tipo == 'CLIENTE')
            rec.is_responsavel_ctx = (rec.tipo == 'RESPONSAVEL')