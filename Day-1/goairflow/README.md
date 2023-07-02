### Structure

Overall, this repository is structured as follows:

```
├── chapter01                # Code examples for Chapter 1.
├── chapter02                # Code examples for Chapter 2.
├── ...
├── .pre-commit-config.yaml  # Pre-commit config for the CI.
├── README.md                # This readme.
└── requirements.txt         # CI dependencies.
```

The *chapterXX* directories contain the code examples for each specific Chapter.

Code for each Chapter is generally structured something like follows:

```
├── dags                  # Airflow DAG examples (+ other code).
├── docker-compose.yml    # Docker-compose file used for running the Chapter's containers.
└── readme.md             # Readme with Chapter-specific details, if any.
```