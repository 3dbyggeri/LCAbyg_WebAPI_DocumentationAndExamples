import sys
from uuid import UUID
import urllib.parse
from typing import Optional, Dict, Tuple, Any
import requests
from sbi_web_api_py.type_hinting import JsonObject


class AuthTokenExpired(Exception):
    def __init__(self, res: requests.Response):
        self.response = res


def ping(api_root: str) -> str:
    return get(f'{api_root}/v2/ping')


def ping_secure(api_root: str, **kwargs) -> str:
    return get(f'{api_root}/v2/ping_secure', **kwargs)


def login_via_query(api_root: str, username: str, password: str) -> str:
    query = urllib.parse.urlencode(dict(username=username, password=password))
    res = post(f'{api_root}/v2/login?{query}')
    UUID(res)  # test that the returned string is an uuid, we dont want to return it however
    return res


def login_via_body(api_root: str, username: str, password: str) -> str:
    res = post(f'{api_root}/v2/login', data=dict(username=username, password=password))
    UUID(res)  # test that the returned string is an uuid, we dont want to return it however
    return res


def login_via_headers(api_root: str, username: str, password: str) -> str:
    res = post(f'{api_root}/v2/login', auth=(username, password))
    UUID(res)  # test that the returned string is an uuid, we dont want to return it however
    return res


def get_account(api_root: str, **kwargs) -> JsonObject:
    return get(f'{api_root}/v2/account', **kwargs)


def get_jobs(api_root: str, **kwargs):
    return get(f'{api_root}/v2/jobs', **kwargs)


def get_job_by_id(api_root: str, job_id: str, **kwargs):
    return get(f'{api_root}/v2/jobs/{job_id}', **kwargs)


def post_job(api_root: str, payload: dict, **kwargs):
    return post(f'{api_root}/v2/jobs', payload, **kwargs)


def get_job_input_by_id(api_root: str, job_id: str, **kwargs):
    return get(f'{api_root}/v2/jobs/{job_id}/input', **kwargs)


def get_job_output_by_id(api_root: str, job_id: str, **kwargs):
    return get(f'{api_root}/v2/jobs/{job_id}/output', **kwargs)


def mark_job_as_finished(api_root: str, job_id: str, **kwargs):
    return delete(f'{api_root}/v2/jobs/{job_id}', **kwargs)


def get(url: str,
        headers: Optional[Dict] = None,
        auth_token: Optional[UUID] = None) -> Any:

    if auth_token:
        if not headers:
            headers = dict()
        headers['Authorization'] = f'Bearer {auth_token}'
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 440:
        raise AuthTokenExpired(res)
    else:
        print(f'GET ERROR: {res.text}', file=sys.stderr)
        res.raise_for_status()


def post(url: str,
         data: Optional[Dict] = None,
         headers: Optional[Dict] = None,
         auth_token: Optional[UUID] = None,
         auth: Optional[Tuple[str, str]] = None) -> Any:

    if auth_token:
        if not headers:
            headers = dict()
        headers['Authorization'] = f'Bearer {auth_token}'
    res = requests.post(url, json=data, headers=headers, auth=auth)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 440:
        raise AuthTokenExpired(res)
    else:
        print(f'POST ERROR: {res.text}', file=sys.stderr)
        res.raise_for_status()


def put(url: str,
         data: Optional[Dict] = None,
         headers: Optional[Dict] = None,
         auth_token: Optional[UUID] = None,
         auth: Optional[Tuple[str, str]] = None) -> Any:

    if auth_token:
        if not headers:
            headers = dict()
        headers['Authorization'] = f'Bearer {auth_token}'
    res = requests.put(url, json=data, headers=headers, auth=auth)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 440:
        raise AuthTokenExpired(res)
    else:
        print(f'PUT ERROR: {res.text}', file=sys.stderr)
        res.raise_for_status()


def delete(url: str,
        headers: Optional[Dict] = None,
        auth_token: Optional[UUID] = None) -> Any:

    if auth_token:
        if not headers:
            headers = dict()
        headers['Authorization'] = f'Bearer {auth_token}'
    res = requests.delete(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 440:
        raise AuthTokenExpired(res)
    else:
        print(f'DELETE ERROR: {res.text}', file=sys.stderr)
        res.raise_for_status()


