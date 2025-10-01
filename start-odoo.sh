#!/bin/bash
set -e

echo "===== Variáveis de ambiente ====="
echo "PGHOST=$PGHOST"
echo "PGPORT=$PGPORT"
echo "ODOO_DB_NAME=$ODOO_DB_NAME"
echo "ODOO_DB_USER=$ODOO_DB_USER"
echo "ODOO_DB_PASSWORD=$ODOO_DB_PASSWORD"
echo "ADMIN_PASSWORD=$ADMIN_PASSWORD"
echo "================================="

# Aguardar PostgreSQL
echo "Aguardando PostgreSQL..."
until pg_isready -h "$PGHOST" -p "$PGPORT" -U "$ODOO_DB_USER" >/dev/null 2>&1; do
    sleep 2
done
echo "PostgreSQL disponível!"

# Substituir variáveis no template de configuração
envsubst < /etc/odoo/odoo.conf.template > /etc/odoo/odoo.conf

# Inicializar banco se vazio
echo "Verificando banco $ODOO_DB_NAME..."
export PGPASSWORD="$ODOO_DB_PASSWORD"
TABLE_COUNT=$(psql -h "$PGHOST" -U "$ODOO_DB_USER" -d "$ODOO_DB_NAME" -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';" | xargs)
if [ "$TABLE_COUNT" -eq 0 ]; then
    echo "Banco vazio, inicializando módulos base..."
    odoo -c /etc/odoo/odoo.conf -i base --without-demo=all &
    ODOO_PID=$!
else
    echo "Banco já possui tabelas ($TABLE_COUNT), pulando inicialização base."
    odoo -c /etc/odoo/odoo.conf --without-demo=all &
    ODOO_PID=$!
fi

# Iniciar Nginx em foreground
echo "Iniciando Nginx..."
nginx &

# Esperar Odoo ficar disponível
echo "Aguardando Odoo web (/web/login) ficar disponível..."
until curl -s -o /dev/null -w "%{http_code}" http://localhost:80/web/login | grep -q "200"; do
    sleep 2
done

echo "Odoo pronto! Página de login disponível."

# Esperar processo principal do Odoo terminar
wait $ODOO_PID
