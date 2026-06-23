# nyc-taxi-glue

Python Glue scripts for the NYC taxi data pipeline. Scripts are automatically uploaded to S3 on every merge to `main`.

## What this repo does

- Holds Python scripts that run as AWS Glue Python Shell jobs
- GitHub Actions uploads scripts to S3 (`nyc-taxi-glue-scripts-721559935914-dev`) on merge to `main`
- Scripts are referenced by Glue job definitions managed in the infrastructure repo

## Repo structure

```
nyc-taxi-glue/
├── scripts/
│   └── yellow_taxi/
│       └── download_yellow_taxi_april_2026.py   # downloads April 2026 yellow taxi parquet
├── iam/
│   └── bootstrap/
│       ├── github-oidc-trust-policy.json        # trust policy for GitHub OIDC role
│       └── github-deploy-permissions.json       # S3 upload permissions
└── .github/
    └── workflows/
        └── deploy-scripts.yml                   # uploads scripts/ to S3 on merge to main
```

## Branch strategy

```
dev  ──→ PR ──→ main
```

- Work on `dev` or feature branches
- Open a PR to `main` — scripts are validated
- On merge to `main` — GitHub Actions uploads changed scripts to S3 automatically

## Adding a new Glue job script

1. Create your `.py` file under `scripts/<dataset>/`
2. Push to `dev`, open a PR to `main`
3. Once merged, the script lands in S3 automatically
4. Then add the matching Glue job definition in the infrastructure repo (see below)

## Infrastructure repo

Glue job definitions, S3 bucket creation, and IAM roles are all managed in:
[nyc-taxi-glue-terraform](https://github.com/ranjanumesh11/nyc-taxi-glue-terraform)

Full setup documentation (architecture, IAM, Terraform Cloud, GitHub Actions) is in that repo's `docs/` folder.
