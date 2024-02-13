from enum import Enum


class FreightStatus(Enum):
    ACTIVE = 'Activo'
    CANCELED = 'Cancelado'

class ProcessStatus(Enum):
    PENDING = 0
    PROCESSED = 1
    PROCESSED_CORRECTLY = 2
    PROCESSED_WITH_ERRORS = 3
    IN_ERROR = 4