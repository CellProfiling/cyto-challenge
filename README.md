# Submission deadline

- The leader board and presentation submissions will close 24hrs prior to presentations (June 13 15:30
EST).
- Please note that results submission may need some time, so make your first submission well ahead of the deadline to be on the safe side.


# Disclaimer

By submitting a solution to any of these challenges, you agree to the following:

- Your username can be published alongside your results publicly available on our webpages, https://cellprofiling.github.io/cyto-challenge/, http://proteinatlas.org/, and http://cytoconference.org.
- Your username and results can be used during our workshop at the Cyto conference 2017 as well as in any conference proceedings for the Cyto conference 2017.
- Your anonymized results can be used in future publications.
- Your author list, including potential affiliations and emails, will be kept on record privately with your results until after the winners of the competition have been announced.


# Leaderboard

## Challenge 2

| Team   |   F1 score |   Highest F1 Score |   Precision |   Recall |
|:-------|-----------:|-------------------:|------------:|---------:|
| Dapid  |       0.21 |               0.21 |       0.305 |    0.511 |

## Challenge 3

There is a problem with the uploaded image test set for challenge 3. We are working on a fix.

| Team   | F1 score            | Highest F1 Score   | Precision           | Recall              |
|:-------|:--------------------|:-------------------|:--------------------|:--------------------|
| Dapid  | auto-scoring failed | N/A                | auto-scoring failed | auto-scoring failed |

## Challenge test

| Team           |   F1 score |   Highest F1 Score |   Precision |   Recall |
|:---------------|-----------:|-------------------:|------------:|---------:|
| MartinHjelmare |       0.26 |               0.65 |         0.3 |    0.233 |

Data provided by the [Human Protein Atlas](http://proteinatlas.org)

Challenge hosted by [cytoconference.org](http://cytoconference.org/2017/Program/Image-Analysis-Challenge.aspx)

# Generating results for submission

We will only score challenge 2, 3 and 4. But you are welcome to submit results for challenge 1 and the bonus challenge too. To do so, please send a short presentation (5 slides or less) to the cyto-challenge [email address](mailto:cytochallenge2017@gmail.com).

- Go to the challenge data set [download page](http://www.proteinatlas.org/CYTO_challenge2017/) on the protein atlas. There you will now find the image test sets that contain the withheld images that you should use to generate your results for each challenge, using your trained model.
- You only need to download two image test sets:
  - major13_test.tar should be used for generating results for challenge 2, 4 and bonus.
  - rare_events_test.tar should be used for generating results for challenge 3.

# Result submission instructions

Follow these instructions to submit your challenge results.

- Follow the link to our repo by clicking "View on GitHub" above.
- Fork the repo on GitHub, by clicking the "fork" button.
- Clone your fork.

```
git clone https://github.com/YOUR_GIT_USERNAME/cyto-challenge.git
```

- Go to the cloned directory.

```
cd cyto-challenge
```

- Set our repo as `upstream` remote. Your fork should already be the `origin` remote.

```
git remote add upstream https://github.com/CellProfiling/cyto-challenge.git
```

- Check your remotes.

```
git remote -v
```

- Checkout a new branch based on `master` branch.

```
git checkout -b awesome-solution master
```

- Add the csv files from your submission to the respective challenge subdirectories in the `submissions` directory.
  - A submission csv file for a challenge must be named `[YOUR_GIT_USERNAME]_[CHALLENGE].csv`, eg `MartinHjelmare_2.csv`.
  - Each challenge must have its own subdirectory in the `submissions` subdirectory, eg challenge 2 should have a directory named `2`, challenge 3 should have a directory named `3` etc. All teams that try to solve challenge 2 should put their solutions in the challenge subdirectory named `2`.

```
cp ~/my_experiments/YOUR_GIT_USERNAME_2.csv ./submissions/2/
```

- Add a team info csv file in the `teams` directory. The team info csv file should have three columns, `author`, `affiliation`, `contact info`. Enter all the info for all team members in this file. We will not display this info on the leader board page. We will only keep this info to be able to contact the teams during and after the challenge. You will encrypt the csv file in the next step, so your info will not be public. We have added an unencrypted team info csv file (`MartinHjelmare_team.csv`), as an example in the `teams` directory.

| author          | affiliation                                              | contact info        |
|-----------------|----------------------------------------------------------|---------------------|
| Martin Hjelmare | Royal Institute of Technology SE-171 21 Stockholm Sweden | example@example.com |

```
cp ~/my_experiments/YOUR_GIT_USERNAME_team.csv ./teams/
```

- Encrypt each submitted csv file with gpg using our public pgp key. Since you don't want to give your competitors a free ride, all submissions must be encrypted. We have included a bash script that does this for you. This should work in Linux and Mac environments. You must have `gpg` installed. We have also added a `.gitignore` file to the repo, to avoid unencrypted csv files from being committed by mistake. The script will encrypt the contents of your csv file and create a new file with the `.gpg` extension in the same directory as your csv file. Your csv file will remain in the directory.

```
./gpg/encrypt.sh ./submissions/2/YOUR_GIT_USERNAME_2.csv
./gpg/encrypt.sh ./teams/YOUR_GIT_USERNAME_team.csv
```

- Add your encrypted csv files and commit your changes. Write at minimum a short commit message. If you want to write something longer, you can call `commit` without the `-m` option which should open your preferred editor instead. If you write something longer, try to keep the header of the commit message within 50 characters and the body within 72 characters per line. A blank line should separate the header from the body of the commit message. Markdown is cool.

```
git add -A
git commit -m "Add submission for challenge 2"
```

- Push your local changes to your fork.

```
git push origin HEAD
```

- [Create a pull request at GitHub](https://help.github.com/articles/creating-a-pull-request/) to our `cyto-challenge` repository and target the `master` branch with your changes.
- If the Travis build turns green :white_check_mark:, we will merge your pull request. This should automatically update the leader board on the site. If the Travis build fails, you should look at the build logs and see what made the build fail. You are only allowed to change files that are named `[YOUR_GIT_USERNAME]_[CHALLENGE].csv.gpg` or `[YOUR_GIT_USERNAME]_team.csv.gpg`. Any other changes will fail the pull request build. Changing source files to cheat would lead to very bad Karma. Don't do that. :wink: After the pull request is merged, Travis will build again and this time score your submission. If the auto-scorer can't score your csv file, your row in the leader board will contain a message about this when the site has updated.
- If you want to update your submission or try new challenges, make sure you pull the latest version from our repo, ie the `upstream` remote, before making your changes. You can also delete your old solution branch.

```
git checkout master
git branch -D awesome-solution
git pull upstream master
git checkout -b another-awesome-solution master
```
