import sys
from lcabyg_web_api_py import *

WEB_API_USERNAME = ''
WEB_API_PASSWORD = ''

cli = Client(WEB_API_USERNAME, WEB_API_PASSWORD)
#'testdata/lcabyg/empty/', 'testdata/lcabyg/reno/',
for project_path in ['testdata/lcabyg/single/']:
    data = NewJob(project=collect_json([project_path]))
    job, output = cli.submit_job(data)  # The results are in the output variable!!!
    print(f'output {output}')
    print(f'{project_path}: {job.status}')
