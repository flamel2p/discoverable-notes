
Coolify's self-hosted Supabase uses a `docker-compose` template. The Postgres container accepts config overrides via the `command` field or environment variables. The cleanest way in Coolify:

Go to your Supabase resource → **"Advanced"** → **"Custom Docker Compose"**, find the `db` service and add a `command` override:

yaml

```yaml
db:
  image: supabase/postgres:15.x.x
  command:
    - postgres
    - -c
    - max_connections=50
    - -c
    - shared_buffers=256MB
    - -c
    - pg_stat_statements.track=none   # disables pg_stat_statements tracking
    - -c
    - effective_cache_size=512MB
    - -c
    - work_mem=8MB
```

Alternatively, in the Supabase service **Environment Variables** section in Coolify, you can set:

```
POSTGRES_MAX_CONNECTIONS=50
```

But this only works if the Supabase Postgres image actually reads that env var — not all versions do. The `command` override is more reliable.

To verify what's active after restart, run in your Coolify terminal or via SSH:

bash

```bash
docker exec -it <supabase-db-container> psql -U postgres -c "SHOW max_connections;"
docker exec -it <supabase-db-container> psql -U postgres -c "SHOW shared_buffers;"
```