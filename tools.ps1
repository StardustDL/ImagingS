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
            npm install -g pyright
            if (!$?) {
                exit 1
            }
        }
        "clean" {
            Write-Output "Clean generated files.."
            Get-ChildItem -Include .coverage -Recurse | Remove-item
            Get-ChildItem -Include htmlcov -Recurse | Remove-item -Recurse -Force ./htmlcov
            Get-ChildItem -Include .pytest_cache -Recurse | Remove-item -Recurse
            Get-ChildItem -Include __pycache__ -Recurse | Remove-item -Recurse
            Get-ChildItem ./ImagingS/Gui/ui -Exclude .gitignore | Remove-item -Recurse
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
            flake8 . --count --select="E9,F63,F7,F82" --exclude=".svn,CVS,.bzr,.hg,.git,__pycache__,.tox,.eggs,*.egg,_ui_*.py" --show-source --statistics
            if (!$?) {
                exit 1
            }
            # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
            flake8 . --count --ignore="E501,E121,E123,E126,E226,E24,E704,W503,W504" --exclude=".svn,CVS,.bzr,.hg,.git,__pycache__,.tox,.eggs,*.egg,_ui_*.py" --exit-zero --max-complexity=10 --max-line-length=127 --statistics
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
            exit 2
        }
    }
}
else {
    Write-Output "Missing command"
    exit 2
}