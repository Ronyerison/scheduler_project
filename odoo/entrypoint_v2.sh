#!/bin/bash

set -e

echo "Aguardando PostgreSQL..."
export PGPASSWORD="$PASSWORD"

echo "Parâmetros recebidos: $@"

while ! pg_isready -h "$HOST" -p 5432 -U "$USER"; do
  sleep 2
done

# Verifica se o banco já existe
if psql -h "$HOST" -U "$USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "Banco '$DB_NAME' já existe, iniciando Odoo normalmente."
else
    echo "Criando banco '$DB_NAME' com módulos base..."
    odoo -d "$DB_NAME" -i base --without-demo=all --stop-after-init
fi

# Ignora os dois primeiros parâmetros enviados pelo PyCharm: /usr/bin/python3 e /usr/bin/odoo
shift 2

# Primeiro argumento útil após shift
CMD="$1"
shift

if [[ "$CMD" == "update" ]]; then
    echo "Atualizando módulos: $@"
    exec odoo \
        --db_user="$USER" \
        --db_password="$PASSWORD" \
        --db_host="$HOST" \
        --db_port=5432 \
        --db-filter=^.*$ \
        --database="$DB_NAME" \
        -u "$@" \
        --stop-after-init
else
    echo "Iniciando o servidor Odoo normalmente..."
    exec odoo \
        --db_user="$USER" \
        --db_password="$PASSWORD" \
        --db_host="$HOST" \
        --db_port=5432 \
        --db-filter=^.*$ \
        --database="$DB_NAME"

    tail -f /dev/null
fi
