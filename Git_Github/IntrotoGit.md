# Introduction to Git

## 1. Overview & Core Concepts

Version Control Systems (VCS) track changes to files over time, allowing recall of specific versions and parallel collaboration.

### Centralized vs. Distributed VCS
- **Centralized (CVS, SVN, Perforce):** Uses a central server for history. Single point of failure.
- **Distributed (Git):** Every clone contains the complete repository history locally. Enables offline work, redundancy, and flexible workflows.

---

## 2. Key Git Terminology

- **Working Directory:** The directory containing active project files.
- **Staging Area (Index):** A preparation zone where changes are selected before committing.
- **Repository (Repo):** Hidden `.git` folder containing history, objects, and metadata.
- **Hash:** SHA-1 / SHA-256 identifier unique to file contents or commits.
- **Objects:**
  - **Blob:** Ordinary file content.
  - **Tree:** Directory listing (names, hashes, permissions).
  - **Commit:** Snapshot of working tree with author, date, and commit message.
  - **Tag:** Reference marking specific release point.
- **Branch:** Lightweight, named pointer to a commit (`main`, `HEAD`).
- **Remote:** Named link to offsite repository (e.g., `origin`).

---

## 3. Global Configuration & Setup

Set identity prior to committing:

```bash
# Set user name
git config --global user.name "First Last"

# Set user email
git config --global user.email "me@example.com"

# Verify configuration
git config --global --list
```

---

## 4. Essential Git Commands

### Local Workflow
```bash
# Initialize a repository
git init

# View status of working directory & staging
git status

# Stage files
git add <filename>
git add src/*

# Commit staged changes
git commit -m "Descriptive commit message"
```

### Exploring History
```bash
# Detailed commit log
git log

# Concise commit log
git log --oneline

# Graphical representation of branches
git log --all --graph --oneline

# Checkout specific commit or branch
git checkout <commit-hash-or-branch>
git checkout main
```

### Inspecting Differences
```bash
# Difference between working tree and staging
git diff <filename>

# Difference between staging and last commit
git diff --staged <filename>
```

---

## 5. Branching & Merging Strategies

Branches allow isolated feature development without breaking `main`.

### Creating & Managing Branches
```bash
# Create branch
git branch <branch-name>

# Switch branch (older method)
git checkout <branch-name>

# Create & switch (newer command)
git switch -c <branch-name>

# List local branches
git branch --list

# Delete merged branch pointer
git branch -d <branch-name>
```

### Merge Types
1. **Fast-Forward Merge:** Moves target branch pointer forward to HEAD of child branch.
2. **Non-Fast-Forward Merge (`--no-ff`):** Explicitly creates a merge commit to keep branch visualization visible in graph history.
3. **Squash Merge:** Combines all commits from feature branch into a single commit on target branch.

```bash
# Perform explicit non-fast-forward merge
git checkout main
git merge --no-ff <feature-branch> -m "Merge feature branch"
```

---

## 6. Remote Collaboration Concepts

- **Clone:** Copy remote repo locally (`git clone <url>`).
- **Push:** Send local commits to remote (`git push origin <branch>`).
- **Fetch/Pull:** Retrieve updates from remote (`git fetch` / `git pull`).
- **Pull Request (PR):** Propose merging code into shared target repository on platforms like GitHub/GitLab/Gitea.




---

## 7. Knowledge Check / Self-Assessment

### Q1: What is a common use case for a version control system?
- [ ] Deleting earlier versions of a project or file to keep only current data.
- [x] **Making experimental changes to your project in an isolated branch.**
- [ ] Gathering feature requirements and communicating them to stakeholders.

### Q2: Which broader discipline commonly includes version control?
- [ ] Version management software (VMS)
- [ ] Software control management (SCM) system
- [x] **Software configuration management (SCM) system**

### Q3: What is the difference between Git and GitHub?
- [x] **Git lets you work with local branches and push changes to a remote repository. GitHub acts as the remote repository cloud host.**
- [ ] Git runs in the cloud; GitHub is an interface layer.
- [ ] Git is only for individuals; GitHub is for teams.

### Q4: What Git command gives information about how to use Git?
- [ ] `git init`
- [ ] `git status`
- [x] **`git help`** (or `git --help`)

