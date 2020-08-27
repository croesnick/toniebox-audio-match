import functools
import os

# from redis import Redis
# from rq import get_current_job
#
# from worker.worker import ApiWorker
from toniecloud.client import TonieCloud


def toniecloud_access(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # redis = Redis.from_url(os.getenv("TONIE_AUDIO_MATCH_REDIS_URI"))
        # current_job = get_current_job()
        # worker = ApiWorker.find_by_job(job=current_job, connection=redis)

        api = TonieCloud(os.environ.get("TONIE_AUDIO_MATCH_USER"), os.environ.get("TONIE_AUDIO_MATCH_PASS"))
        return wrapper(api, *args, **kwargs)

    return wrapper
