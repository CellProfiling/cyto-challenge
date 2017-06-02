# Leaderboard

## Challenge test

| Team           |   F1 score |   Precision |   Recall |
|:---------------|-----------:|------------:|---------:|
| MartinHjelmare |       0.65 |        0.75 | 0.583333 |

Data provided by the [Human Protein Atlas](http://proteinatlas.org)

Challenge hosted by [cytoconference.org](http://cytoconference.org/2017/Program/Image-Analysis-Challenge.aspx)

# Result submission instructions

Follow these instructions to submit your challenge results.

- Follow the link to our repo by clicking "View on GitHub" above.
- Fork the repo on GitHub, by clicking the "fork" button.
- Clone your fork.

  ```
  $ git clone https://github.com/YOUR_GIT_USERNAME/cyto-challenge.git
  ```

- Go to the cloned directory.

  ```
  $ cd cyto-challenge
  ```

- Set our repo as `upstream` remote. Your fork should already be the `origin` remote.

  ```
  $ git remote add upstream https://github.com/CellProfiling/cyto-challenge.git
  ```

- Check your remotes.

  ```
  $ git remote -v
  ```

- Checkout a new branch based on `master` branch.

  ```
  $ git checkout -b awesome-solution master
  ```

- Add the csv files from your submission to the respective challenge subdirectories in the `submissions` directory.
  - A submission csv file for a challenge must be named `[YOUR_GIT_USERNAME]_[CHALLENGE].csv`, eg `MartinHjelmare_2.csv`.
  - Each challenge must have its own subdirectory in the `submissions` subdirectory, eg challenge 2 should have a directory named `2`, the bonus challenge should have a directory named `bonus` etc. All teams that try to solve challenge 2 should put their solutions in the challenge subdirectory named `2`.

  ```
  $ cp ~/my_experiments/YOUR_GIT_USERNAME_2.csv ./submissions/2/
  ```

- Encrypt each submitted csv file with gpg using our public pgp key. Since you don't want to give your competitors a free ride, all submissions must be encrypted. We have included a bash script that does this for you. This should work in Linux and Mac environments. You must have `gpg` installed. We have also added an `.gitignore` file to the repo, to avoid unencrypted csv files from being committed by mistake. The script will encrypt the contents of your csv file and create a new file with the `.gpg` extension in the same directory as your csv file. Your csv file will remain in the directory.

  ```
  $ ./gpg/encrypt.sh ./submissions/2/YOUR_GIT_USERNAME_2.csv
  ```

- Add your encrypted csv files and commit your changes. Write at minimum a short commit message. If you want to write something longer, you can call `commit` without the `-m` option which should open your preferred editor instead. If you write something longer, try to keep the header of the commit message within 50 characters and the body within 72 characters per line. A blank line should separate the header from the body of the commit message. Markdown is cool.

  ```
  $ git add -A
  $ git commit -m "Add submission for challenge 2"
  ```

- Push your local changes to your fork.

  ```
  $ git push origin HEAD
  ```

- Create a pull request at GitHub to our `cyto-challenge` repository and target the `master` branch with your changes.
- If the Travis build turns green :white_check_mark:, we will merge your pull request. This should automatically update the leader board on the site. If the Travis build fails, you should look at the build logs and see what made the build fail. You are only allowed to change files that are named `[YOUR_GIT_USERNAME]_[CHALLENGE].csv.gpg`. Any other changes will fail the pull request build. After the pull request is merged, Travis will build again and this time score your submission. If the auto-scorer can't score your csv file, your row in the leader board will contain a message about this when the site has updated.
- If you want to update your submission or try new challenges, make sure you pull the latest version from our repo, ie the `upstream` remote, before making your changes. You can also delete your old solution branch.

  ```
  $ git checkout master
  $ git branch -D awesome-solution
  $ git pull upstream master
  $ git checkout -b another-awesome-solution master
  ```
