# Beekeeper-Monitoring: Vollständige Imker-KI

**KI-App für Echtzeit-Erkennung von 6 Bedrohungen: Hornisse, Varroa, Drohnenbrut, Pollenmangel, Schwarm, Königin.**

## Funktionen
- **Registrierung**: E-Mail + Nummer (lokal, anonym).
- **Echtzeit-KI**: YOLOv8n im Browser.
- **SMS-Alarm**: Per E-Mail-to-SMS (kostenlos).
- **Dark Mode**: Bordeaux-Rot Header.
- **Logs**: Export als JSON.
- **Offline-PWA**: Installierbar.

## Registrierungs-Anleitung
1. App öffnen → E-Mail eingeben (optional) → "Weiter".
2. Handynummer (+49...) eingeben → "Speichern".
3. Daten bleiben lokal – 100% anonym.

## Bau-Anleitung (Raspberry Pi)
1. **Hardware**: Pi 4, Arducam-Kamera, 5V-Netzteil.
2. **Setup**: `sudo apt update; pip install ultralytics`.
3. **Training**: `python src/train_multimodal.py` (Kaggle-Dataset).
4. **Start**: `python src/app.py` – Alarme per SMS.

## Nutzungs-Anleitung
1. App öffnen → Registrierung (einmalig).
2. "Kamera starten" – richte auf Stock.
3. Rote Box + SMS bei Bedrohung.
4. "Logs exportieren" für Reports.
5. Install als App (Chrome/Safari).

## Installation
- Repo fork/clone.
- GH Pages: Settings > Pages > main /docs.

Made with ❤️ für Imker – 100% kostenlos.
