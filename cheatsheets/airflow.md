# Commands

airflow dags trigger llm_text_orchestration \
  --conf '{"text": "Airflow is a powerful tool for orchestrating LLM pipelines."}'
  
airflow dags list-runs -d llm_text_orchestration


## 1. Why Airflow needs a database

The database is **the brain and memory** of Airflow.

Airflow is constantly answering questions like:

- Has this task already run?
- Did it succeed or fail?
- Should it retry?
- What data was passed between tasks?
- Which DAGs are paused? 
- What’s scheduled next?

All of this lives in the DB.

### 1.1 What is stored in the DB (concrete)
| Stored in DB   | Why                             |
| -------------- | ------------------------------- |
| DAG runs       | Track executions over time      |
| Task instances | State: running, failed, success |
| Retry counters | So retries work                 |
| Schedules      | When to trigger next            |
| XCom metadata  | Pass data between tasks         |
| SLA misses     | Alerting                        |
| User actions   | Pausing, triggering DAGs        |


Without a DB:
- ❌ No retries
- ❌ No scheduling
- ❌ No backfills
- ❌ No parallelism
- ❌ No observability

### 1.2 Example without DB (what breaks)

Imagine your LLM sentiment task fails.

Airflow asks:

“Is this the first failure or the second?”

Without DB:

It wouldn’t know

Retry logic is impossible

## 2. Why Airflow needs a webserver

The webserver is **your control plane.**

- It lets you:
- See DAGs
- Trigger runs
- Inspect logs
- Debug failures
- Pause / resume workflows
Think of it as Kubernetes Dashboard, but for workflows.

## 2.1 Could you run without UI?
Technically yes (CLI only), but:

| Without Webserver | Impact          |
| ----------------- | --------------- |
| No DAG graph      | Hard to debug   |
| No logs view      | Painful         |
| No manual trigger | Poor UX         |
| No monitoring     | Blind execution |



For ML/LLM pipelines, this is **not optional.**

## 3. Why Airflow needs a scheduler

This is subtle but critical.

The scheduler:

- Reads DAG definitions
- Creates task instances
- Decides what runs next
- Queues tasks for execution

It:

- Reads DAG code
- Writes state to DB
- Tells workers what to do

Without scheduler:
❌ DAG never runs
❌ No parallelism
❌ No dependency resolution