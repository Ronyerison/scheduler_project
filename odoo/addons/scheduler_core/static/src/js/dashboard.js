/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component, onWillStart, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class SchedulerDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.menu = useService("menu");
        this.router = useService("router");

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
        try {
            console.log("Clicou no menu:", menu);

            if (menu.action) {
                // Se tem action, executa diretamente
                console.log("Executando action:", menu.action);
                await this.action.doAction(menu.action);
            } else if (menu.has_children) {
                // Se tem filhos, navega para mostrar os submenus
                console.log("Navegando para menu com submenus:", menu.id);

                // Método 1: Usar o serviço de menu
                try {
                    await this.menu.selectMenu(menu.id);
                } catch (menuError) {
                    console.log("Erro no método 1, tentando método 2");

                    // Método 2: Usar router para navegar
                    try {
                        this.router.pushState({
                            action: null,
                            menu_id: menu.id,
                        });

                        // Força a atualização da interface
                        window.location.reload();
                    } catch (routerError) {
                        console.log("Erro no método 2, tentando método 3");

                        // Método 3: Navegação direta via URL
                        const url = `/web#menu_id=${menu.id}`;
                        window.location.href = url;
                    }
                }
            } else {
                // Menu sem action e sem filhos - pode ser um erro de configuração
                console.warn("Menu sem ação nem filhos:", menu.name);
            }
        } catch (error) {
            console.error("Erro ao navegar para o menu:", error);

            // Fallback final: navegação direta
            try {
                const url = `/web#menu_id=${menu.id}`;
                console.log("Tentativa de fallback para:", url);
                window.location.href = url;
            } catch (fallbackError) {
                console.error("Todos os métodos de navegação falharam:", fallbackError);
            }
        }
    }

    getCompanyLogoUrl() {
        if (this.state.company.logo) {
            return `data:image/png;base64,${this.state.company.logo}`;
        }
        return '/web/static/img/placeholder.png';
    }

    getMenuDescription(menu) {
        if (menu.action) {
            return "Clique para acessar";
        } else if (menu.has_children) {
            return "Ver submenus";
        } else {
            return "Menu de navegação";
        }
    }

    onImageError(event) {
        // Esconde a imagem quebrada e mostra o ícone fallback
        const img = event.target;
        const fallback = img.nextElementSibling;

        if (img && fallback) {
            img.style.display = 'none';
            fallback.style.display = 'inline-block';
        }
    }
}

SchedulerDashboard.template = "scheduler_core.dashboard_template";

// Registrar o componente
registry.category("actions").add("scheduler_core.dashboard", SchedulerDashboard);

console.log("SchedulerDashboard avançado registrado:", SchedulerDashboard);