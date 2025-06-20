# Problem Set Picker

A random problem generator + zulip message sender for problem sets!

### Developing locally

This project uses uv for dependency management. To start the dev server:

```bash
uv run fastapi dev
```

### Deployments

This project currently uses [disco](https://docs.letsdisco.dev/) to deploy to a raspberry pi. The deployments are handled automatically with push to this repo :) 

### Contributing

1. Create a new problem set in the `problem_sets/` folder.
1. Follow the guidelines in the `problem_sets/problem_set_interface.py`
1. Add the problem set to the `PROBLEM_SET_MAPPING` in `main.py`
1. Optionally, create an endpoint to allow others to generate random problems.