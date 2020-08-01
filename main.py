from indeed import get_whole_jobs as get_indeed_jobs
from linkedin import get_whole_jobs as get_linkedin_jobs
from save import save_to_file

indeed_jobs = get_indeed_jobs()
linkedin_jobs = get_linkedin_jobs()

jobs = indeed_jobs + linkedin_jobs
save_to_file(jobs)
