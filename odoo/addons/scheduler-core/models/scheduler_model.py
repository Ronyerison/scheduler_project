from odoo import models, fields

class ArenaExample(models.Model):
    _name = 'scheduler.example'
    _description = 'Exemplo do Módulo Scheduler'

    name = fields.Char(string='Nome', required=True)
    active = fields.Boolean(string='Ativo', default=True)
