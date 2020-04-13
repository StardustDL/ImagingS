if ($args.Count -gt 0) {
    switch ($args[0]) {
        "dep" {
            Write-Output "Install dependencies..."
            pip install -r requirements.txt
            if (!$?) {
                exit 1
            }
        }
        "dep-dev" {
            Write-Output "Install dependencies for development..."
            pip install pytest flake8
            pip install pytest-qt pytest-cov
            pip install autopep8 isort
            pip install PyQt5-stubs
            npm install -g pyright
            if (!$?) {
                exit 1
            }
        }
        "format" {
            Write-Output "Formatting..."
            isort -rc -ac -s __init__.py -y
            if (!$?) {
                exit 1
            }
            autopep8 -ir . --list-fixes
            if (!$?) {
                exit 1
            }
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
            Get-ChildItem ./ImagingS/Gui/ui -Exclude .gitignore | Remove-item -Recurse
        }
        "gen-ui" {
            Write-Output "Generate UI files..."
            python -m ImagingS.Gui.uic
            if (!$?) {
                exit 1
            }
        }
        "gui" {
            Write-Output "Run GUI..."
            python -m ImagingS.Gui
            if (!$?) {
                exit 1
            }
        }
        "cli" {
            Write-Output "Run CLI..."
            python -m ImagingS.Cli
            if (!$?) {
                exit 1
            }
        }
        "lint" {
            Write-Output "Lint..."
            Write-Output "Flake8 check..."
            # stop the build if there are Python syntax errors or undefined names
            flake8 . --config=tox_fatal.ini
            if (!$?) {
                exit 1
            }
            # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
            flake8 . --exit-zero
            if (!$?) {
                exit 1
            }
            Write-Output "Pyright check..."
            pyright
            if (!$?) {
                exit 1
            }
        }
        "test" {
            Write-Output "Test..."
            pytest --verbose
            if (!$?) {
                exit 1
            }
        }
        "testcov" {
            Write-Output "Test and coverage..."
            pytest --verbose --cov=. --cov-report=term --cov-report=html
            if (!$?) {
                exit 1
            }
        }
        "testcov-noui" {
            Write-Output "Test and coverage (without UI)..."
            pytest --verbose --ignore test/gui --cov=. --cov-report=term --cov-report=html
            if (!$?) {
                exit 1
            }
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