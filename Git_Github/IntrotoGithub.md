# Introduction to GitHub

## 1. Overview & Core Pillars

GitHub is an AI-powered cloud developer platform built on top of **Git**, providing collaboration, automation, security, and scalability tools.

### Core Pillars
- **AI:** Powered by Copilot, Copilot Chat, Copilot Agents, and AI-driven PR summaries.
- **Collaboration:** Tools like Repositories, Issues, Pull Requests, and Discussions streamline team workflows.
- **Productivity:** Built-in CI/CD via GitHub Actions automates repetitive processes.
- **Security:** Integrated tools including CodeQL, Secret Scanning, Dependabot, and Security Overview.
- **Scale:** Hosts over 100M developers and 420M+ repositories worldwide.

---

## 2. Repositories, Gists, Wikis & Pages

### Core Features
- **Repository:** Central location containing project files, folders, and complete revision history.
  - *Visibility:* **Public** (accessible to all) or **Private** (restricted access).
  - *Cloning:* `git clone <repository-url>` creates a local copy.
  - *Subdirectories:* Created in GitHub web interface by typing `/` (e.g., `folder/file.md`).

- **Gists:** Lightweight mini Git repositories for sharing code snippets or configuration files.
  - *Public Gists:* Searchable and indexed.
  - *Secret Gists:* Unlisted; accessible via URL (never store passwords, API keys, or confidential data).

- **Wikis:** Section built into repositories for hosting long-form project documentation and architectural overviews.

- **GitHub Pages:** Static site hosting service publishing directly from HTML/CSS/JS or Markdown files in a designated branch or folder (e.g., `/docs`).

---

## 3. GitHub Flow vs. Git Flow

### GitHub Flow (Lightweight & Continuous Delivery)
1. **Create Branch:** Branch off `main` to isolate work (`git checkout -b feature-branch`).
2. **Make Commits:** Track modifications with clear commit messages.
3. **Open Pull Request (PR):** Propose changes, invite feedback, and start team review.
4. **Review & Iterate:** Address feedback with additional commits.
5. **Merge PR:** Integrate feature branch into `main` after approval.
6. **Delete Branch:** Clean up outdated branches.

### Git Flow (Structured & Release-Driven)
- **`master`/`main`:** Always production-ready code.
- **`develop`:** Integration branch for upcoming releases.
- **`feature/*`:** Temporary branches for new functionality, merged into `develop`.
- **`release/*`:** Prepares a new release version for testing and minor fixes before merging into `main` and `develop`.
- **`hotfix/*`:** Emergency patches branched from `main` and merged into both `main` and `develop`.

---

## 4. Collaborative Tools: Issues vs. Discussions

| Feature | Primary Purpose | Best Use Cases |
| :--- | :--- | :--- |
| **Issues** | Actionable task management | Bug reports, feature tasks, specific work items, milestones. |
| **Discussions** | Open forum communication | Community Q&A, announcements, general feedback, brainstorming ideas. |

### Key Workflows
- **Discussion Answers:** In Q&A discussions, maintainers or OP can mark a comment as **Marked as Answer**.
- **Convert Discussion to Issue:** Useful when open discussion turns into actionable development tasks.
- **Pinned Discussions:** Important threads can be pinned to top of Discussions tab.

---

## 5. Notification & Subscription Management

- **Watch Options:** `Watching` (all activity), `Not watching` (only participating/mentions), `Ignore`, or `Custom`.
- **Delivery Channels:** Email, Web dashboard, or GitHub Mobile app.
- **Search Qualifiers:** `mentions:<username>` searches for items where a user was @mentioned.

---

## 6. Knowledge Check / Self-Assessment

### Q1: What is the advantage of using GitHub Discussions over Issues for announcements?
- [x] **Discussions allow for open-ended conversations and engagement beyond specific tasks.**
- [ ] Discussions require less permissions to access.
- [ ] Discussions are automatically linked to pull requests.

### Q2: What role do commits play in the GitHub flow?
- [x] **They track changes and provide a history of modifications.**
- [ ] They create new branches automatically.
- [ ] They merge branches automatically.

### Q3: Which describes a unique feature of managing notifications on GitHub?
- [ ] Notifications are automatically enabled for all visited repos.
- [ ] You can only receive notifications via email.
- [x] **You can subscribe to notifications for a specific issue or pull request.**

### Q4: How do GitHub Issues and Discussions complement each other?
- [ ] Discussions track bugs; Issues are for announcements.
- [ ] Both are used interchangeably.
- [x] **Issues track tasks and bugs, while Discussions serve broader conversations.**

### Q5: A team member reports merged changes aren't visible in main. What is a likely reason?
- [x] **The merge was performed into a different branch, not main.**
- [ ] Repository settings forbid merging to main.
- [ ] The branch was deleted before merging.

### Q6: When should a GitHub issue be used instead of a discussion?
- [ ] When seeking open-ended feedback on project ideas.
- [x] **When tracking specific tasks or bugs related to a project.**
- [ ] When announcing project milestones to the team.

### Q7: What characteristic makes GitHub Discussions suitable for community engagement?
- [x] **Discussions can be categorized and organized for different conversation topics.**
- [ ] Discussions are designed for task management.
- [ ] Discussions automatically track code changes.

### Q8: What sequence of actions ensures smooth integration of a feature branch into main?
- [ ] Commit to main, then create a pull request.
- [ ] Merge branch directly, then open a pull request.
- [x] **Create a pull request, review the pull request, merge the branch.**

### Q9: How do you specify subdirectories when adding a new file in the GitHub UI?
- [ ] Create each directory individually before adding the file.
- [ ] Use the 'Add directory' command in the GitHub UI.
- [x] **Use the `/` directory separator in the file name field.**