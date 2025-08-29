from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from ..enums import SituacaoEstacaoEnum


class ConfiguracaoFuncionamentoModel(models.Model):
    _name = 'scheduler-core.configuracao_funcionamento'
    _description = 'Configuração de Funcionamento das estações'

    name = fields.Char(string='Nome', required=True)
    active = fields.Boolean(string='Ativo', default=True)

    # Dias da semana
    segunda_feira = fields.Boolean(string='Segunda-feira', default=True)
    terca_feira = fields.Boolean(string='Terça-feira', default=True)
    quarta_feira = fields.Boolean(string='Quarta-feira', default=True)
    quinta_feira = fields.Boolean(string='Quinta-feira', default=True)
    sexta_feira = fields.Boolean(string='Sexta-feira', default=True)
    sabado = fields.Boolean(string='Sábado', default=False)
    domingo = fields.Boolean(string='Domingo', default=False)

    # Horários de funcionamento
    horario_inicio = fields.Float(
        string='Horário de Início',
        required=True,
        default=8.0,  # 08:00
        help='Horário de início do funcionamento (formato: 8.5 = 08:30)'
    )
    horario_fim = fields.Float(
        string='Horário de Fim',
        required=True,
        default=18.0,  # 18:00
        help='Horário de fim do funcionamento (formato: 18.5 = 18:30)'
    )

    # Intervalo para almoço (opcional)
    tem_intervalo_almoco = fields.Boolean(string='Tem Intervalo para Almoço', default=False)
    almoco_inicio = fields.Float(
        string='Início do Almoço',
        help='Horário de início do intervalo para almoço'
    )
    almoco_fim = fields.Float(
        string='Fim do Almoço',
        help='Horário de fim do intervalo para almoço'
    )

    # Campos computados para exibição
    horario_inicio_display = fields.Char(
        string='Horário Início',
        compute='_compute_horario_display',
        store=False
    )
    horario_fim_display = fields.Char(
        string='Horário Fim',
        compute='_compute_horario_display',
        store=False
    )
    dias_funcionamento_display = fields.Char(
        string='Dias de Funcionamento',
        compute='_compute_dias_display',
        store=False
    )

    @api.depends('horario_inicio', 'horario_fim')
    def _compute_horario_display(self):
        for record in self:
            record.horario_inicio_display = self._float_to_time_string(record.horario_inicio)
            record.horario_fim_display = self._float_to_time_string(record.horario_fim)

    @api.depends('segunda_feira', 'terca_feira', 'quarta_feira', 'quinta_feira',
                 'sexta_feira', 'sabado', 'domingo')
    def _compute_dias_display(self):
        for record in self:
            dias = []
            if record.segunda_feira:
                dias.append('Seg')
            if record.terca_feira:
                dias.append('Ter')
            if record.quarta_feira:
                dias.append('Qua')
            if record.quinta_feira:
                dias.append('Qui')
            if record.sexta_feira:
                dias.append('Sex')
            if record.sabado:
                dias.append('Sáb')
            if record.domingo:
                dias.append('Dom')

            record.dias_funcionamento_display = ', '.join(dias) if dias else 'Nenhum dia selecionado'

    def _float_to_time_string(self, float_time):
        """Converte float para string de horário (ex: 8.5 -> '08:30')"""
        if not float_time:
            return '00:00'

        hours = int(float_time)
        minutes = int((float_time - hours) * 60)
        return f'{hours:02d}:{minutes:02d}'

    @api.constrains('horario_inicio', 'horario_fim')
    def _check_horarios(self):
        for record in self:
            if record.horario_inicio >= record.horario_fim:
                raise ValidationError(_('O horário de início deve ser menor que o horário de fim.'))

            if record.horario_inicio < 0 or record.horario_inicio >= 24:
                raise ValidationError(_('O horário de início deve estar entre 00:00 e 23:59.'))

            if record.horario_fim < 0 or record.horario_fim > 24:
                raise ValidationError(_('O horário de fim deve estar entre 00:01 e 24:00.'))

    @api.constrains('almoco_inicio', 'almoco_fim', 'tem_intervalo_almoco')
    def _check_intervalo_almoco(self):
        for record in self:
            if record.tem_intervalo_almoco:
                if not record.almoco_inicio or not record.almoco_fim:
                    raise ValidationError(
                        _('Quando há intervalo para almoço, os horários de início e fim devem ser preenchidos.'))

                if record.almoco_inicio >= record.almoco_fim:
                    raise ValidationError(_('O horário de início do almoço deve ser menor que o horário de fim.'))

                if record.almoco_inicio < record.horario_inicio or record.almoco_fim > record.horario_fim:
                    raise ValidationError(_('O intervalo do almoço deve estar dentro do horário de funcionamento.'))

    @api.constrains('segunda_feira', 'terca_feira', 'quarta_feira', 'quinta_feira',
                    'sexta_feira', 'sabado', 'domingo')
    def _check_pelo_menos_um_dia(self):
        for record in self:
            dias_selecionados = [
                record.segunda_feira, record.terca_feira, record.quarta_feira,
                record.quinta_feira, record.sexta_feira, record.sabado, record.domingo
            ]
            if not any(dias_selecionados):
                raise ValidationError(_('Pelo menos um dia da semana deve ser selecionado.'))

    def get_dias_funcionamento_list(self):
        """Retorna uma lista com os números dos dias da semana que funcionam (0=segunda, 6=domingo)"""
        dias = []
        if self.segunda_feira:
            dias.append(0)
        if self.terca_feira:
            dias.append(1)
        if self.quarta_feira:
            dias.append(2)
        if self.quinta_feira:
            dias.append(3)
        if self.sexta_feira:
            dias.append(4)
        if self.sabado:
            dias.append(5)
        if self.domingo:
            dias.append(6)
        return dias

    def is_horario_funcionamento(self, datetime_obj):
        """Verifica se um datetime está dentro do horário de funcionamento"""
        # Verifica se é um dia de funcionamento
        dia_semana = datetime_obj.weekday()  # 0=segunda, 6=domingo
        if dia_semana not in self.get_dias_funcionamento_list():
            return False

        # Converte o horário para float
        hora_float = datetime_obj.hour + datetime_obj.minute / 60.0

        # Verifica se está dentro do horário geral
        if hora_float < self.horario_inicio or hora_float > self.horario_fim:
            return False

        # Verifica se não está no intervalo do almoço
        if self.tem_intervalo_almoco:
            if self.almoco_inicio <= hora_float <= self.almoco_fim:
                return False

        return True
