#!/bin/bash
set -e

# Substituir variáveis de ambiente no arquivo de configuração
envsubst < /etc/odoo/odoo.conf.template > /etc/odoo/odoo.conf

# Iniciar Odoo
exec odoo -c /etc/odoo/odoo.conf --without-demo=all "$@"
