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

@enum.unique
class TipoResPartnerEnum(enum.Enum):
    RESPONSAVEL_ESTACAO = 'RESPONSAVEL_ESTACAO'
    CLIENTE = 'CLIENTE'

    def __init__(self, *args):
        self.display_name = {
            'RESPONSAVEL_ESTACAO': _('Responsável Estação'),
            'CLIENTE': _('Cliente'),
        }[self.value]
