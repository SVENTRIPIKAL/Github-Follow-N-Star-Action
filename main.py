import pathlib
from model.github_api_client import *


EXPLORED_LOGINS = pathlib.Path().resolve() / "EXPLORED_LOGINS"


def purge_set(set_followers):
    """ scrubs set by removing usernames whose profiles have been explored and are currently
     followers. Usernames who are no longer followers get added to set_unfollowers. Both sets
     get returned in a list for processing (ie: [set_unfollowers, set_followers]) """
    # if set iterable, read names from file
    if set_followers:
        with open(file=EXPLORED_LOGINS, mode="rt") as file:
            # create set for those who are no longer followers
            set_unfollowers = set()
            # use list comprehension to create list from file lines
            list_names = [line.rstrip() for line in file]
            # if name in list & set, remove name from set since profile has been explored
            for follower in list_names:
                if follower in set_followers:
                    set_followers.discard(follower)
                else:
                    # if name not in set, add them to unfollower set
                    set_unfollowers.add(follower)
            # update color for additions
            if set_followers:
                color = GREEN
            else:
                color = RED
            print(f"Additions {color}[{len(set_followers)}]{RESET} | ", end="")
            # update color for deletions
            if set_unfollowers:
                color = RED
            else:
                color = GREEN
            print(f"Deletions {color}[{len(set_unfollowers)}]{RESET}\n")
    else:
        raise Exception("Data Not Iterable")
    return [set_unfollowers, set_followers]


def write_owner_to_file(owner):
    """ appends owner name to EXPLORED_LOGINS file to reduce future api calls """
    with open(file=EXPLORED_LOGINS, mode="at") as file:
        file.write(f"{owner}\n")
    print()


def delete_owner_from_file(owner):
    """ re-writes & re-sizes EXPLORED_LOGINS file to exclude owner """
    with open(file=EXPLORED_LOGINS, mode="r+") as file:
        # create list of names excluding owner
        list_names = [line for line in file if line.rstrip() != owner]
        # move to start of file
        file.seek(0)
        # write names to file
        file.writelines(list_names)
        # resize file to position
        file.truncate()
    print()


async def follow_n_star():
    """ gets the user's list of followers, reduces it to contain only usernames
    whose pages the user has not explored yet, follows them back, gets their
    top 4 repositories & stars them, then writes the username to an
    EXPLORED_LOGINS file in order to reduce the user's API call count
    the next time this function is executed. Any prior followers saved
    to the file who are no longer followers get removed in the process """
    # create client session object
    client = GithubApiClient()
    try:
        # stop process if internal file does not exist
        if not pathlib.Path(EXPLORED_LOGINS).exists():
            raise FileNotFoundError("File Not Found")

        # make call to API endpoint & update/check user count/limit info
        await client.get_user_api_info()

        # get all user followers
        set_followers = await client.get_user_followers()

        # purge set against EXPLORED_LOGINS file
        purged_sets_list = purge_set(set_followers=set_followers)

        # get set of additions & deletions
        set_additions = purged_sets_list.pop()
        set_deletions = purged_sets_list.pop()

        # show alert for follower additions
        if set_additions:
            print(f"{YELLOW}Exploring {len(set_additions)} New Profile(s) [!]{RESET}\n")
            # wait 1 second
            await asyncio.sleep(1)
            # loop set of follower additions
            for owner in set_additions:
                # print api info or throw exception if threshold exceeded
                client.check_user_api_info()
                # follow owner
                await client.update_following_status(owner=owner, follow_owner=True)
                # get owner's top-4 recent repos
                set_repos = await client.get_owner_top_repos(owner=owner)
                # star each repo
                for repo in set_repos:
                    await client.update_stargazing_status(owner=owner, repo=repo, star_repo=True)
                # save owner to EXPLORED_LOGINS file
                write_owner_to_file(owner=owner)

        # show alert for follower deletions
        if set_deletions:
            print(f"{YELLOW}Removing {len(set_deletions)} Stale Profile(s) [!]{RESET}\n")
            # wait 1 second
            await asyncio.sleep(1)
            # loop set of follower deletions
            for owner in set_deletions:
                # unfollow owner
                await client.update_following_status(owner=owner, follow_owner=False)
                # delete owner from EXPLORED_LOGINS file
                delete_owner_from_file(owner=owner)

    # catch exceptions
    except Exception as e:
        print(f"{RED}{e} [X]{RESET}\n")

    # close session
    finally:
        client.print_user_api_info()
        print(f"{YELLOW}Closing Program [!]{RESET}")
        await client.close()


if __name__ == "__main__":
    asyncio.run(follow_n_star())