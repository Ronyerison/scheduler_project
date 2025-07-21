from odoo import models, fields

class ArenaExample(models.Model):
    _name = 'arena.example'
    _description = 'Exemplo do Módulo Arena'

    name = fields.Char(string='Nome', required=True)
    active = fields.Boolean(string='Ativo', default=True)
