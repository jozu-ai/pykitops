# Contributing Guide

* [Ways to Contribute](#ways-to-contribute)
* [Development Environment Setup](#development-environment-setup)
* [Pull Request Lifecycle](#pull-request-lifecycle)
* [Sign off on Commits](#sign-off-on-commits)
* [Ask for Help](#ask-for-help)

Welcome! We are so excited that you want to contribute to our project! 💖

As you get started, you are in the best position to give us feedback on areas of our project that we need help with including:

* Problems found during setting up a new developer environment
* Gaps in our guides or documentation
* Bugs in our tools and automation scripts

If anything doesn't make sense, or doesn't work when you try it, please open a bug report and let us know!

## Ways to Contribute

We welcome many different types of contributions including:

* [New features](https://github.com/kitops-ml/pykitops/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)
* [Bug fixes](https://github.com/kitops-ml/pykitops/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)
* [Documentation](https://github.com/kitops-ml/pykitops/issues?q=is%3Aopen+is%3Aissue+label%3Adocumentation)
* [Builds and CI/CD](https://github.com/kitops-ml/pykitops/issues?q=is%3Aopen+is%3Aissue+label%3Abuild)
* Release management
* Issue triage
* Answering questions on Discord, or the mailing list
* Communications, social media, blog posts, or other marketing

If you think there's something else you can help with please contact us in the [#general channel of our Discord server](https://discord.gg/Tapeh8agYy) or during our [office hours meeting](https://github.com/jozu-ai/kitops/blob/main/GOVERNANCE.md#-meetings) and let's discuss how we can work together.

## Development Environment Setup

### Prerequisites

* Python: At least the minimum support version of Python.
* Poetry: Latest version. Installation instructions are available at https://python-poetry.org/docs/#installation.
* Git: Version control system for cloning the repository and managing code changes. Installation instructions are available at https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.

### Setting up the project

1. Clone the Repository: Clone the PyKitOps source code to your local machine:

    ```shell
    git clone https://github.com/kitops-ml/pykitops.git
    cd pykitops
    ```

1. Install Project Dependencies: Inside the project directory, fetch and install the project's dependencies using the poetry command:

    ```shell
    poetry install --with=dev
    ```

1. Run test

    ```shell
    poetry run pytest
    ```

1. Run ruff: Execute the built CLI to see all available commands:

    ```shell
    poetry run ruff format
    poetry run ruff check
    ```

1. Updating Dependencies: If you add or update dependencies:

    ```shell
    poetry add <dependency>
    ```
    
    or for development dependencies:
    ```shell
    poetry add --group dev <dependency>
    ```

## Reporting Bugs/Feature Requests

We use the project's GitHub issue tracker to report bugs or suggest features/enhancements.

Before creating an issue, please check [existing open](https://github.com/kitops-ml/pykitops/issuess) or [recently closed](https://github.com/kitops-ml/pykitops/issues?utf8=%E2%9C%93&q=is%3Aissue%20is%3Aclosed%20) issues to make sure somebody else hasn't already 
reported the issue. Please try to include as much information as you can. Details like these are incredibly useful:

* A series of steps to reproduce
* The version of our code being used
* Any modifications you've made relevant to the bug

## Pull Request Lifecycle

Pull requests are often called a "PR". KitOps generally follows the standard [GitHub pull request process](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).

Before sending us a pull request, please ensure that:

1. You are working against the latest source on the *main* branch.
2. You check existing open, and recently merged, pull requests to make sure someone else hasn't addressed the problem already.
3. You open an issue to discuss any significant work - we would hate for your time to be wasted.
4. PR is merged submitted to merge into *main* branch.

To send us a pull request, please:

1. Fork the repository.
2. Modify the source; please focus on the specific change you are contributing.
3. Ensure local tests pass.
4. Commit to your fork using clear commit messages. Don't forget to [sign off on your commits](#sign-off-on-commits)!
5. Send us a pull request, answering any default questions in the pull request interface.
6. Pay attention to any automated CI failures reported in the pull request, and stay involved in the conversation.

GitHub provides additional document on [forking a repository](https://help.github.com/articles/fork-a-repo/) and 
[creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## Sign off on Commits

Licensing is important to open source projects. It provides some assurances that the software will continue to be available based under the terms that the author(s) desired. We require that contributors sign off on commits submitted to our project's repositories. The [Developer Certificate of Origin (DCO)](https://probot.github.io/apps/dco/) is a way to certify that you wrote and have the right to contribute the code you are submitting to the project.

You sign-off by adding the following to your commit messages. Your sign-off must match the git user and email associated with the commit. Your commit message should be followed by:

    Signed-off-by: Your Name <your.name@example.com>

Git has a `-s` command line option to do this automatically:

    git commit -s -m 'This is my commit message'

If you forgot to do this and have not yet pushed your changes to the remote
repository, you can amend your commit with the sign-off by running

    git commit --amend -s

## Ask for Help

The best way to reach us with a question when contributing is to ask on:

* The original github issue
* Our [Discord server](https://discord.gg/Tapeh8agYy)
* At our [office hours meeting](https://github.com/jozu-ai/kitops/blob/main/GOVERNANCE.md#-meetings)