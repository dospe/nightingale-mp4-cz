# Ověření předpokladů – M0

Stav k 5. 11. 2026. Část ověření proběhla v cloudovém prostředí (Linux, bez GPU). To prostředí pouští jen registry balíčků (PyPI, npm, crates.io), archiv Ubuntu a git přístup na GitHub. GitHub Releases, Hugging Face, YouTube, české weby s texty ani servery s buildy ffmpeg z něj dostupné nejsou. Zbylá ověření je nutné spustit lokálně na Windows a macOS podle postupů níže a výsledky dopsat sem.

| # | Ověření | Stav | Výsledek / co chybí |
| --- | --- | --- | --- |
| 1 | Build a kontroly kvality | částečně | Linux: `quality` a `build` zelené. Windows a macOS čekají |
| 2 | libass v přibaleném ffmpeg | čeká | Buildy ffmpeg nejsou z cloudu dostupné |
| 3 | Model zarovnání pro češtinu | částečně | Model potvrzen, pokrytí znaků čeká (Hugging Face) |
| 4 | Detekce jazyka (cs vs. sk/pl/sl) | čeká | Potřebuje testovací sadu a audio |
| 5 | Výkon Whisper modelů | čeká | Potřebuje Windows notebook a Mac |
| 6 | České weby s texty | čeká | Weby nejsou z cloudu dostupné |
| 7 | yt-dlp + Deno | částečně | Volby a balíčky potvrzeny, stažení čeká |

## 1. Build a kontroly

| Platforma | `pnpm --dir client quality` | `pnpm --dir client build` | `cargo desktop dev` (první spuštění, vendor setup) |
| --- | --- | --- | --- |
| Linux x86_64 (Ubuntu 24.04, cloud) | ✅ | ✅ | nelze (bez displeje a bez přístupu ke stahování vendor nástrojů) |
| Windows 11 | | | |
| macOS (Apple Silicon) | | | |

Postup (Windows i macOS):

```bash
pnpm --dir client install --frozen-lockfile
pnpm --dir client quality
cargo desktop dev
```

Při prvním spuštění projít celý setup (ffmpeg, uv, Python, venv, balíčky, modely). Ověřit, že data vznikla v `~/.nightingale-cz` (Windows `%USERPROFILE%\.nightingale-cz`) a že upstream Nightingale, pokud je nainstalovaný, dál používá `~/.nightingale` beze změny.

## 2. libass v přibaleném ffmpeg

Zdroje ffmpeg podle `app-core/src/vendor.rs`: Linux johnvansickle (static), macOS evermeet (`ffmpeg-8.1.zip`), Windows BtbN (`ffmpeg-master-latest-win64-gpl.zip`).

Postup po dokončení vendor setupu:

```bash
# macOS a Linux
~/.nightingale-cz/vendor/ffmpeg -hide_banner -filters | grep -E " ass | subtitles "
~/.nightingale-cz/vendor/ffmpeg -hide_banner -buildconf | grep -E "libass|libfreetype|libfontconfig|libharfbuzz"
```

```powershell
# Windows
& "$env:USERPROFILE\.nightingale-cz\vendor\ffmpeg.exe" -hide_banner -filters | Select-String " ass | subtitles "
& "$env:USERPROFILE\.nightingale-cz\vendor\ffmpeg.exe" -hide_banner -buildconf | Select-String "libass|libfreetype|libfontconfig|libharfbuzz"
```

| Platforma | Filtr `ass` | Filtr `subtitles` | `--enable-libass` | Poznámka |
| --- | --- | --- | --- | --- |
| Linux (johnvansickle) | | | | |
| macOS (evermeet) | | | | |
| Windows (BtbN) | | | | |

Když některý build libass nemá, M4 potřebuje pro export jiný build ffmpeg (riziko v kap. 8 plánu).

## 3. Zarovnání pro češtinu

**Ověřeno (cloud):**

- `whisperx.alignment.DEFAULT_ALIGN_MODELS_HF["cs"]` je `comodoro/wav2vec2-xls-r-300m-cs-250` ve všech verzích, které vendor instaluje: `whisperx 3.3.3` (větev `legacy_torch`, `whisperx>=3.3.0,<3.3.4`), `3.8.6` a `3.8.7rc1` (`whisperx>=3.8.7rc1`). Vlastní mapování v `align_models.py` (M2) tedy není nutné, pokud model nebude slabý.
- Qwen aligner češtinu nepodporuje: `qwen_align.SUPPORTED_LANGS` = `en, zh, yue, fr, de, it, ja, ko, pt, ru, es`. `align.py` pro `cs` použije rovnou cestu přes wav2vec2 (podmínka `qwen_align.is_supported(language)`).

**Čeká (potřebuje Hugging Face):** licence modelu a pokrytí znaků ve slovníku. Postup ve vendor venv:

```bash
~/.nightingale-cz/vendor/venv/bin/python - <<'EOF'
from transformers import Wav2Vec2Processor
p = Wav2Vec2Processor.from_pretrained("comodoro/wav2vec2-xls-r-300m-cs-250")
vocab = set(p.tokenizer.get_vocab())
need = set("áčďéěíňóřšťúůýž")
print("chybí:", sorted(need - vocab) or "nic")
print("velikost slovníku:", len(vocab))
EOF
```

