### CONFIGURAÇÃO PYCHARM RUN-SERVER AUDITOR ###

```yaml
INTERPRETADOR: Remote Python 3.9.2 Docker Compose (odoo)
SCRIPT: /usr/bin/odoo
SCRIPT PARAMS: --db_user {usuario_db} --db_password {senha_db} --db_host {host_container_db} --db_port 5432 --db-filter ^.*$ --dev qweb,xml
WORKING DIRECTORY: {caminho_ate_workspace}/scheduler_project/odoo/addons/scheduler_core
ENVIRONMENT VARIABLES: PYTHONUNBUFFERED=1
PATH MAPPINGS: {caminho_ate_workspace}/scheduler_project=/mnt/scheduler_project
```
### CONFIGURAÇÃO PYCHARM UPDATE-APPLICATIONS AUDITOR ###

```yaml
INTERPRETADOR: Remote Python 3.9.2 Docker Compose (odoo)
SCRIPT: /usr/bin/odoo
SCRIPT PARAMS: --db_user {usuario_db} --db_password {senha_db} --db_host {host_container_db} --db_port 5432 --dev qweb,xml  --database auditordb -u scheduler_core --stop-after-init
WORKING DIRECTORY: {caminho_ate_workspace}/scheduler_project/odoo/addons/scheduler_core
ENVIRONMENT VARIABLES: PYTHONUNBUFFERED=1
PATH MAPPINGS: {caminho_ate_workspace}/scheduler_project=/mnt/scheduler_project
```


### ESCOPO PLANEJADO ###
### ⚙️ Funcionalidades básicas (MVP) ###
    📅 Agenda/Kanban: visualização por dia, semana, mês e colunas por "unidade/recurso" (ex: sala, equipe, quadra).
    👥 Clientes: cadastro com tipo (pessoa física/jurídica), contatos, histórico de agendamentos.
    📌 Serviços/Procedimentos: cadastro com duração padrão, preço, descrição.
    💰 Valores: cálculo automático do valor total, descontos e status de pagamento.
    ✅ Status do agendamento: agendado, confirmado, em andamento, concluído, cancelado.
    🔄 Recorrência: possibilidade de agendamentos recorrentes (ex: toda segunda às 9h).
    📲 Notificações: e-mail/WhatsApp lembrando clientes e responsáveis.

### 🛠 Funcionalidades avançadas ###
    🔎 Busca de disponibilidade automática: o cliente ou atendente escolhe serviço e sistema sugere horários livres.
    🏷 Pacotes e combos: venda de combos (ex: 10 sessões com desconto).
    ⏱ Tempo de preparação: intervalo entre atendimentos (ex: higienização da sala).
    📍 Locais múltiplos: suporte a mais de uma filial.
    🔑 Controle de acesso: perfil para cliente (autoagendamento), funcionário (ver sua agenda) e admin.
    📊 Relatórios: taxa de ocupação, faturamento por serviço, agendamentos por cliente.
    🧩 Integração com calendário externo: Google Calendar/Outlook.
    💡 Funcionalidades que geram valor no dia a dia
    📸 Check-in/check-out no agendamento (quem atendeu, hora real de início e fim).
    ⏳ Fila de espera: se um cliente cancela, o próximo interessado pode ocupar o horário.
    🔄 Reagendamento rápido: botão para mover o agendamento de horário/unidade sem precisar recriar.
    🖨 Recibo automático: imprimir ou enviar comprovante de agendamento/pagamento.
    💳 Integração com meios de pagamento: Pix, cartão, boleto.
    🧾 Faturamento: integração com vendas/faturas do Odoo (se quiser linkar ao módulo Accounting).

### 🌐 Funcionalidades “wow” (diferenciais) ###
    👨‍💻 Portal do cliente: área onde o cliente agenda, paga e acompanha seus serviços.
    📱 App responsivo ou PWA: acesso rápido no celular.
    🤖 Chatbot de agendamento: integração com WhatsApp/Telegram.
    📡 IoT/Controle físico: abrir portão da arena, liberar sala, etc., com base no agendamento.
    🧠 IA para previsão: prever horários de pico, recomendar serviços ou otimizar agenda.