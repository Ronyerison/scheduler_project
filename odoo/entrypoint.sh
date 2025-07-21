#!/bin/bash

set -e

echo "🛠️ Parâmetros recebidos: $3 $4"
echo "🚀 Iniciando Odoo Arena..."

# Configuração das variáveis de ambiente
export PGPASSWORD="$PASSWORD"

echo "📡 Aguardando PostgreSQL ficar disponível..."
while ! pg_isready -h "$HOST" -p 5432 -U "$USER" -q; do
  echo "   ⏳ PostgreSQL ainda não está pronto, aguardando..."
  sleep 3
done

echo "✅ PostgreSQL está pronto!"

# Verifica se o banco de dados já existe
echo "🔍 Verificando se o banco '$DB_NAME' existe..."
if psql -h "$HOST" -U "$USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo "✅ Banco '$DB_NAME' já existe"
else
    echo "📦 Criando banco '$DB_NAME' e instalando módulos base..."
    odoo \
        --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons \
        --db_user="$USER" \
        --db_password="$PASSWORD" \
        --db_host="$HOST" \
        --db_port=5432 \
        --database="$DB_NAME" \
        --init=base \
        --without-demo=all \
        --stop-after-init \
        --logfile=/dev/stdout

    echo "✅ Banco criado com sucesso!"
fi

if [[ "$3" == "update" ]]; then
    echo "Atualizando módulos: $4"
    exec odoo \
        --db_user="$USER" \
        --db_password="$PASSWORD" \
        --db_host="$HOST" \
        --db_port=5432 \
        --db-filter=^.*$ \
        --database="$DB_NAME" \
        -u "$4" \
        --stop-after-init
else
    echo "🌐 Iniciando servidor Odoo..."
    echo "📂 Addons path: /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons"
    echo "🔗 Acesse: http://localhost:8069"
    echo "📊 Database: $DB_NAME"
    echo ""

    # Inicia o Odoo
    exec odoo -c /etc/odoo/odoo.conf
fi

