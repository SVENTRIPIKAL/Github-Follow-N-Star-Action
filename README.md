# Github-Follow-N-Star ⭐
An automation program that helps users follow back their Github followers and star 4 of their top repositories in the process. This repository uses `Github Actions` to automate each build and execution.


<br />
<details>
  <summary><strong>Table of Contents</strong></summary>

- [Terminal Example](#terminal-example)
- [Initial Setup](#initial-setup)
- [Running Workflow](#running-workflow)
- [Workflow Timings](#workflow-timings)
- [Github API Rate Limit & Actions Allowance](#github-api-rate-limit--actions-allowance)
- [References](#references)
- [Inspiration](#inspiration)
</details>
<br />


## Terminal Example
<img src="./images/example-output.png" alt="Terminal Output Example" width="300">

---

## Initial Setup
1. **Fork The Repo** 🍴

> [!NOTE]
> Forking the repo may already grant this permission but just in case

2. **Grant Workflow Read/Write Permission** ✍️
    - *`{repo-fork-name}` > Settings > Actions > General*
    - *Workflow Permissions > Read and Write Permissions*
    - *Save*

3. **Create a Personal Access Token** 🥇
    - *Profile > Settings > Developer Settings > Personal Access Tokens > Tokens (Classic)*
    - *Generate New Token (Classic)*
    - *Name Your Token (example: `GITHUB_API_FOLLOW_N_STAR`)*
    - *Optional: Add Token Expiration*
    - *Select Scopes:*
        - *`public_repo`*
        - *`read:user`*
        - *`user:follow`*
    - *Update Token*
  > [!WARNING]
  > Copy your personal access token value now. You won’t be able to see it again!

4. **Create Repository Secrets** 🤐
    - *`{repo-fork-name}` > Settings > Secrets and Variables > Actions*
      
    - *Create 2 New Repository Secrets:*
        1. *PERSONAL_ACCESS_TOKEN*
            - `Bearer {paste-the-personal-access-token-value-you-copied-earlier}`
              
        2. *PERSONAL_USERNAME*
            - `{your-github-username}`

5. **Profit** 💸

---

## Running Workflow
- **Manual:**
    - *Manual executions can be achieved by visiting the repository's `Action` section, selecting the `Follow-N-Star-Action` workflow, and clicking `Run Workflow`*

- **Scheduled:**
    - *The program is scheduled to execute `@12pm every Wednesday`. This can be changed in the `.github/workflows/actions.yml` file by adjusting the `Cron Expression` to fit your needs*

```yaml
on:
  schedule:
    - cron: '0 12 * * WED'  # run @12pm every Wednesday (~4x/month)
```

---

## Workflow Timings
- **Environment Setup:**
    - *~8 seconds*
      
- **Cost Per Follower:**
    - *~7.28 seconds*

---

## Github API Rate Limit & Actions Allowance
> [!IMPORTANT]
> API Limit: 5,000 requests per/hr | Actions Allowance: 2,000-mins (500MB) per/Month

Using the new `Personal Access Token` created earlier for this repository, API rates will be limited to `5,000 requests per hour`, as well as a `2,000 minute (500MB) Free Monthly Actions` allowance. Currently, the program only has a protection in place to prevent exceeding the user API limit rate:
```python
def check_user_api_info(self, threshold=4000):
``` 
(`line-97` in the `model/github_api_client.py` file, which can be increased), so it's advised that users keep track of their `Actions` usage. Adjusting the `Cron Expression` to execute the program less times a month can also help with this as well.

> [!TIP]
> If the program stops early due to exceeding the `API threshold`, the workflow can be ran again after `1-hour` once the user's API rate limit has refreshed, since the program saves explored profiles to file and continues with those not saved to file (as long as `Actions` minutes remain).

---

## References

For more information explaining previous topics and documentation used for communicating with Github API, the following links have be curated:

* [Creating a Personal Access Token (Classic)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)

* [Personal Access Token Scopes](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes)

* [Authenticating to the REST API](https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api?apiVersion=2022-11-28)

* [Rate Limits for the REST API](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28#primary-rate-limit-for-authenticated-users)

* [GitHub Actions Allowance](https://docs.github.com/en/billing/concepts/product-billing/github-actions)

* [Using Pagination in the REST API](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api?apiVersion=2022-11-28)

* [REST API endpoints for Followers](https://docs.github.com/en/rest/users/followers?apiVersion=2022-11-28&versionId=free-pro-team%40latest&restPage=using-pagination-in-the-rest-api#list-followers-of-the-authenticated-user)

* [REST API endpoints for Starring](https://docs.github.com/en/rest/activity/starring?apiVersion=2022-11-28#star-a-repository-for-the-authenticated-user)

* [REST API endpoints for Repositories](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-a-user)

* [Workflow Syntax for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)

* [Github Actions Events: Schedule](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

* [Using Secrets in GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)

* [Github Actions Extensions](https://github.com/marketplace?type=actions)

---

## Inspiration
Grew tired of manually following users & starring more than 1 of their repos 😅
