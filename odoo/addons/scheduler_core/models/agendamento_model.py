from odoo import _, fields, models, api
from ..enums import TipoResPartnerEnum, SituacaoAgendamentoEnum
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError



class Agendamento(models.Model):
    _name = 'scheduler_core.agendamento'
    _description = 'Model para registros dos agendamentos de serviços'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'cliente_id'

    data_hora_agendamento = fields.Datetime(string='Data de Agendamento', required=True, tracking=True)
    data_hora_fim = fields.Datetime(string='Data/Hora término do Agendamento', tracking=True)
    recurso_id = fields.Many2one('scheduler_core.recurso', string='Recurso', required=True, tracking=True, group_expand='_read_group_recurso_id')
    responsavel_id = fields.Many2one('res.partner', string='Responsavel', tracking=True, related='recurso_id.responsavel_id', store=True)
    cliente_id = fields.Many2one('res.partner', string='Cliente', tracking=True, required=True, domain=[('tipo', '=', TipoResPartnerEnum.CLIENTE.value)])
    procedimento_ids = fields.Many2many('scheduler_core.procedimento', 'agendamento_procedimento_rel', 'agendamento_id', 'procedimento_id', string='Procedimentos', tracking=True)
    valor_total = fields.Float(string='Valor Total', compute='_compute_valor_total', tracking=True, store=True)
    status = fields.Selection([(item.value, item.display_name) for item in SituacaoAgendamentoEnum], _("Status"), tracking=True, default=SituacaoAgendamentoEnum.AGENDADO.value)
    is_recurring = fields.Boolean(string="Recorrente")
    descricao_procedimentos = fields.Char(string="Descrição de Serviços", tracking=True)
    recurrence_unit = fields.Selection(
        [('day', 'Diário'),
         ('week', 'Semanal'),
         ('month', 'Mensal')],
        string="Repetir a cada",
        default='week'
    )
    recurrence_interval = fields.Integer(
        string="Intervalo",
        default=1,
        help="Ex: 1 = toda semana, 2 = a cada 2 semanas"
    )
    recurrence_count = fields.Integer(
        string="Número de ocorrências",
        default=5
    )
    ordem_servico_ids = fields.One2many("scheduler_core.ordem_servico", "agendamento_id", string="Ordens de Serviço")

    @api.onchange('data_hora_agendamento', 'procedimento_ids')
    def _onchange_datas(self):
        for record in self:
            if record.data_hora_agendamento:
                if record.procedimento_ids:
                    duracao_total = sum(record.procedimento_ids.mapped('duracao_minutos'))
                    record.data_hora_fim = record.data_hora_agendamento + timedelta(minutes=duracao_total)
                else:
                    record.data_hora_fim = record.data_hora_agendamento + timedelta(hours=1)

    @api.constrains('data_hora_agendamento', 'data_hora_fim')
    def _check_datas_agendamento(self):
        for record in self:
            if record.data_hora_agendamento and record.data_hora_fim:
                if record.data_hora_fim <= record.data_hora_agendamento:
                    raise ValidationError(
                        _("A data/hora de término deve ser maior que a data/hora de início do agendamento.")
                    )

    @api.depends('procedimento_ids')
    def _compute_valor_total(self):
        for record in self:
            record.valor_total = sum(record.procedimento_ids.mapped('valor')) if record.procedimento_ids else 0.0

    @api.model
    def _read_group_recurso_id(self, stages, domain, order):
        """Garante que todas as estações apareçam no Kanban, mesmo sem registros."""
        return self.env['scheduler_core.recurso'].search([])

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.is_recurring and record.recurrence_count > 1:
                # calcula duração do agendamento base
                duration = False
                if record.data_hora_agendamento and record.data_hora_fim:
                    duration = record.data_hora_fim - record.data_hora_agendamento

                for i in range(1, record.recurrence_count):
                    if record.recurrence_unit == 'day':
                        new_date = record.data_hora_agendamento + relativedelta(days=i * record.recurrence_interval)
                    elif record.recurrence_unit == 'week':
                        new_date = record.data_hora_agendamento + relativedelta(weeks=i * record.recurrence_interval)
                    elif record.recurrence_unit == 'month':
                        new_date = record.data_hora_agendamento + relativedelta(months=i * record.recurrence_interval)
                    else:
                        continue

                    # se houver duração definida, soma ao término
                    new_date_end = new_date + duration if duration else False

                    record.copy({
                        'data_hora_agendamento': new_date,
                        'data_hora_fim': new_date_end,
                        'is_recurring': False,  # instâncias não ficam recorrentes
                    })
        return records

    @api.onchange('procedimento_ids')
    def _onchange_procedimento_ids(self):
        for record in self:
            if record.procedimento_ids:
                descricoes = ", ".join(record.procedimento_ids.mapped('name'))
                record.descricao_procedimentos = descricoes

    def action_confirmar(self):
        for rec in self:
            rec.status = "CONFIRMADO"

    def action_gerar_os(self):
        self.ensure_one()
        if self.status != "CONFIRMADO":
            raise UserError("O agendamento deve estar CONFIRMADO antes de gerar a OS.")

        return {
            "type": "ir.actions.act_window",
            "res_model": "wizard.gerar.os",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_agendamento_id": self.id,
            },
        }