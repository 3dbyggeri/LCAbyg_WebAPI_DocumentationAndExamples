from dataclasses import dataclass
from datetime import datetime
from sbi_web_api_py.type_hinting import JsonObject
from sbi_web_api_py.job_status import JobStatus


@dataclass
class Job:
    id: str
    created: datetime
    account_id: str
    status: JobStatus
    priority: int
    job_target: str
    job_target_min_ver: str
    job_target_max_ver: str
    job_arguments: str
    extra_input: str
    extra_output: str
    input_blob_id: str
    output_blob_id: str
    input_cache_hit: bool
    output_cache_hit: bool

    @staticmethod
    def from_json(data: JsonObject) -> 'Job':
        data['created'] = datetime.strptime(data['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
        data['status'] = JobStatus(data['status'])
        return Job(**data)