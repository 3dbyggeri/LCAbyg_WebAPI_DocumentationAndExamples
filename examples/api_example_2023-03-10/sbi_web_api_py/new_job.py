from dataclasses import dataclass, InitVar
from sbi_web_api_py.utils import pack_bytes


@dataclass
class NewJob:
    priority: int = 0
    job_target: str = ''
    job_target_min_ver: str = ''
    job_target_max_ver: str = ''
    job_arguments: str = ''
    extra_input: str = ''
    input_blob: str = ''
    input_data: InitVar[bytes] = None

    def __post_init__(self, input_data: bytes):
        self.input_blob = pack_bytes(input_data)

    def to_dict(self):
        return self.__dict__
