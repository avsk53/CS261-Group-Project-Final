import requests
from sqlalchemy import select, insert, update
from app import session
from database import *
import datetime

# Personal access token is specified in request header
headers = {'Authorization': 'token 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'}


def get_quality(url, prs):
    pull_number = 0
    results = []
    sample = 30
    for i in range(sample):
        try:
            pr = prs[i]
            pull_number = pr['url'].split("/")[1]
            endpoint = f"pulls/{pull_number}/comments"

            # Make a GET request to the endpoint
            response = requests.get(url + endpoint, headers=headers)
            comments = len(response.json())
            results.append(comments)
        except:
            break

    quality = 10 * (10 - (sum(results) / sample))
    return max(0, min(quality, 100))

def pulls_last_week(url):
    endpoint = '/pulls?state=closed'

    # Make a GET request to the endpoint
    response = requests.get(url + endpoint, headers=headers)
    pulls_this_week = 0
    for pr in response.json():
        merged = pr.get("merged_at")

        if merged is None: continue

        merged = datetime.datetime.strptime(merged, '%Y-%m-%dT%H:%M:%SZ')

        # Count it if it was merged in the last week
        if merged + datetime.timedelta(days=7) > datetime.datetime.now():
            pulls_this_week += 1
        else:
            break

    # Return the total number of pull requests this week
    return pulls_this_week, response.json()

def deploys_last_month(url):
    endpoint = '/deployments'

    # Make a GET request to the endpoint
    response = requests.get(url + endpoint, headers=headers)

    deploys_this_month = 0
    for deploy in response.json():
        created = deploy.get("created_at")
        # print(f"{deploy['description']} created at {deploy.get('created_at')}")

        if created is None: continue

        created = datetime.datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ')

        # Count it if it was created in the last month
        if created + datetime.timedelta(days=30) > datetime.datetime.now():
            deploys_this_month += 1
        else:
            break

    # Return the total number of deployments this month
    return deploys_this_month

def test_success_rate(url):
    endpoint = '/actions/runs'

    # Make a GET request to the endpoint
    response = requests.get(url + endpoint, headers=headers)

    total = 0
    passed = 0
    
    for run in response.json()["workflow_runs"]:
        created = run.get("created_at")
        created = datetime.datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ')

        # print(f"{run['id']} | {run['conclusion']} | {run['status']} | {created}")

        # Count it if it was run in the last week
        if created + datetime.timedelta(days=7) > datetime.datetime.now():
            total += 1
            if run.get("conclusion") == "success":
                passed += 1
        else:
            break

    return passed / total * 100

def get_churn(url):
    endpoint = '/stats/code_frequency'

    # Make a GET request to the endpoint
    response = requests.get(url + endpoint, headers=headers)

    this_week = response.json()[0]

    # Percentage of lines deleted over lines added
    if this_week[1] == 0:
        churn = 100
    else:
        churn = min(abs(this_week[2]) / this_week[1] * 100, 100)
    return churn

def scrape(project_id):
    '''Function to scrape metrics for a given project by calling each specific
    request and building up a final list of metrics '''

    project = session.get(Project_Table, project_id)
    repo_link = project.github_link

    # passed in link is parsed to get owner and repo name
    parse = repo_link.split("/")
    repo_link = "/" + "/".join(parse[-2:])

    # url for passed in repository is constructed
    url = 'https://api.github.com/repos' + repo_link

    # all the necessary metrics are scraped
    try:
        num_pulls, prs = pulls_last_week(url)
        quality = get_quality(url, prs)
        churn = get_churn(url)

        tests_success = test_success_rate(url)
        num_deploys = deploys_last_month(url)
        if num_deploys > 30:
            num_deploys = 30
    except:
        num_pulls = project.number_of_people
        quality = 60
        churn = 40
        tests_success = 60
        num_deploys = 5

    data = {
        6: quality,
        7: num_pulls / project.number_of_people,
        8: num_deploys / 4, # Maximum is 1 deployment each day
        9: tests_success, # Percentage, from 0 to 100
        10: churn, # Percentage, from 0 to 100
    }

    for metric_id in data:
        session.execute(
            update(Metric_Assignment_Table)
            .where(Metric_Assignment_Table.project_id == project_id)
            .where(Metric_Assignment_Table.metric_id == metric_id)
            .values(metric_value=data[metric_id])
        )
    session.commit()

    # print(f"Quality: {data[6]}")
    # print(f"Code review frequency: {data[7]}")
    # print(f"Deployment frequency: {data[8]}")
    # print(f"Test success rate: {data[10]}")
    # print(f"Code churn: {data[11]}")

# scrape('https://github.com/freeCodeCamp/freeCodeCamp')