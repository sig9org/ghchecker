import configparser
import os

from dotenv import load_dotenv
from github import Auth, Github
from notify_to_cisco_webex.notify_to_cisco_webex import Webex, WebexConfig


def main():
    load_dotenv()
    ghtoken = os.environ.get("GITHUB_TOKEN")
    if ghtoken is None or ghtoken == "":
        print("Without GitHub Token.")
        gh = Github()
    else:
        print("With GitHub Token.")
        gh = Github(auth=Auth.Token(ghtoken))
        gh.get_user().login
    is_update = False
    msg = ""
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    for section in cfg.sections():
        repo = cfg[section]["repo"]
        oldver = cfg[section]["version"]

        releases = gh.get_repo(repo).get_releases()
        if releases.totalCount > 0:
            newver = releases[0].tag_name
            if oldver != newver:
                is_update = True
                msg += f"### [{section}](https://github.com/{repo})\n- [{oldver}](https://github.com/{repo}/releases/tag/{oldver}) ---> [{newver}](https://github.com/{repo}/releases/tag/{newver})\n"
                cfg.set(section, "version", newver)

    if is_update:
        with open("config.ini", "w") as f:
            cfg.write(f)
        try:
            wcfg = WebexConfig(
                token=os.environ.get("WEBEX_TOKEN"),
                dst=os.environ.get("WEBEX_DST"),
                msg_format="markdown",
                timeout=10.0,
                insecure=False,
                verbose=False,
                proxy=None,
            )
            Webex(wcfg).send(message=msg)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
