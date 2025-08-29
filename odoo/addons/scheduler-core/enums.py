import enum
from odoo import _


@enum.unique
class SituacaoEstacaoEnum(enum.Enum):
    DISPONIVEL = 'DISPONIVEL'
    OCUPADA = 'OCUPADA'

    def __init__(self, *args):
        self.display_name = {
            'DISPONIVEL': _('Disponível'),
            'OCUPADA': _('Ocupada'),
        }[self.value]
