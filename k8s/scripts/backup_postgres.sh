#!/bin/bash
set -e

BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/kairos_pg_dump_$TIMESTAMP.sql"

echo "🚀 Initiating PostgreSQL Backup from Kubernetes..."

# Ensure we are pointing to the correct namespace and pod
POD_NAME=$(kubectl get pods -n kairos -l app=postgres -o jsonpath="{.items[0].metadata.name}")

if [ -z "$POD_NAME" ]; then
    echo "❌ No PostgreSQL pod found in the 'kairos' namespace."
    exit 1
fi

echo "📦 Found Database Pod: $POD_NAME"
echo "⏳ Dumping database..."

kubectl exec -n kairos $POD_NAME -- pg_dumpall -U postgres > $BACKUP_FILE

echo "✅ Backup successfully saved to $BACKUP_FILE"
