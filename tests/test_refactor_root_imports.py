"""Tests for the one-off root import migration utility."""

import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "refactor_root_imports.py"
SPEC = spec_from_file_location("refactor_root_imports", SCRIPT)
assert SPEC and SPEC.loader
migration = module_from_spec(SPEC)
sys.modules[SPEC.name] = migration
SPEC.loader.exec_module(migration)


def make_package(tmp_path: Path) -> Path:
    package = tmp_path / "src" / "typhoon_vn"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    return package


def test_rewrites_from_import_relative_to_importing_module(tmp_path: Path) -> None:
    package = make_package(tmp_path)
    module = package / "training" / "legacy_train.py"
    module.parent.mkdir()
    source = (
        "from data_loader import TyphoonDataset\n"
        "from model import TropicalCycloneLSTM\n"
        "from share_func import normalize_df\n"
    )
    rewritten, diagnostics = migration.rewrite_source(source, module, package)
    assert diagnostics == []
    assert "from ..datasets.legacy_dataset import TyphoonDataset" in rewritten
    assert "from ..models.legacy_lstm import TropicalCycloneLSTM" in rewritten
    assert "from ..features.legacy_preprocessing import normalize_df" in rewritten


def test_rewrites_plain_import_without_changing_bound_name(tmp_path: Path) -> None:
    package = make_package(tmp_path)
    module = package / "inference" / "legacy_predict.py"
    module.parent.mkdir()
    rewritten, diagnostics = migration.rewrite_source(
        "import draw_map\nimport model as old_model\n", module, package
    )
    assert diagnostics == []
    assert "from ..visualization import track_map as draw_map" in rewritten
    assert "from ..models import legacy_lstm as old_model" in rewritten


def test_check_and_write_modes(tmp_path: Path) -> None:
    package = make_package(tmp_path)
    module = package / "cli.py"
    module.write_text("from predict import predict\n", encoding="utf-8")
    assert migration.run(package, write=False, check=True) == 1
    assert module.read_text(encoding="utf-8") == "from predict import predict\n"
    assert migration.run(package, write=True, check=False) == 0
    assert module.read_text(encoding="utf-8") == (
        "from .inference.legacy_predict import predict\n"
    )
    assert migration.run(package, write=False, check=True) == 0
