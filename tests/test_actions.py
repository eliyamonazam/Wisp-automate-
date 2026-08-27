from pathlib import Path

from wisp.actions.file_ops import MoveByExtensionAction


def test_move_by_extension_sorts_into_subfolder(tmp_path: Path) -> None:
    source = tmp_path / "report.pdf"
    source.write_text("dummy content")
    target_dir = tmp_path / "sorted"

    action = MoveByExtensionAction(target=str(target_dir))
    action.run({"path": str(source)})

    moved = target_dir / "pdf" / "report.pdf"
    assert moved.exists()
    assert not source.exists()


def test_move_by_extension_ignores_missing_file(tmp_path: Path) -> None:
    action = MoveByExtensionAction(target=str(tmp_path / "sorted"))
    # Should not raise even though the file doesn't exist.
    action.run({"path": str(tmp_path / "missing.txt")})
