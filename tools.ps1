$ErrorActionPreference = "Stop"

if ($args.Count -gt 0) {
    switch ($args[0]) {
        "dep" {
            Write-Output "Install dependencies..."
            pip install -r requirements.txt || exit $LASTEXITCODE
        }
        "dep-dev" {
            Write-Output "Install dependencies for development..."
            pip install pytest flake8  || exit $LASTEXITCODE
            pip install pytest-qt pytest-cov  || exit $LASTEXITCODE
            pip install autopep8 isort  || exit $LASTEXITCODE
            pip install PyQt5-stubs  || exit $LASTEXITCODE
            npm install -g pyright  || exit $LASTEXITCODE
        }
        "format" {
            Write-Output "Formatting..."
            isort -rc -ac -s __init__.py -y || exit $LASTEXITCODE
            autopep8 -ir . --list-fixes || exit $LASTEXITCODE
        }
        "clean" {
            Write-Output "Clean generated files.."
            Get-ChildItem -Include .coverage -Recurse | Remove-item
            Get-ChildItem -Include htmlcov -Recurse | Remove-item -Recurse
            Get-ChildItem -Include .pytest_cache -Recurse | Remove-item -Recurse
            Get-ChildItem -Include __pycache__ -Recurse | Remove-item -Recurse
        }
        "clean-ui" {
            Write-Output "Clean generated UI files.."
            Get-ChildItem ./src/ImagingS/Gui/ui -Exclude .gitignore | Remove-item -Recurse
        }
        "gen-ui" {
            Write-Output "Generate UI files..."
            Set-Location src
            python -m ImagingS.Gui.uic || exit $LASTEXITCODE
            Set-Location ..
        }
        "gui" {
            Write-Output "Run GUI..."
            Set-Location src
            python -m ImagingS.Gui || exit $LASTEXITCODE
            Set-Location ..
        }
        "cli" {
            Write-Output "Run CLI..."
            Set-Location src
            python -m ImagingS.Cli || exit $LASTEXITCODE
            Set-Location ..
        }
        "lint" {
            Write-Output "Lint..."
            Write-Output "Flake8 check..."
            # stop the build if there are Python syntax errors or undefined names
            flake8 . --config=tox_fatal.ini
            # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
            flake8 . --exit-zero
            Write-Output "Pyright check..."
            pyright
        }
        "test" {
            Write-Output "Test..."
            pytest --verbose || exit $LASTEXITCODE
        }
        "testcov" {
            Write-Output "Test and coverage..."
            pytest --verbose --cov=. --cov-report=term --cov-report=html || exit $LASTEXITCODE
        }
        "testcov-noui" {
            Write-Output "Test and coverage (without UI)..."
            pytest --verbose --ignore test/gui --cov=. --cov-report=term --cov-report=html || exit $LASTEXITCODE
        }
        Default {
            Write-Output "Unrecognized command"
            exit -1
        }
    }
}
else {
    Write-Output "Missing command"
    exit -1
}