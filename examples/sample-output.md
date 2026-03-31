# Sample Output: "What are the real-world tradeoffs between SQLite and PostgreSQL for new web applications?"

> This is an example output from `/deep-research standard` demonstrating source tiers, confidence labels, and quality gates.

---

**Scope**: standard (3 breadth agents, 2 depth agents)

**Research angles**:
1. Performance characteristics and scaling limits
2. Operational complexity and deployment tradeoffs
3. When SQLite actually works in production (case studies)

---

## Executive Summary

The research question is **fully answered**. SQLite and PostgreSQL serve different operational profiles, but the tradeoff is more nuanced than "SQLite for small, Postgres for big." SQLite excels in read-heavy single-server deployments and eliminates an entire infrastructure dependency, while PostgreSQL is necessary when you need concurrent writes from multiple servers, advanced querying (full-text, JSONB, CTEs with write operations), or managed cloud hosting. The emergence of tools like Litestream and LiteFS has shifted the boundary — SQLite is now viable for a larger class of production applications than conventional wisdom suggests.

## Key Findings

1. **SQLite handles more concurrent readers than most developers expect** — Confidence: **Established**
   SQLite in WAL mode supports unlimited concurrent readers with a single writer, achieving read throughput comparable to PostgreSQL for datasets under 1TB. The bottleneck is concurrent writes, not reads. (Sources: #1, #3)

2. **PostgreSQL's operational overhead is frequently underestimated by teams choosing it "to scale later"** — Confidence: **Likely**
   Connection pooling (PgBouncer), vacuuming, backup configuration, and version upgrades represent ongoing maintenance that SQLite eliminates entirely. For teams without a DBA, this overhead often exceeds the cost of SQLite's limitations. (Source: #4)

3. **Litestream enables SQLite replication to S3, closing the durability gap** — Confidence: **Established**
   Litestream continuously streams WAL changes to S3-compatible storage, providing point-in-time recovery without a separate backup system. Used in production by Fly.io customers and the Litestream author's own applications. (Sources: #2, #5)

4. **SQLite cannot serve multiple application servers writing to the same database** — Confidence: **Established**
   This is a fundamental architectural constraint, not a performance limitation. LiteFS (distributed SQLite by Fly.io) provides read replicas but still requires a single primary writer node. Applications requiring multi-server write concurrency need PostgreSQL or equivalent. (Sources: #1, #6)

5. **Rails 8 defaulting to SQLite signals mainstream acceptance for certain workloads** — Confidence: **Likely**
   DHH and the Rails core team chose SQLite as the default database for new Rails 8 applications, explicitly arguing it's sufficient for most web apps that run on a single server. This is a notable departure from the prior Rails convention of defaulting to PostgreSQL in production. (Source: #7)

6. **PostgreSQL's JSONB, full-text search, and extension ecosystem have no SQLite equivalent** — Confidence: **Established**
   While SQLite has JSON functions and FTS5, PostgreSQL's JSONB indexing, pg_trgm, PostGIS, and the broader extension ecosystem (pgvector, TimescaleDB) offer capabilities that SQLite cannot match. Teams with these requirements should not consider SQLite. (Sources: #1, #3)

## Detailed Analysis

### Performance and Scaling

SQLite's performance ceiling is higher than commonly assumed. In WAL mode, read operations run concurrently without blocking, and a single server can handle thousands of read queries per second for datasets that fit comfortably in memory. [Tier 1] The SQLite documentation explicitly states the design target as "websites that get fewer than 100K hits/day" but notes this is conservative — real-world deployments regularly exceed this. (Source: #1)

PostgreSQL's advantage manifests primarily in write-heavy concurrent workloads. Connection pooling via PgBouncer or pgcat becomes necessary at scale, but this infrastructure exists and is well-understood. [Tier 2] Benchmarks from Percona show PostgreSQL handling 10x+ more concurrent write transactions than SQLite on equivalent hardware. (Source: #3)

The critical threshold is architectural, not performance-based: the moment your application requires a second server writing to the database, PostgreSQL (or another client-server database) becomes mandatory.

### Operational Complexity

This was the most surprising finding across agents. [Tier 3] Multiple practitioners report that choosing PostgreSQL "because we might need it later" frequently creates more operational burden than the scaling problems it prevents. Connection management, backup verification, version upgrades across environments, and the gap between local SQLite (used in development) and production PostgreSQL all introduce failure modes. (Source: #4)

SQLite's operational model is uniquely simple: the database is a single file. Backups are file copies (or Litestream for continuous replication). There is no connection pooling, no vacuum tuning, no separate process to monitor. [Tier 1] (Source: #1)

However, this simplicity has a hard ceiling. SQLite provides no built-in authentication, no role-based access control, and no query-level resource limits — all features PostgreSQL provides out of the box. For multi-tenant applications or teams with compliance requirements around data access, these are not optional. (Sources: #1, #3)

### Production Case Studies

[Tier 1] Fly.io built LiteFS specifically to enable distributed SQLite for their platform, and multiple Fly.io customers run production applications on SQLite with Litestream for durability. (Source: #6)

[Tier 2] Expensify reported running SQLite in production handling billions of database operations, though their architecture is heavily customized and not representative of typical deployments. (Source: #8)

[Tier 3] The "SQLite is not a toy database" blog post by Anton Zhiyanov catalyzed much of the recent re-evaluation of SQLite for web applications, compiling benchmarks and case studies. While thorough, it is a single author's analysis and some claims lack independent verification. (Source: #4)

## Sources

1. [SQLite: When to Use](https://www.sqlite.org/whentouse.html) — [Tier 1] Official SQLite documentation on appropriate use cases and design limits
2. [Litestream - Streaming SQLite Replication](https://litestream.io/) — [Tier 1] Official project documentation for SQLite replication to S3
3. [PostgreSQL vs SQLite Benchmark](https://www.percona.com/blog/postgresql-vs-sqlite/) — [Tier 2] Percona's comparative benchmarks with methodology
4. [SQLite is not a toy database](https://antonz.org/sqlite-is-not-a-toy-database/) — [Tier 3] Comprehensive practitioner analysis with benchmarks (single author)
5. [Ben Johnson - How I Use Litestream](https://fly.io/blog/how-i-use-litestream/) — [Tier 2] Litestream author's production usage on Fly.io blog
6. [LiteFS - Distributed SQLite](https://fly.io/docs/litefs/) — [Tier 1] Fly.io official documentation for distributed SQLite
7. [Rails 8 Default Database](https://rubyonrails.org/2024/11/7/rails-8-no-paas-required) — [Tier 1] Official Rails 8 release announcement
8. [Expensify SQLite at Scale](https://blog.expensify.com/2018/01/08/scaling-sqlite-to-4m-qps-on-a-single-server/) — [Tier 2] Expensify engineering blog on production SQLite usage

## Research Gaps

- Long-term migration stories (SQLite → PostgreSQL) with quantified effort were not found in Tier 1/2 sources. Multiple Tier 3 blog posts discuss this anecdotally but without reproducible specifics.
- Cost comparisons (managed PostgreSQL hosting vs. single-server SQLite) were not investigated — this would require pricing data that varies by provider.
- SQLite extensions ecosystem (sqlean, etc.) was mentioned in breadth research but not explored in depth.
