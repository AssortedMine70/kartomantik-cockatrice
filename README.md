# KartomaintiK for Cockatrice

Bring **KartomantiK** to Cockatrice using its custom sets feature.

## How to Setup

* **Option 1 (Recommended):** Download `kartomantik_database.xml` directly from the [GitHub Releases](https://github.com/AssortedMine70/kartomantik-cockatrice/releases) page.
* **Option 2:** Clone the repository and run the generation script:
  ```bash
  python main.py

**IMPORTANT NOTE:** the generation is based on a non-documented API endpoint from the [KartomantiK official website](https://www.kartomantik.com/). If they change their response schema in the future, the script or generation might break.

### STEP 2 - Import the custom set in Cockatrice

1. Open **Cockatrice**.
2. From the top menu, select **Card Database → Add custom sets/cards**.
3. Choose your card database file (`kartomantik_database.xml`).

You shouldn't need to add **Custom Card Images** because they're already embedded in the `.xml`.

**IMPORTANT NOTE:** You do not need to configure custom card images manually because they are already embedded directly within the XML file. However, image links may occasionally break if the host changes.

## Decks

I've also included in the `/decks` directory a transcription of KartomantiK suggested decks in their [Rulebook PDF](https://www.kartomantik.com/files/it/Regole_kartomantik.pdf), ready to be imported in Cockatrice.

## Disclamer
*This is an unofficial fan project and is not affiliated with, endorsed, or sponsored by KartomantiK. All card names, text, and artwork are the property of their respective owners.*