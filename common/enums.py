from enum import Enum

class CONTAINER_STATUS(Enum):
    RUNNING = 'running'
    STOPPED = 'stopped'
    UNKNOWN = 'unknown'
    REMOVED = 'removed'
    INIT = 'init'
    FAILED = 'failed'