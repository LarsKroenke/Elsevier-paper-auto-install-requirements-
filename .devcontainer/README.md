# Devcontainer-Setup

Diese Datei dokumentiert die Devcontainer-Konfiguration für dieses Projekt.

## Ziel

Die Funktion bleibt unverändert, aber die Konfiguration ist in wartbare Skripte aufgeteilt.

## Struktur

- `devcontainer.json` enthält die Container-Definition und VS-Code-Customizations.
- `scripts/on-create.sh` installiert die TeX/LaTeX-Abhängigkeiten beim Erstellen des Containers.
- `scripts/post-create.sh` installiert zusätzliche Tools (u. a. Homebrew, Font, Python-Pakete) nach der Erstellung.

## Ausführungsreihenfolge

1. `onCreateCommand` → `bash .devcontainer/scripts/on-create.sh`
2. `postCreateCommand` → `bash .devcontainer/scripts/post-create.sh`

## Anpassungen vornehmen

- Neue Systempakete: in `scripts/on-create.sh` oder `scripts/post-create.sh` ergänzen.
- Neue Python-Pakete: in `scripts/post-create.sh` unter `pip install` ergänzen.
- Editor-/Extension-Einstellungen: in `devcontainer.json` unter `customizations.vscode` ändern.

## Hinweise

- Beide Skripte nutzen `set -euo pipefail` für robustes Fehlerverhalten.
- Skripte sind ausführbar und können bei Bedarf lokal getestet werden:

```bash
bash .devcontainer/scripts/on-create.sh
bash .devcontainer/scripts/post-create.sh
```
