import os
import asyncio
import aiohttp
import tenacity


# API AUTHENTICATION
headers = {
    "Authorization": os.environ["PERSONAL_ACCESS_TOKEN"]
}


# URL
GET = "get"
PUT = "put"
DELETE = "delete"
USER = "user"
USERS = "users"
GITHUB_API = "https://api.github.com"

# LOGIN
MY_USERNAME = os.environ["PERSONAL_USERNAME"]

# TERMINAL COLORS
GREEN = "\033[32m"      # ok
YELLOW = "\033[33m"     # alert
RED = "\033[31m"        # danger
MAGENTA = "\033[35m"    # login
BLUE = "\033[34m"       # repo
RESET = "\033[0m"       # resets terminal color


def get_key_from_json(json_list, key):
    """ returns a set of key-value strings from a list of json objects """
    string_set = set()
    for obj in json_list:
        string_set.add(obj[key])
    return string_set


def assign_status_code(status_code, repo=None, owner=None):
    """ returns status code information """
    if repo:
        return f"\t{YELLOW}[{status_code}]{RESET} {BLUE}{repo}{RESET}"
    else:
        return f"{MAGENTA}{owner}{RESET} {YELLOW}[{status_code}]{RESET}"


def print_following_status(owner, follow_owner, response):
    """ prints response status code & description for following owner """
    if follow_owner and response.status == 204:
        print(f"{MAGENTA}{owner}{RESET} {GREEN}[+]{RESET}")
    elif not follow_owner and response.status == 204:
        print(f"{MAGENTA}{owner}{RESET} {RED}[-]{RESET}")
    else:
        print(assign_status_code(status_code=response.status, owner=owner))


def print_stargazing_status(repo, star_repo, response):
    """ prints response status code & description for stargazing owner repo"""
    if star_repo and response.status == 204:
        print(f"\t{GREEN}[+]{RESET} {BLUE}{repo}{RESET}")
    elif not star_repo and response.status == 204:
        print(f"\t{RED}[-]{RESET} {BLUE}{repo}{RESET}")
    else:
        print(assign_status_code(status_code=response.status, repo=repo))


class GithubApiClient:
    """ Creates a client session
     for submitting api requests """

    # class initialization
    def __init__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        self.api_used = 0
        self.api_limit = 0

    def update_user_api_info(self, client_response):
        """ updates user API count & limit with integer values """
        self.api_used = int(client_response.headers.get("X-RateLimit-Used"))
        self.api_limit = int(client_response.headers.get("X-RateLimit-Limit"))

    def print_user_api_info(self):
        """ prints user current API information """
        # color code used info
        if self.api_used <= 1666:
            color = GREEN
        elif self.api_used <= 3332:
            color = YELLOW
        else:
            color = RED
        print(f"API Rate Limit {color}[{self.api_used}/{self.api_limit}]{RESET}\n")

    def check_user_api_info(self, threshold=4000):
        """ throws an Exception if user API count exceeds threshold else prints user API information """
        if self.api_used >= threshold:
            raise Exception(f"API Threshold Reached: {threshold}")
        else:
            self.print_user_api_info()

    # attach tenacity retry approach to following method
    @tenacity.retry(
        stop=tenacity.stop.stop_after_attempt(3),
        wait=tenacity.wait_fixed(3),
        reraise=True
    )
    async def send_request(self, method=GET, url=f"{GITHUB_API}/{USERS}/{MY_USERNAME}", is_json=True):
        """ sends get/put/delete requests to url & returns a response. updates user API info after every
        request. default method is get & url is to user's profile. awaits 1-second between requests. NOTE:
        is_json should be set to FALSE if a response is not expected to return a JSON object or when a raw
        client response is preferred """
        # make api request using method
        client_response = await self.session.request(method=method, url=url, headers=headers)
        # wait for 1 second
        await asyncio.sleep(1)
        # update user API rate information
        self.update_user_api_info(client_response=client_response)
        # if response is json format
        if is_json:
            # decode json
            return await client_response.json()
        else:
            # return client response
            return client_response

    async def get_user_api_info(self):
        """ updates client with user current API info. NOTE:
        calls to this endpoint do not count towards limit """
        url = f"{GITHUB_API}/rate_limit"
        await self.send_request(url=url, is_json=False)
        self.check_user_api_info()

    async def get_user_followers(self):
        """ returns a set containing all of a user's followers via api pagination """
        # create url
        page = 1
        url = f"{GITHUB_API}/{USERS}/{MY_USERNAME}/followers?page={page}&per_page={100}"
        # create logins set from client response
        client_response = await self.send_request(url=url, is_json=False)
        set_followers = get_key_from_json(json_list=await client_response.json(), key="login")
        # loop while headers link contains next page urls & update set
        while (client_response.headers.get("link") and
               "rel=\"next\"" in client_response.headers.get("link")): # type: ignore
            url = url.replace(f"?page={page}", f"?page={page + 1}")
            page += 1
            client_response = await self.send_request(url=url, is_json=False)
            set_followers.update(get_key_from_json(json_list=await client_response.json(), key="login"))
        print(f"Followers {GREEN}[{len(set_followers)}]{RESET}\n")
        return set_followers

    async def get_owner_top_repos(self, owner):
        """ returns a set containing an owner's top-4 repositories """
        # create url
        url = f"{GITHUB_API}/{USERS}/{owner}/repos?sort=created&per_page={4}"
        # get json response
        json_response = await self.send_request(url=url, is_json=True)
        # convert response to set & return
        return get_key_from_json(json_list=json_response, key="name")

    async def update_following_status(self, owner, follow_owner=True):
        """ actively makes user follow/unfollow owner & prints status code & description to screen """
        # create url
        url = f"{GITHUB_API}/{USER}/following/{owner}"
        # send put request & get response
        if follow_owner:
            response = await self.send_request(method=PUT, url=url, is_json=False)
        else:
            # send delete request & get response
            response = await self.send_request(method=DELETE, url=url, is_json=False)
        print_following_status(owner=owner, follow_owner=follow_owner, response=response)

    async def update_stargazing_status(self, owner, repo, star_repo=True):
        """ actively makes user star/unstar owner repo & prints status code & description to screen """
        # create url
        url = f"{GITHUB_API}/{USER}/starred/{owner}/{repo}"
        # send put request & get response
        if star_repo:
            response = await self.send_request(method=PUT, url=url, is_json=False)
        else:
            # send delete request & get response
            response = await self.send_request(method=DELETE, url=url, is_json=False)
        # print response status
        print_stargazing_status(repo=repo, star_repo=star_repo, response=response)

    async def close(self) -> None:
        """ closes client session """
        await self.session.close()