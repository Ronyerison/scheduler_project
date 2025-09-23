/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class SchedulerDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            company: {
                name: "Carregando...",
                cnpj: "",
                logo: null
            },
            menus: [],
            loading: true
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        try {
            const data = await this.orm.call(
                "scheduler_core.dashboard",
                "get_dashboard_data",
                []
            );

            this.state.company = data.company || this.state.company;
            this.state.menus = data.menus || [];
            this.state.loading = false;

            console.log("Dados carregados:", data);
        } catch (error) {
            console.error("Erro ao carregar dados do dashboard:", error);

            // Dados fallback em caso de erro
            this.state.company = {
                name: "Minha Empresa",
                cnpj: "",
                logo: null
            };
            this.state.menus = [];
            this.state.loading = false;
        }
    }

    async onMenuClick(menu) {
        if (menu.action) {
            try {
                await this.action.doAction(menu.action);
            } catch (error) {
                console.error("Erro ao executar ação:", error);
            }
        } else {
            console.log("Menu sem ação definida:", menu.name);
        }
    }

    getCompanyLogoUrl() {
        if (this.state.company.logo) {
            return `data:image/png;base64,${this.state.company.logo}`;
        }
        return '/web/static/img/placeholder.png';
    }
}

SchedulerDashboard.template = "scheduler_core.dashboard_template";

// Registrar o componente
registry.category("actions").add("scheduler_core.dashboard", SchedulerDashboard);

console.log("SchedulerDashboard registrado:", SchedulerDashboard);