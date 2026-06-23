# nyc-taxi-glue

Python Glue scripts for the NYC taxi data pipeline. Scripts are automatically uploaded to S3 on every merge to `dev` (dev environment) or `main` (prod environment).

## What this repo does

- Holds Python scripts that run as AWS Glue Python Shell jobs
- GitHub Actions uploads scripts to S3 when changes under `scripts/` land on `dev` or `main`
- Scripts are referenced by Glue job definitions managed in the [infrastructure repo](https://github.com/ranjanumesh11/nyc-taxi-glue-terraform)

## Repo structure

```
nyc-taxi-glue/
├── scripts/
│   └── yellow_taxi/
│       └── download_yellow_taxi_april_2026.py   # downloads April 2026 yellow taxi parquet
├── iam/
│   └── bootstrap/
│       ├── github-oidc-trust-policy.json        # trust policy for GitHub OIDC role (one-time setup)
│       └── github-deploy-permissions.json       # S3 upload permissions (one-time setup)
└── .github/
    └── workflows/
        └── deploy-scripts.yml                   # uploads scripts/ to S3 on push to dev or main
```

## Branch strategy

```
feature/* ──→ PR ──→ dev ──→ PR ──→ main
                     │               │
                     ▼               ▼
               uploads to          uploads to
               ...-dev bucket      prod bucket
               (verify job works)  (no suffix)
```

- Work on `feature/*` branches
- PR to `dev` — no upload (path filter requires an actual scripts/ change on push)
- Merge to `dev` with script changes → GitHub Actions uploads to dev S3 bucket → run Glue job to verify
- Once verified, PR `dev → main` → merge → uploads to prod S3 bucket

## Environment buckets

| Branch | S3 bucket |
|--------|-----------|
| `dev` | `nyc-taxi-glue-scripts-721559935914-dev` |
| `main` | `nyc-taxi-glue-scripts-721559935914` |

Bucket names are stored as GitHub repository variables (`GLUE_SCRIPTS_BUCKET_DEV`, `GLUE_SCRIPTS_BUCKET_PROD`) — not hardcoded in the workflow.

## Adding a new Glue job script

1. Create your `.py` file under `scripts/<dataset>/`
2. Push to a feature branch, open PR to `dev`
3. Once merged to `dev`, the script lands in the dev S3 bucket automatically
4. Trigger the Glue job in AWS to verify it works end-to-end
5. Open PR `dev → main` to promote to prod

Then add the matching Glue job definition in the infrastructure repo — see [Adding a new Glue job](https://github.com/ranjanumesh11/nyc-taxi-glue-terraform/blob/main/docs/06-adding-a-new-glue-job.md).

## Manual deploy (workflow_dispatch)

The workflow also supports manual triggering from the Actions tab — useful when the script already exists but needs to be re-synced to S3 without changing the file:

```
GitHub → Actions → Deploy Glue Scripts to S3 → Run workflow → pick dev or prod
```

## Infrastructure repo

Glue job definitions, S3 bucket creation, and IAM roles are all managed in:
[nyc-taxi-glue-terraform](https://github.com/ranjanumesh11/nyc-taxi-glue-terraform)

Full setup documentation (architecture, IAM, Terraform Cloud, GitHub Actions) is in that repo's `docs/` folder.

## Quick commands

```bash
# Check what's in the dev scripts bucket
aws s3 ls s3://nyc-taxi-glue-scripts-721559935914-dev/scripts/ --recursive --profile default

# Trigger the Glue job manually (dev)
aws glue start-job-run \
  --job-name "yellow-taxi-april-2026-download-dev" \
  --profile default

# Check job run status
aws glue get-job-runs --job-name "yellow-taxi-april-2026-download-dev" --profile default

# Verify downloaded data in S3
aws s3 ls s3://nyc-taxi-raw-data-721559935914-dev/yellow/2026/04/ --profile default
```
