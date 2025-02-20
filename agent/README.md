
## Test commands currently working

```bash
uv run pytest libraries/common
uv run pytest libraries/tools
uv run pytest libraries/agents
```

## Command that seems to fix random module missing stuff

```bash
uv sync --all-packages
```

## Reminders

- Took forever how to get imports between libraries and app to work
  + Had to make sure the name of the folder underneath `src` was the package name to import in other python files, i.e. `src/scimaitools` to get `from scimaitools.sql_read_schema import read_schema` to work.
  + Had to make sure all the build system config was there
- pytest still a little squirelly
  + Had to make sure there was an __init__.py file under src/<x> and tests