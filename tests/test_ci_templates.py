from pathlib import Path


ROOT = Path(__file__).parent.parent
CI_DIR = ROOT / "examples" / "ci"


def test_ci_template_files_exist():
    assert (CI_DIR / "github-actions-breakpoint.yml").is_file()
    assert (CI_DIR / "run-breakpoint-gate.sh").is_file()


def test_ci_shell_template_is_executable():
    shell_template = CI_DIR / "run-breakpoint-gate.sh"
    assert shell_template.stat().st_mode & 0o111
