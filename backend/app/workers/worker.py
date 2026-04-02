from rq import Connection, Worker

from app.core.config import settings
from app.core.redis import get_redis_connection


def run_worker() -> None:
    redis_conn = get_redis_connection()
    with Connection(redis_conn):
        worker = Worker([settings.rq_queue])
        worker.work(with_scheduler=True)


if __name__ == "__main__":
    run_worker()
