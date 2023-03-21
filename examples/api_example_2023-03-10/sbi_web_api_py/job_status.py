from enum import Enum


class JobStatus(Enum):
    NEW = 'New'
    STARTED = 'Started'
    READY = 'Ready'
    FINISHED = 'Finished'
    ABANDONED = 'Abandoned'
    FAILED = 'Failed'

    def worker_done(self) -> bool:
        if self == JobStatus.NEW or self == JobStatus.STARTED:
            return False
        else:
            return True

    def failed(self) -> bool:
        if self == JobStatus.FAILED or self == JobStatus.ABANDONED:
            return True
        else:
            return False
