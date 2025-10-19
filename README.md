# Github-Follow-N-Star ⭐
A personalized program that helps its user follow back their Github followers and star 4 of their top repositories in the process. This repository uses `Github Actions` to automate each build and execution.


## Initial Setup
1. **Fork The Repo** 🍴

> [!NOTE]
>
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
  >
  > Copy your personal access token value now. You won’t be able to see it again!

4. **Create Repository Secrets** 🤐
    - *`{repo-fork-name}` > Settings > Secrets and Variables > Actions*
    - *Create 2 New Repository Secrets:*
        1. *PERSONAL_ACCESS_TOKEN*
            - `Bearer {paste-the-personal-access-token-value-you-copied-earlier}`
        2. *PERSONAL_USERNAME*
            - `{your-github-username}`

5. **Profit** 💸


## Usage
- **Manual**
    - *Manual execution can be achieved by visiting the repository's `Action` section, selecting the `Follow-N-Star-Action` workflow, and clicking `Run Workflow`*

- **Timer**
    - *The program is scheduled to execute `@12pm every Wednesday`. This can be changed in the `.github/workflows/action.yml` file by adjusting the `Cron Expression` to fit your needs*

```yaml
on:
  schedule:
    - cron: '0 12 * * WED'  # run @12pm every Wednesday (~4x/month)
```


## Github API Rate Limit & Actions Billing
> [!IMPORTANT]
>
> API Limit: 5,000 requests per/hr | Actions: 2,000-mins (500MB)/Month

Using the new `Personal Access Token` created earlier for this repository, API rates will be limited to `5,000 requests per hour`, as well as a `2,000 minute (500MB) Monthly Actions` limit. Currently, the program only has a protection in place to prevent exceeding the user API limit rate:
```python
def check_user_api_info(self, threshold=4000):
``` 
(line-97 in the `github_client_api.py` file, which can be altered), so it's advised that users keep track of their `Actions` usage. Adjusting the `Cron Expression` to execute the program less times a month can also help with this as well.

> [!TIP]
>
> If the program stops early due to exceeding the `API threshold`, the workflow can be ran again after `1-hour` once the user's API rate limit has refreshed, since the program saves explored profiles to file and continues with those not saved to file (as long as `Actions` minutes remain).


## Inspiration
Grew tired of manually following & starring repos :hurtrealbad:
