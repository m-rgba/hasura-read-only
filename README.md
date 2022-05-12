# Hasura Read-Only
Example read-only database implementation using Hasura.
- Postgres container contains 2 databases:
    - `read_only_db` with a user with read-only permissions
    - `pg_write_db` (defined in the docker-compose.yml) which has full read/write priviledges
    - Connected to Hasura using metadata

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/m-rgba/hasura-read-only/tree/main)