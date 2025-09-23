from odoo import models, fields, api
import base64


class SchedulerDashboard(models.TransientModel):
    _name = "scheduler_core.dashboard"
    _description = "Dashboard Inicial"

    name = fields.Char(string="Nome da Empresa", readonly=True)
    cnpj = fields.Char(string="CNPJ", readonly=True)
    logo = fields.Binary(string="Logo", readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        company = self.env.company
        res.update({
            "name": company.name,
            "cnpj": company.vat,
            "logo": company.logo,
        })
        return res

    @api.model
    def get_main_menus(self):
        """Retorna os menus de primeiro nível (sem parent) para o dashboard"""
        # Buscar apenas menus principais, excluindo alguns menus do sistema
        menus = self.env["ir.ui.menu"].search([
            ("parent_id", "=", False),
            ("name", "not in", ["Dashboard"])
        ], order="sequence,name")

        return [
            {
                "id": menu.id,
                "name": menu.name,
                "action": menu.action.id if menu.action else None,
                "action_type": menu.action._name if menu.action else None,
                "has_children": bool(self.env["ir.ui.menu"].search_count([("parent_id", "=", menu.id)])),
                "icon": self._get_menu_icon(menu),
                "icon_type": self._get_icon_type(menu.web_icon),
                "web_icon": menu.web_icon,
            }
            for menu in menus
        ]

    def _get_menu_icon(self, menu):
        """Retorna o ícone do menu ou um padrão"""
        if menu.web_icon:
            # Tratar ícones do tipo 'modulo,static/description/icon.png'
            if ',' in menu.web_icon and 'static' in menu.web_icon:
                # Extrair o módulo e caminho
                module_path = menu.web_icon.split(',')
                if len(module_path) == 2:
                    module = module_path[0]
                    path = module_path[1]
                    # Retornar o caminho completo para a imagem
                    return f"/{module}/{path}"

            # Se tem ícone FontAwesome
            elif menu.web_icon.startswith('fa-'):
                return f"fa {menu.web_icon}"

            # Se é um ícone direto (caminho de imagem)
            elif menu.web_icon.startswith('/') or menu.web_icon.startswith('http'):
                return menu.web_icon

            # Outros formatos de ícone
            else:
                return menu.web_icon

        # Ícones padrão baseados no nome do menu
        icon_mapping = {
            'sales': 'fa fa-shopping-cart',
            'purchase': 'fa fa-shopping-bag',
            'inventory': 'fa fa-cubes',
            'accounting': 'fa fa-calculator',
            'invoicing': 'fa fa-file-invoice',
            'hr': 'fa fa-users',
            'project': 'fa fa-tasks',
            'crm': 'fa fa-handshake',
            'manufacturing': 'fa fa-industry',
            'website': 'fa fa-globe',
            'point_of_sale': 'fa fa-cash-register',
            'pos': 'fa fa-cash-register',
            'calendar': 'fa fa-calendar',
            'contacts': 'fa fa-address-book',
            'fleet': 'fa fa-truck',
            'maintenance': 'fa fa-wrench',
            'helpdesk': 'fa fa-life-ring',
            'agendamento': 'fa fa-calendar-check',
            'scheduler': 'fa fa-clock',
            'cadastros': 'fa fa-database',
            'configuracao': 'fa fa-cog',
            'configurações': 'fa fa-cog',
            'apps': 'fa fa-th',
            'aplicativos': 'fa fa-th',
        }

        # Buscar por palavra-chave no nome do menu
        menu_name_lower = menu.name.lower()
        for keyword, icon in icon_mapping.items():
            if keyword in menu_name_lower:
                return icon

        # Ícone padrão
        return 'fa fa-folder'

    def _get_icon_type(self, web_icon):
        """Determina o tipo do ícone para renderização no frontend"""
        if not web_icon:
            return 'fontawesome'

        if ',' in web_icon and 'static' in web_icon:
            return 'image'
        elif web_icon.startswith('fa-') or web_icon.startswith('fa '):
            return 'fontawesome'
        elif web_icon.startswith('/') or web_icon.startswith('http'):
            return 'image'
        else:
            return 'fontawesome'

    @api.model
    def get_dashboard_data(self):
        """Retorna logo, nome, CNPJ e menus"""
        company = self.env.company
        menus = self.get_main_menus()

        # Converter logo para base64 se existir
        logo_b64 = None
        if company.logo:
            try:
                logo_b64 = base64.b64encode(base64.b64decode(company.logo)).decode('utf-8')
            except:
                logo_b64 = company.logo

        return {
            "company": {
                "name": company.name or "Minha Empresa",
                "cnpj": company.vat or "",
                "logo": logo_b64,
            },
            "menus": menus,
        }

    @api.model
    def get_recent_activities(self):
        """Retorna atividades recentes do usuário"""
        # Buscar últimas ordens de serviço criadas (se o modelo existir)
        recent_data = {}

        try:
            if 'ordem.servico' in self.env:
                recent_os = self.env['ordem.servico'].search([], limit=5, order='create_date desc')
                recent_data['ordens_servico'] = [
                    {
                        'id': os.id,
                        'name': os.name if hasattr(os, 'name') else f'OS #{os.id}',
                        'create_date': os.create_date.strftime('%d/%m/%Y %H:%M') if os.create_date else '',
                    }
                    for os in recent_os
                ]
        except:
            pass

        try:
            if 'agendamento' in self.env:
                recent_agendamentos = self.env['agendamento'].search([], limit=5, order='create_date desc')
                recent_data['agendamentos'] = [
                    {
                        'id': ag.id,
                        'name': ag.name if hasattr(ag, 'name') else f'Agendamento #{ag.id}',
                        'create_date': ag.create_date.strftime('%d/%m/%Y %H:%M') if ag.create_date else '',
                    }
                    for ag in recent_agendamentos
                ]
        except:
            pass

        return recent_data