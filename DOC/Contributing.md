# Contributing to Andromeda

We would love for you to contribute to Andromeda and help make it even better than it is today! As a contributor, here are the guidelines we would like you to follow:

- [Code of Conduct](#coc)
- [Issues and Bugs](#issue)
- [Coding Rules](#rules)
- [Commit Message Guidelines](#commit)

## <a name="coc"></a> Code of Conduct

Please read and follow our [Code of Conduct](Contributing/code_of_donduct.md) before contributing to the project.

## <a name="issue"></a> Found a Bug?

If you find a bug in the source code, you can help us by [submitting an issue](#submit-issue) to our GitHub Repository.
Even better, you can submit a __Pull Request__ with a fix.

## <a name="commit"></a> Commit Message Format

*This specification is inspired by [Commits Convencionales](https://www.conventionalcommits.org/es/v1.0.0/).*

We have very precise rules over how our Git commit messages must be formatted.
This format leads to **easier to read commit history**.

The `header` is mandatory and must conform to the [Commit Message Header](#commit-header) format.

#### <a name="commit"></a>Commit Message Header

```
<type>: <short summary>
  │       │
  │       └─⫸ Summary in present tense. Capitalized.
  │
  └─⫸ Commit Type: DOC|Feat|Fix|Sec|refactor|Init|Update
```

##### Type

Must be one of the following:


* **Init**: Initial commit
* **Fix**: A bug fix
* **Sec**: A security fix
* **Feat**: A new feature
* **Update**: Update to existing code
* **DOC**: Documentation only changes
* **refactor**: A code change that neither fixes a bug nor adds a feature

### <a name="submit-issue"></a> Submitting an Issue

Before you submit an issue, please search the issue tracker. An issue for your problem might already exist and the discussion might inform you of workarounds readily available.

We want to fix all the issues as soon as possible, but before fixing a bug, we need to reproduce and confirm it.
In order to reproduce bugs, we require that you provide a minimal reproduction.
Having a minimal reproducible scenario gives us a wealth of important information without going back and forth to you with additional questions.

A minimal reproduction allows us to quickly confirm a bug (or point out a coding problem) as well as confirm that we are fixing the right problem.

We require a minimal reproduction to save time and ultimately be able to fix more bugs.
Often, developers find coding problems themselves while preparing a minimal reproduction.
We understand that sometimes it might be hard to extract essential bits of code from a larger codebase but we really need to isolate the problem before we can fix it.

Unfortunately, we are not able to investigate / fix bugs without a minimal reproduction, so if we don't hear back from you, we are going to close an issue that doesn't have enough info to be reproduced.

The minimum information we need is a description of the problem and the __andromeda__ log, if you have more information we will use it to help you reproduce the problem.

### <a name="submit-pr"></a> Submitting a Pull Request (PR)

Before you submit your Pull Request (PR) consider the following guidelines:

1. Search [GitHub](https://github.com/DiegoDG-01/Andromeda-Whatsapp_BOT/pulls) for an open or closed PR that relates to your submission.
   You don't want to duplicate existing efforts.

2. Be sure that an issue describes the problem you're fixing, or documents the design for the feature you'd like to add.
   Discussing the design upfront helps to ensure that we're ready to accept your work.

3. [Fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) the andromeda repo.

4. In your forked repository, make your changes in a new git branch:

     ```shell
     git checkout -b my-fix-branch main
     ```

5. Create your patch.

6. Follow our [Coding Rules](Contributing/coding_rules.md).

7. Commit your changes using a descriptive commit message that follows our [commit message conventions](#commit).
     ```shell
     git commit -m "Feat: Add a new feature"
     ```
   
8. Push your branch to GitHub:

   ```shell
   git push origin my-fix-branch
   ```

9. In GitHub, send a pull request.

### Reviewing a Pull Request

We reserve the right not to accept pull requests from community members who haven't been good citizens of the community. Such behavior includes not following the [Code of conduct](/DOC/Contributing/code_of_donduct.md).

#### Addressing review feedback

If we ask for changes via code reviews then:

1. Make the required updates to the code.

2. Create a fixup commit and push to your GitHub repository (this will update your Pull Request):

    ```shell
    git commit --all --fixup HEAD
    git push
    ```

That's it! Thank you for your contribution!


##### Updating the commit message

A reviewer might often suggest changes to a commit message (for example, to add more context for a change or adhere to our [commit message guidelines](#commit)).
In order to update the commit message of the last commit on your branch:

1. Check out your branch:

    ```shell
    git checkout my-fix-branch
    ```

2. Amend the last commit and modify the commit message:

    ```shell
    git commit --amend
    ```

3. Push to your GitHub repository:

    ```shell
    git push --force-with-lease
    ```

> NOTE:<br />
> If you need to update the commit message of an earlier commit, you can use `git rebase` in interactive mode.
> See the [git docs](https://git-scm.com/docs/git-rebase#_interactive_mode) for more details.


#### After your pull request is merged

After your pull request is merged, you can safely delete your branch and pull the changes from the main (upstream) repository:

* Delete the remote branch on GitHub either through the GitHub web UI or your local shell as follows:

    ```shell
    git push origin --delete my-fix-branch
    ```

* Check out the main branch:

    ```shell
    git checkout main -f
    ```

* Delete the local branch:

    ```shell
    git branch -D my-fix-branch
    ```

* Update your local `main` with the latest upstream version:

    ```shell
    git pull --ff upstream main
    ```

## Information

This file is based on the contribution file of the angular repository.