from odoo import _, fields, models, api
from ..enums import TipoResPartnerEnum
from pypdf import PdfWriter, PdfReader
import base64
from io import BytesIO


class OrdemServico(models.Model):
    _name = "scheduler_core.ordem_servico"
    _description = "Ordem de Serviço"

    name = fields.Char(string="Número OS", required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('ordem.servico'))

    agendamento_id = fields.Many2one("scheduler_core.agendamento", string="Agendamento", required=True,
                                     ondelete="cascade")
    cliente_id = fields.Many2one(related="agendamento_id.cliente_id", store=True, readonly=True)
    recurso_id = fields.Many2one(related="agendamento_id.recurso_id", store=True, readonly=True)

    data_inicio = fields.Datetime(string="Início Execução")
    data_fim = fields.Datetime(string="Fim Execução")

    responsavel_execucao_id = fields.Many2one("res.partner", string="Responsável Execução", domain=[('tipo', '=', TipoResPartnerEnum.RESPONSAVEL_RECURSO.value)])

    descricao_execucao = fields.Text(string="Descrição da Execução")
    material_ids = fields.One2many(
        "scheduler_core.ordem_servico_material",
        "ordem_servico_id",
        string="Materiais Utilizados"
    )

    status = fields.Selection([
        ("PENDENTE", "Pendente"),
        ("EM_EXECUCAO", "Em Execução"),
        ("FINALIZADA", "Finalizada"),
        ("CANCELADA", "Cancelada"),
    ], string="Status", default="PENDENTE")
    procedimento_ids = fields.Many2many(
        "scheduler_core.procedimento",
        "ordem_servico_procedimento_rel",  # nome da tabela relacional
        "ordem_servico_id",
        "procedimento_id",
        string="Procedimentos",
    )
    valor_total = fields.Float(string='Valor Total', tracking=True, compute="_compute_valor_total", store=True)
    valor_pago = fields.Float(string='Valor Pago', tracking=True)
    valor_desconto = fields.Float(string='Desconto', tracking=True)
    company_id = fields.Many2one(
        'res.company',
        string="Empresa",
        required=True,
        default=lambda self: self.env.company
    )

    @api.model
    def create(self, vals):
        record = super().create(vals)
        # Atualiza o agendamento para "EM_ANDAMENTO"
        if record.agendamento_id:
            record.agendamento_id.status = "EM_ANDAMENTO"
        return record

    def action_finalizar(self):
        for rec in self:
            rec.status = "FINALIZADA"
            rec.data_fim = fields.Datetime.now()
            # Atualiza o agendamento para concluído
            rec.agendamento_id.status = "CONCLUIDO"

    @api.depends('procedimento_ids', 'material_ids')
    def _compute_valor_total(self):
        for record in self:
            valor_total_procedimentos = sum(record.procedimento_ids.mapped('valor')) if record.procedimento_ids else 0.0
            valor_total_materiais = sum(record.material_ids.mapped('valor_total')) if record.material_ids else 0.0
            record.valor_total = valor_total_procedimentos + valor_total_materiais

    def action_print_os(self):
        """Imprimir Ordem de Serviço / Orçamento"""
        return self.env.ref("scheduler_core.ordem_servico_report").report_action(self)

    def action_gerar_pdf(self):

        merged_pdf_b64 = self.gerar_pdf()

        if not merged_pdf_b64:
            raise ValidationError("O documento NÃO foi gerado. Verifique se os dados foram processados")

        attachment = self.env['ir.attachment'].create([{
            'name': str(self.name) + '.pdf',
            'datas': merged_pdf_b64,
            'mimetype': 'application/pdf',
            'res_model': self._name,
            'res_id': self.id,
        }])

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def gerar_pdf(self):
        pdf_writer = PdfWriter()
        pdf_content, __ = self.env['ir.actions.report']._render_qweb_pdf('scheduler_core.ordem_servico_report', self.id)
        pdf_stream = BytesIO(pdf_content)
        pdf_reader = PdfReader(pdf_stream)

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        merged_pdf_stream = BytesIO()
        pdf_writer.write(merged_pdf_stream)
        pdf_writer.close()

        return base64.b64encode(merged_pdf_stream.getvalue())
