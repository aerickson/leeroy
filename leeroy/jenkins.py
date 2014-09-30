# Copyright 2012 litl, LLC.  Licensed under the MIT license.

import logging
import requests

## works with auth tokens from https://wiki.jenkins-ci.org/display/JENKINS/Build+Token+Root+Plugin
build_path = "/buildByToken/buildWithParameters?job={job_name}&token={jenkins_token}" \
    "&GIT_BASE_REPO={git_base_repo}" \
    "&GIT_HEAD_REPO={git_head_repo}" \
    "&GIT_SHA1={git_sha1}" \
    "&GITHUB_URL={github_url}"


def get_jenkins_url(app, repo_config):
    return repo_config.get("jenkins_url", app.config["JENKINS_URL"])


def schedule_build(app, repo_config, head_repo_name, sha, html_url):
    base_repo_name = repo_config["github_repo"]
    job_name = repo_config["jenkins_job_name"]
    token = repo_config.get("jenkins_token", app.config["JENKINS_TOKEN"])

    # TODO: if token == "", then use non-'build token root plugin' url?
    # - currently broken for people who use no auth
    # - could also support basic auth still...

    url = get_jenkins_url(app, repo_config) + \
        build_path.format(job_name=job_name,
                          git_base_repo=base_repo_name,
                          git_head_repo=head_repo_name,
                          git_sha1=sha,
                          github_url=html_url,
                          jenkins_token=token)

    logging.debug("Requesting build from Jenkins: %s", url)
    response = requests.post(url)
    logging.debug("Jenkins responded with status code %s",
                  response.status_code)
