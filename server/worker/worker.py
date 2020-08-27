import os
from typing import Optional

from redis import Redis
from rq import Worker
from rq.job import Job

from toniecloud.client import TonieCloud


class ApiWorker(Worker):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.api = TonieCloud(os.environ.get("TONIE_AUDIO_MATCH_USER"), os.environ.get("TONIE_AUDIO_MATCH_PASS"))

    @classmethod
    def find_by_job(cls, job: Job, connection: Redis) -> Optional["ApiWorker"]:
        workers = ApiWorker.all(connection=connection)
        # TODO Handle case where no worker could be found in a reasonable way
        return next(filter(lambda worker: worker.get_current_job() == job, workers))