| Kontrola | Výsledek |
| --- | --- |
| Licence modelu (karta na Hugging Face) | |
| Chybějící znaky z `áčďéěíňóřšťúůýž` | |
| Velká písmena ve slovníku (ano/ne) | |

## 4. Detekce jazyka

`detect_language_multiwindow` (`app-core/analyzer/language.py`) se volá při přepisu i při zarovnání, pokud píseň nemá jazyk nastavený ručně. Výsledek hlasování se zapisuje do logu jako `Language scores: {...} -> '<jazyk>'`.

Postup: analyzovat 10 českých písní z [testovací sady](testovaci-sada.md) bez ručního jazyka a v `~/.nightingale-cz/nightingale.log` vyhledat řádky `Language scores`.

| Píseň | Detekovaný jazyk | Skóre cs | Skóre sk/pl/sl |
| --- | --- | --- | --- |
| | | | |

Výsledek: X z 10 detekováno jako `cs`. Podle výsledku rozhodnout, jestli v M2 stačí jazyk z textu (whatlang) a výchozí jazyk přepisu, nebo je potřeba i přemapování `sk` → `cs` (kap. 2.5 plánu).

## 5. Výkon Whisper modelů

Výchozí model je dnes `large-v3` (`AppConfig::whisper_model`). Měřit celou analýzu jedné 4minutové písně (separace + přepis + zarovnání) s vynuceným přepisem, aby se neuplatnil text z LRCLIB.

| Stroj | `large-v3` | `large-v3-turbo` | `medium` |
| --- | --- | --- | --- |
| Windows notebook, CPU (model CPU, RAM) | | | |
| MacBook M1–M4 (model, RAM) | | | |

**Rozhodnutí o výchozím modelu:** čeká na měření.

## 6. České weby s texty

Pro každý web ověřit: dostupnost, vyhledávání přes URL, strukturu stránky s textem (selektor originálu, ne překladu), `robots.txt` a podmínky použití. Weby, které automatický přístup zakazují, nepoužívat.

| Web | Dostupný | Vyhledávání (vzor URL) | Selektor textu (originál) | `robots.txt` | Podmínky použití | Použít |
| --- | --- | --- | --- | --- | --- | --- |
| karaoketexty.cz | | | | | | |
| texty.cz | | | | | | |
| lyrics.cz | | | | | | |
| supermusic.cz (záloha) | | | | | | |
| pisnicky-akordy.cz (záloha) | | | | | | |

**Rozhodnutí o seznamu a pořadí webů:** čeká na ověření.

## 7. yt-dlp + Deno

**Ověřeno (cloud, PyPI):**

- Aktuální `yt-dlp` je `2026.10.26`. Extra `default` obsahuje `yt-dlp-ejs==0.8.0`, `mutagen`, `pycryptodomex`, `websockets`, `brotli`, `certifi`, `requests`, `urllib3`.
- Volba pro JS runtime je `--js-runtimes RUNTIME[:PATH]`, kde `PATH` je binárka nebo její složka. Ve výchozím stavu je povolené jen `deno`. Argument pro M1 je tedy `--js-runtimes deno:<vendor>/deno/deno` (ve Windows `deno.exe`).
- `--remote-components` není potřeba, protože `yt-dlp-ejs` je nainstalovaný přes extra `default`.

**Čeká:** stažení tří videí. Postup v čistém venv:

```bash
uv venv /tmp/ytdlp-test
uv pip install --python /tmp/ytdlp-test/bin/python "yt-dlp[default]"
# Deno: https://github.com/denoland/deno/releases (zip pro danou platformu + .sha256sum)
/tmp/ytdlp-test/bin/python -m yt_dlp --ignore-config --no-playlist \
  --js-runtimes deno:/cesta/k/deno --ffmpeg-location ~/.nightingale-cz/vendor/ffmpeg \
  -f "bv*[vcodec^=avc1][height<=1080]+ba[ext=m4a]/b[ext=mp4]/bv*[height<=1080]+ba/b" \
  --merge-output-format mp4 -o "%(id)s.%(ext)s" -- "<URL>"
```

| Zdroj | Stažení OK | Kontejner a kodek videa | Poznámka |
| --- | --- | --- | --- |
| YouTube klip | | | |
| YouTube Music | | | |
| SoundCloud | | | |

## Rozhodnutí z M0

| Otázka | Rozhodnutí |
| --- | --- |
| Název, identifier | `Nightingale CZ`, `cz.dospe.nightingale-cz` |
| Datová složka | `~/.nightingale-cz` |
| Updater | endpoint na releases forku, vlastní klíč vygeneruje vlastník lokálně (viz [FORK.md](FORK.md)) |
| Ikony | upstream + štítek CZ (`scripts/fork/cz_badge.py`) |
| Model zarovnání pro `cs` | výchozí z WhisperX (`comodoro/wav2vec2-xls-r-300m-cs-250`), pokud ověření slovníku neukáže problém |
| Výchozí Whisper model | čeká na měření (bod 5) |
| Seznam českých webů | čeká na ověření (bod 6) |
