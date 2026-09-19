"""Tests for the multi-horizon dataset and split helpers."""

from typhoon_vn.datasets.synthetic import generate_synthetic_catalogue
from typhoon_vn.datasets.typhoon_dataset import (
    DatasetConfig,
    TyphoonDataset,
    collate_fn,
    split_by_storm_or_year,
)


def test_split_by_storm_avoids_leakage() -> None:
    df = generate_synthetic_catalogue(n_storms=20, seed=1)
    train, val, test = split_by_storm_or_year(
        df, val_ratio=0.2, test_ratio=0.2, by_year=False, random_seed=7
    )
    train_ids = set(train["storm_id"].unique())
    val_ids = set(val["storm_id"].unique())
    test_ids = set(test["storm_id"].unique())
    assert not train_ids & val_ids
    assert not train_ids & test_ids
    assert not val_ids & test_ids


def test_split_by_year_orders_test_most_recent() -> None:
    df = generate_synthetic_catalogue(n_storms=30, start_year=2015, seed=2)
    train, val, test = split_by_storm_or_year(
        df, val_ratio=0.15, test_ratio=0.15, by_year=True
    )
    assert test["timestamp"].dt.year.max() >= val["timestamp"].dt.year.max()
    assert val["timestamp"].dt.year.max() >= train["timestamp"].dt.year.max()


def test_dataset_produces_multi_horizon_targets() -> None:
    df = generate_synthetic_catalogue(n_storms=5, seed=3)
    config = DatasetConfig(input_len=4, horizon=(1, 2, 4, 8, 12))
    ds = TyphoonDataset(df, config=config)
    assert len(ds) > 0
    sample = ds[0]
    assert sample["x"].shape == (config.input_len, ds.n_features)
    assert sample["y_reg"].shape == (len(config.horizon), 2)
    assert sample["y_cls"].shape == (len(config.horizon),)
    assert sample["mask"].sum() == config.input_len


def test_collate_pads_variable_length() -> None:
    df = generate_synthetic_catalogue(n_storms=3, n_fixes=25, seed=4)
    config = DatasetConfig(input_len=4, horizon=(1, 2, 4))
    ds = TyphoonDataset(df, config=config)
    batch = collate_fn([ds[0], ds[1]])
    assert batch["x"].shape[0] == 2
    assert batch["y_reg"].shape == (2, len(config.horizon), 2)
    assert batch["mask"].shape == batch["x"].shape[:2]


def test_dataset_no_samples_when_too_short() -> None:
    df = generate_synthetic_catalogue(n_storms=2, n_fixes=8, seed=5)
    config = DatasetConfig(input_len=6, horizon=(1, 2, 4, 8, 12))
    ds = TyphoonDataset(df, config=config)
    assert len(ds) == 0
