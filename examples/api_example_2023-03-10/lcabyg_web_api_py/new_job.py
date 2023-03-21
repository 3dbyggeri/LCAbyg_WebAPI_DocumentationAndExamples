from dataclasses import dataclass, InitVar
from sbi_web_api_py.type_hinting import JsonList
from lcabyg_web_api_py.utils import pack_json


@dataclass
class NewJob:
    priority: int = 0
    job_target: str = 'lcabyg5+br23'
    job_target_min_ver: str = ''
    job_target_max_ver: str = ''
    job_arguments: str = ''
    extra_input: str = ''
    input_blob: str = ''
    project: InitVar[JsonList] = None

    def __post_init__(self, project: JsonList):
        self.input_blob = pack_json(project)
        print(self.input_blob)

    def to_dict(self):
        return self.__dict__
