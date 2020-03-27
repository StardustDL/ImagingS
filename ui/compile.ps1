$uifiles = Get-ChildItem . -Include *.ui -Recurse

$initFile = "../src/ui/__init__.py"
$uis = @()

Write-Output "# Generated by UI compiler" | Out-File -Encoding "UTF8" $initFile

foreach ($ui in $uifiles) {
    $name = $ui.BaseName
    Write-Output "Compiling ${name}..."
    python -m PyQt5.uic.pyuic ./${name}.ui -o ../src/ui/_ui_${name}.py
    $uis += "${name}"
    Write-Output "from ._ui_${name} import Ui_${name} as ${name}" | Out-File -Encoding "UTF8" -Append $initFile
}

Write-Output "Generating UI module..."

Write-Output "" | Out-File -Encoding "UTF8" -Append $initFile
Write-Output "__all__ = (" | Out-File -Encoding "UTF8" -Append $initFile

foreach ($ui in $uis) {
    Write-Output "    ""${ui}""," | Out-File -Encoding "UTF8" -Append $initFile
}

Write-Output ")" | Out-File -Encoding "UTF8" -Append $initFile