#!/bin/bash
set -e

# Exibir variáveis de ambiente para debug
echo "===== Variáveis de ambiente ====="
echo "PGHOST=${PGHOST}"
echo "PGPORT=${PGPORT}"
echo "ODOO_DB_NAME=${ODOO_DB_NAME}"
echo "ODOO_DB_USER=${ODOO_DB_USER}"
echo "ODOO_DB_PASSWORD=${ODOO_DB_PASSWORD}"
echo "ADMIN_PASSWORD=${ADMIN_PASSWORD}"
echo "================================="

# Aguardar banco estar disponível
echo "Aguardando PostgreSQL..."
until pg_isready -h "${PGHOST}" -p "${PGPORT}" -U "${ODOO_DB_USER}" >/dev/null 2>&1; do
    sleep 2
done
echo "PostgreSQL disponível!"

# Substituir variáveis de ambiente no arquivo de configuração
envsubst < /etc/odoo/odoo.conf.template > /etc/odoo/odoo.conf

# Inicializar banco se necessário
if ! psql "postgresql://${ODOO_DB_USER}:${ODOO_DB_PASSWORD}@${PGHOST}:${PGPORT}/${ODOO_DB_NAME}" -c '\dt' | grep -q 'ir_module_module'; then
    echo "Banco ${ODOO_DB_NAME} vazio, inicializando módulos base..."
    odoo -c /etc/odoo/odoo.conf -i base --without-demo=all
fi

# Iniciar Odoo normalmente
exec odoo -c /etc/odoo/odoo.conf --without-demo=all "$@"
