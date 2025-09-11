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
    RESPONSAVEL_RECURSO = 'RESPONSAVEL_RECURSO'
    CLIENTE = 'CLIENTE'

    def __init__(self, *args):
        self.display_name = {
            'RESPONSAVEL_RECURSO': _('Responsável Recurso'),
            'CLIENTE': _('Cliente'),
        }[self.value]

@enum.unique
class SituacaoAgendamentoEnum(enum.Enum):
    AGENDADO = 'AGENDADO'
    CONFIRMADO = 'CONFIRMADO'
    EM_ANDAMENTO = 'EM_ANDAMENTO'
    CONCLUIDO = 'CONCLUIDO'
    CANCELADO = 'CANCELADO'

    def __init__(self, *args):
        self.display_name = {
            'AGENDADO': _('Agendado'),
            'CONFIRMADO': _('Confirmado'),
            'EM_ANDAMENTO': _('Em Andamento'),
            'CONCLUIDO': _('Concluído'),
            'CANCELADO': _('Cancelado')
        }[self.value]