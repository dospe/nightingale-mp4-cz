# Nightingale CZ – pravidla forku

Fork `dospe/nightingale-mp4-cz` vychází z `rzru/nightingale`. Tento soubor drží vše, co je potřeba při slučování s upstreamem: kde fork sahá do souborů upstreamu, jak se slučuje a co je v brandingu jinak. Plán funkcí je v [PLAN_IMPLEMENTACE.md](PLAN_IMPLEMENTACE.md).

## Upstream

| | |
| --- | --- |
| Upstream | `https://github.com/rzru/nightingale.git`, větev `master` |
| Výchozí bod forku | `5963fa8` (5. 11. 2026 shodný s `upstream/master`) |
| Slučování | jednou měsíčně a před každým vydáním |

### Postup slučování

```bash
git remote add upstream https://github.com/rzru/nightingale.git   # jen poprvé v klonu
git fetch upstream master
git checkout -b merge-upstream-$(date +%Y-%m) origin/master
git merge upstream/master
```

1. Konflikty by měly vzniknout jen v souborech z tabulky [Háčky do upstreamu](#háčky-do-upstreamu). Jinde je to znamení, že fork sahá někam, kam nemá. Doplnit ho do tabulky.
2. Když upstream změní loga (`client/src/assets/images/logo*.png`), vzít jeho verzi a obnovit štítek CZ (viz [Ikony a logo](#ikony-a-logo)).
3. Když upstream přidá nové odkazy na `rzru/nightingale` nebo na `~/.nightingale`, rozhodnout podle tabulky [Branding](#branding), jestli je fork přesměruje.
4. Zkontrolovat, že upstream nepřidal do `AppConfig` pole se stejným názvem jako pole forku (kap. [Konfigurace](#nová-konfigurační-pole)).
5. Spustit kontroly: `pnpm --dir client format`, `pnpm --dir client quality`, `pnpm --dir client build`, po změně závislostí `pnpm --dir client audit:rust`.
6. Otevřít PR do `master` forku.

## Branding

Změněno v M0, aby fork běžel vedle upstream Nightingale a nesdílel s ním data ani aktualizace.

| Co | Upstream | Fork | Soubor |
| --- | --- | --- | --- |
| Název aplikace | `Nightingale` | `Nightingale CZ` | `client/src-tauri/tauri.conf.json` (`productName`, titulek okna), `client/index.html` |
| Identifier | `com.rzru.client` | `cz.dospe.nightingale-cz` | `client/src-tauri/tauri.conf.json` |
| Výchozí datová složka | `~/.nightingale` | `~/.nightingale-cz` | `app-core/src/cache.rs` (`default_nightingale_dir`), `assetProtocol.scope` v `tauri.conf.json`, text v `client/src/features/setup/components/setup.tsx` |
| Updater endpoint | `rzru/nightingale/releases` | `dospe/nightingale-mp4-cz/releases` | `client/src-tauri/tauri.conf.json` |
| Updater pubkey | klíč upstreamu | **zatím klíč upstreamu**, nahradit (viz níže) | `client/src-tauri/tauri.conf.json` |
| Vydavatel a copyright | `rzru` | `dospe`, copyright upstreamu zůstává | `client/src-tauri/tauri.conf.json` |
| Odkaz na releases v dialogu aktualizací | upstream | fork | `client/src/features/updates/components/parts.tsx` |
| Název a odkaz na GitHub v dialogu Info | upstream | fork | `client/src/features/menu/components/info.tsx` |
| Logo, ikony, favicon | upstream | upstream + štítek CZ | viz [Ikony a logo](#ikony-a-logo) |
| README | upstream | upozornění na fork, odkazy na releases forku | `README.md` |

Proměnná `NIGHTINGALE_DATA_PATH` a volba `--data` serveru zůstávají beze změny. Nastavená složka má přednost před výchozí `~/.nightingale-cz`.

### Záměrně ponecháno na upstreamu (do M7)

| Místo | Proč zatím ne |
| --- | --- |
| `scripts/install.sh` (`DEFAULT_REPO`), příkaz v `client/src/features/updates/components/views/unsupported.tsx` | Fork zatím nemá releases se serverovými binárkami. Přesměrovat v M7 |
| `docker/`, odkazy na Docker image `razzaru/nightingale` | Vlastní image až v M7 |
| `site/` (web a uživatelská příručka) | Web upstreamu, fork vlastní web nemá |
| `TRANSLATIONS_URL` v `client/src/features/settings/settings.tsx`, `CONTRIBUTING.md` | Překlady a příspěvky do upstreamu |
| Texty „Nightingale“ v překladech a v `client/src-tauri/Info.plist` | Změna by dala konflikty v každém sloučení |
| Názvy crate a binárek, `nightingale.log` | Interní, uživatel je nevidí |

### Podpisový klíč updateru

Dokud je v `tauri.conf.json` veřejný klíč upstreamu, updater forku žádnou aktualizaci nepřijme (releases forku neexistují a upstream podpis by na nich nebyl). Před prvním vydáním (nejpozději v M7):

1. Lokálně, mimo repozitář: `pnpm --dir client tauri signer generate -w ~/.tauri/nightingale-cz.key`.
2. Obsah `~/.tauri/nightingale-cz.key.pub` vložit do `plugins.updater.pubkey` v `client/src-tauri/tauri.conf.json`.
3. Privátní klíč a heslo uložit do GitHub Secrets forku jako `TAURI_SIGNING_PRIVATE_KEY` a `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`. Privátní klíč nikdy necommitovat.
4. Klíč zálohovat. Bez něj už nepůjde vydat aktualizaci pro nainstalované verze.

### Ikony a logo

Loga forku jsou loga upstreamu se štítkem CZ v pravém dolním rohu. Po změně loga v upstreamu:

```bash
python3 scripts/fork/cz_badge.py          # čte originály z upstream/master, potřebuje Pillow a písmo Inter
pnpm --dir client icons                   # přegeneruje client/src-tauri/icons/
```

Skript zapíše `logo_square.png`, `logo.png`, `client/public/favicon.png` a `client/public/apple-touch-icon.png`. Jiné písmo jde zadat přes `--font`.

## Háčky do upstreamu

Jediná místa, kde fork mění soubory upstreamu. Při každém novém háčku doplnit řádek.

| Soubor | Změna | Milník | Stav |
| --- | --- | --- | --- |
| `client/src-tauri/tauri.conf.json` | branding, identifier, updater | M0 | hotovo (pubkey čeká na klíč) |
| `app-core/src/cache.rs` | výchozí datová složka `.nightingale-cz` | M0 | hotovo |
| `client/index.html` | titulek a popis | M0 | hotovo |
| `client/src/features/setup/components/setup.tsx` | cesta k datové složce, `alt` loga | M0 | hotovo |
| `client/src/features/menu/components/info.tsx` | název a odkaz na GitHub | M0 | hotovo |
| `client/src/features/menu/components/sidebar/header.tsx` | `alt` loga | M0 | hotovo |
| `client/src/features/updates/components/parts.tsx` | odkaz na releases | M0 | hotovo |
| `client/src/assets/images/logo*.png`, `client/public/*.png`, `client/src-tauri/icons/` | štítek CZ | M0 | hotovo |
| `README.md` | upozornění na fork, odkazy | M0 | hotovo |
| `CHANGELOG.md` | položky forku v `[Unreleased]` | M0– | průběžně |
| `app-core/src/lib.rs` | `mod downloads; mod lyrics_providers; mod karaoke_export;` + `pub use` | M1–M5 | |
| `app-core/src/config.rs` | nová volitelná pole `AppConfig` | M1–M4 | |
| `app-core/src/analyzer.rs` (`process_song`) | `fetch_lrclib_lyrics` → `lyrics_providers::fetch_auto`, předání jazyka | M2 | |
| `app-core/src/vendor.rs` | `uv_path()`, `download_to_file`, `extract_archive` → `pub(crate)` | M1 | |
| `app-core/src/song_export.rs` | `resolve_stem_files` → `pub(crate)` | M4 | |
| `app-core/Cargo.toml` | nové závislosti | M2, M5 | |
| `app-api/src/lib.rs` | větev `_ =>` v `dispatch` volá `fork::dispatch(...)` | M1 | |
| `client/src/features/sources/hooks/use-source-buttons.ts` | tlačítko „Stáhnout z internetu“ | M1 | |
| `client/src/features/menu/hooks/use-dialog.ts`, `client/src/features/menu/menu.tsx` | režimy dialogů `download`, `karaoke-export` | M1, M3 | |
| `client/src/features/library/components/song-details/song-actions.ts` | akce „Exportovat karaoke…“ | M3 | |
| `client/src/features/lyrics/components/index.tsx` | záložka `czech` | M2 | |
| `client/src/features/settings/settings.tsx`, `components/constants.ts` | sekce Stahování, Zdroje textů, Export | M1–M4 | |
| `client/src/i18n/index.ts` | sloučení katalogů forku, registrace `cs` | M1, M6 | |
| `.github/workflows/release.yml` | artefakty, repozitář, podpisový klíč | M7 | |

## Nová konfigurační pole

Pole forku v `AppConfig` (všechna `Option<…>` se `#[serde(default)]`). Plný seznam s výchozími hodnotami je v kap. 6.1 plánu.

| Pole | Milník | Stav |
| --- | --- | --- |
| – | M0 | M0 žádná pole nepřidává |
