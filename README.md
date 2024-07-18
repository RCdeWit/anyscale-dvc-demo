# Anyscale DVC demo

Demo project to showcase DVC versioning and pipelines to Anyscale.

Steps:
1. Run `python3 src/download_data.py --params params.yaml` to download Lego dataset.
2. `dvc init`, `dvc add data`, and `dvc commit` to show data versioning.
3. Switch branch
4. Update dataset version in params.yaml and `python3 src/download_data.py --params params.yaml` to update dataset.
5. Checkout to old branch and us `dvc checkout` to revert back to older version
6. Show pipeline config, use `dvc dag`
7. Change parameter in second stage, show caching
8. Mentioned experiment tracking (ephemeral commits)