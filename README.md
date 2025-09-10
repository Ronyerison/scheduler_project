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