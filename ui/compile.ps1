$uifiles = Get-ChildItem . -Include *.ui -Recurse
foreach ($ui in $uifiles) {
    $name = $ui.BaseName
    python -m PyQt5.uic.pyuic ./${name}.ui -o ../src/ui/${name}.py
}