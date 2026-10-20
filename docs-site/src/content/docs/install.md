---
title: Install
description: Install mddocslint from source.
---

## Prerequisites

- Python 3.12+
- [Git](https://git-scm.com/downloads)

mddocslint has no runtime dependencies.

## Installation steps

1. Clone the repository in your desired directory:

   ```
   git clone https://github.com/caseylee-TC/mddocslint.git
   ```

2. Move into the cloned repository:

   ```
   cd mddocslint
   ```

3. Create a virtual environment. This keeps mddocslint separate from your other Python projects:

   ```
   python -m venv .venv
   ```

4. Activate the virtual environment:

   - PowerShell:

     ```
     .venv\Scripts\Activate.ps1
     ```

   - Git Bash:

     ```
     source .venv/Scripts/activate
     ```

   - macOS and Linux:

     ```
     source .venv/bin/activate
     ```

   When the virtual environment is active, your prompt starts with `(.venv)`. You must activate it again in every new terminal before you use `mddocslint`.

5. Install mddocslint:

   ```
   python -m pip install .
   ```

   :::note
   If you plan to change the code and run tests, install mddocslint in editable mode with the `dev` extras (pytest):

   ```
   python -m pip install -e ".[dev]"
   ```

   Editable mode links the installed command to the files in `src/`, so your edits take effect right away. Run the tests with `pytest`.
   :::

6. Check that it is installed:

   ```
   mddocslint --help
   ```

   If you see the usage message, you are ready to go. 
   
   If your shell says it can't find `mddocslint`, the virtual environment is not active. Repeat step 4.

To update mddocslint later, run `git pull` and then `python -m pip install .` again. A regular install is a copy, so it does not pick up changes until you reinstall.

## Next steps

- [Run mddocslint](./usage.md) on a docs folder.
- [Set up the pre-commit hook](./pre-commit.md) to lint before each commit.
