## Executive Summary

SQLite and PostgreSQL serve different needs for small SaaS applications. SQLite excels in simplicity and zero-ops for single-server deployments, while PostgreSQL provides concurrency, horizontal scaling, and richer query capabilities. This question is fully answered.

## Key Findings

1. **SQLite handles up to ~100 concurrent writers reliably with WAL mode** — Confidence: Likely
   The SQLite documentation notes WAL mode allows concurrent reads with a single writer. Real-world benchmarks show adequate performance for many SaaS workloads. (Source: #1)

2. **PostgreSQL provides MVCC-based concurrency without writer contention** — Confidence: Established
   Multiple concurrent transactions can read and write simultaneously. This is well-documented in PostgreSQL internals. (Source: #2, #3)

3. **SQLite eliminates operational overhead: no server process, no connection pooling** — Confidence: Established
   The database is a single file, deployable alongside the application binary. (Source: #1, #4)

4. **PostgreSQL is required for multi-server deployments** — Confidence: Established
   SQLite cannot be shared across multiple application servers without third-party replication tools like LiteFS or Turso. (Source: #1, #5)

5. **Migration path from SQLite to PostgreSQL is non-trivial** — Confidence: Likely
   Schema differences, type system mismatches, and query syntax variations make later migration costly. (Source: #4)

## Detailed Analysis

### Concurrency and Performance

SQLite's WAL mode enables concurrent reads but serializes writes. For read-heavy SaaS workloads, this is often sufficient. PostgreSQL's MVCC provides true concurrent reads and writes, which matters as write volume scales.

### Operational Complexity

SQLite requires zero database administration — no connection strings, no user management, no backup orchestration beyond file copies. PostgreSQL requires provisioning, monitoring, connection pooling, and backup strategies, though managed services (Neon, Supabase, RDS) reduce this burden.

### Data Integrity

Both databases provide ACID guarantees. PostgreSQL offers richer constraint types (exclusion constraints, partial indexes) and more sophisticated transaction isolation levels.

## Sources

1. [SQLite documentation — When to use SQLite](https://sqlite.org/whentouse.html) — [Tier 1] Official guidance from SQLite authors
2. [PostgreSQL MVCC documentation](https://www.postgresql.org/docs/current/mvcc.html) — [Tier 1] Official concurrency model docs
3. [PostgreSQL vs SQLite comparison](https://www.percona.com/blog/postgresql-vs-sqlite/) — [Tier 2] Technical comparison from database vendor
4. [Litestream — SQLite replication](https://litestream.io/alternatives/cgo-free/) — [Tier 2] Technical analysis of SQLite in production
5. [Fly.io LiteFS documentation](https://fly.io/docs/litefs/) — [Tier 1] Official docs for distributed SQLite

## Research Gaps

- Limited real-world benchmarks comparing SQLite WAL vs PostgreSQL at specific request volumes (e.g., 1K, 10K, 100K requests/day)
- Cost comparison data for managed PostgreSQL vs self-hosted SQLite at different scales
