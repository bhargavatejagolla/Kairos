# PostgreSQL Backup & Recovery Plan

## Architecture
Our PostgreSQL instance runs as a Kubernetes `StatefulSet` attached to a `PersistentVolumeClaim` (PVC). While the PVC ensures data survives pod restarts and rescheduling, it does not protect against volume corruption or catastrophic cluster failure.

## Backup Strategy
In production, a Kubernetes CronJob will be deployed to automatically execute pg_dump every night.

### Nightly Backup Flow
1. **CronJob Triggers**: Every night at 02:00 AM.
2. **Execute**: Runs `pg_dump -U postgres -d kairos > backup.sql`.
3. **Compress**: Compresses the dump into a `.tar.gz` archive.
4. **Offsite Transfer**: Uploads the archive to an S3 Bucket (e.g., AWS S3, Cloudflare R2) using the AWS CLI.

## Recovery Procedure
If a catastrophic failure occurs, follow these steps to restore from S3:

1. **Download Backup**: Fetch the latest `.tar.gz` from the S3 bucket.
2. **Transfer to Pod**:
   ```bash
   kubectl cp backup.sql kairos/postgres-0:/tmp/backup.sql
   ```
3. **Restore**:
   ```bash
   kubectl exec -it postgres-0 -n kairos -- psql -U postgres -d kairos -f /tmp/backup.sql
   ```
