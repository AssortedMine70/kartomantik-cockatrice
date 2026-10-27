# KartomaintiK for Cockatrice

Bring **KartomantiK** to Cockatrice using its custom sets feature.

## How to Setup

### STEP 1 - Obtain the custom set

* **Option 1 (Recommended):** Download `kartomantik_database.zip` directly from the [GitHub Releases](https://github.com/AssortedMine70/kartomantik-cockatrice/releases) page.
* **Option 2:** Clone the repository and run the generation script:
  ```bash
  python main.py

**IMPORTANT NOTE:** the generation is based on a non-documented API endpoint from the [KartomantiK official website](https://www.kartomantik.com/). If they change their response schema in the future, the script or generation might break.

### STEP 2 - Import the custom set in Cockatrice

1. Unzip `kartomantik_database.zip`.
1. Open **Cockatrice**.
1. From the top menu, select **Card Database → Add custom sets/cards**.
1. Choose your card database file (`kartomantik_database.xml`).
1. From the top menu, select **Card Database → Open custom image folder**.
1. Drag in the images folters (`images/{SetName}` folders).

## Decks

I've also included in the `/decks` directory a transcription of KartomantiK suggested decks in their [Rulebook PDF](https://www.kartomantik.com/files/it/Regole_kartomantik.pdf), ready to be imported in Cockatrice.

## Disclamer
*This is an unofficial fan project and is not affiliated with, endorsed, or sponsored by KartomantiK. All card names, text, and artwork are the property of their respective owners.*