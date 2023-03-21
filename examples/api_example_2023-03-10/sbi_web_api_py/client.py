import json
import logging
import time
from typing import List, Tuple
from sbi_web_api_py.type_hinting import JsonList, JsonObject, IdList
from sbi_web_api_py.new_job import NewJob
from sbi_web_api_py.job import Job
from sbi_web_api_py.utils import unpack_bytes
from sbi_web_api_py import raw_api


class JobFailed(Exception):
    def __init__(self, job: Job, output_blob: bytes):
        self.job = job
        self.output_blob = output_blob

    def __str__(self):
        return self.job.extra_output


class Client:

    def __init__(self,
                 username: str,
                 password: str,
                 api_base_url: str = 'https://api1.lcabyg.dk',
                 login_now: bool = True):
        self._username = username
        self._password = password
        self._api_base_url = api_base_url
        self._token = self._login() if login_now else None
        self.api_ping_test()

    def _login(self):
        return raw_api.login_via_body(self._api_base_url, self._username, self._password)

    def _smart_call(self, api_function, *args, **kwargs):
        # Inject the auth token
        if 'auth_token' not in kwargs:
            kwargs['auth_token'] = self._token
        else:
            logging.warning('Auth token for smart_call overridden!')

        # Inject base url
        if 'api_root' not in kwargs:
            kwargs['api_root'] = self._api_base_url
        else:
            logging.warning('Base url for smart_call overridden!')

        try:
            return api_function(*args, **kwargs)
        except raw_api.AuthTokenExpired:
            logging.debug('Token expired. Logging in again automatically.')
            self._token = self._login()
            return api_function(*args, **kwargs)

    def api_ping_test(self):
        assert raw_api.ping(self._api_base_url) == 'pong'
        assert self._smart_call(raw_api.ping_secure) == 'pong secure'

    def api_get_account_info(self) -> JsonObject:
        return self._smart_call(raw_api.get_account)

    def api_submit_job(self, job: NewJob) -> Job:
        res = self._smart_call(raw_api.post_job, payload=job.to_dict())
        return Job.from_json(res)

    def api_get_jobs(self) -> IdList:
        res = self._smart_call(raw_api.get_jobs)
        return res

    def api_get_job(self, job_id: str) -> Job:
        res = self._smart_call(raw_api.get_job_by_id, job_id=job_id)
        return Job.from_json(res)

    def api_get_job_input(self, job_id: str) -> bytes:
        res = self._smart_call(raw_api.get_job_input_by_id, job_id=job_id)
        return unpack_bytes(res)

    def api_get_job_output(self, job_id: str) -> bytes:
        res = self._smart_call(raw_api.get_job_output_by_id, job_id=job_id)
        return unpack_bytes(res)

    def api_mark_job_as_finished(self, job_id: str):
        self._smart_call(raw_api.mark_job_as_finished, job_id=job_id)

    def submit_job(self, job: NewJob, pool_interval: float = 1, auto_mark_as_finished: bool = True) -> Tuple[Job, bytes]:
        job_row = self.api_submit_job(job)

        while not job_row.status.worker_done():
            job_row = self.api_get_job(job_row.id)
            time.sleep(pool_interval)

        output_blob = self.api_get_job_output(job_row.id)

        if job_row.status.failed():
            raise JobFailed(job_row, output_blob)

        if auto_mark_as_finished:
            self.api_mark_job_as_finished(job_row.id)
            job_row = self.api_get_job(job_row.id)

        return job_row, output_blob
