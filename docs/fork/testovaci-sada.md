# Testovací sada

Sada 10 českých a 10 anglických písní pro ověření milníků M0–M5. Do repozitáře patří jen tento seznam. Média, texty ani výsledné exporty sem nedávat.

**Stav:** návrh výběru. URL doplní vlastník (ověřit, že vedou na oficiální nahrávku nebo klip a že video je ke stažení). Písně lze vyměnit, ale každá kategorie by měla zůstat pokrytá.

## Sloupce

- **Co ověřuje**: proč je píseň v sadě.
- **Očekávaný text**: odhad, odkud by měl text přijít (`LRCLIB`, `CZ web`, `Whisper`). Skutečný výsledek se zapisuje do `overeni-Mx.md`.
- **Pozor na**: známá úskalí (refrény psané jednou, dlouhé instrumentální části, sbor, živá verze).

## České písně

| # | Interpret – Název | Žánr | URL | Co ověřuje | Očekávaný text | Pozor na |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Karel Gott – Být stále mlád | pop (80. léta) | | klasický pop, čistá výslovnost | LRCLIB nebo CZ web | |
| 2 | Marta Kubišová – Modlitba pro Martu | balada, starší nahrávka | | starší záznam, šum, pomalé tempo | CZ web | dlouhé tóny (UltraStar) |
| 3 | Lucie – Amerika | rock balada | | rock, nástroje přes zpěv | CZ web | refrén psaný jednou |
| 4 | Olympic – Želva (živě) | rock, živá nahrávka | | živá verze, potlesk, odchylky od studiového textu | CZ web | metrika kvality zarovnání (M2) |
| 5 | Jaromír Nohavica – Těšínská | folk, kytara | | folk, hodně slov, nářeční výrazy | CZ web | slova mimo slovník modelu |
| 6 | Ewa Farna – Měls mě vůbec rád | moderní pop | | ženský hlas, moderní produkce | LRCLIB nebo CZ web | |
| 7 | Mirai – Když nemůžeš, tak přidej | moderní pop | | současná produkce, detekce jazyka | LRCLIB nebo CZ web | |
| 8 | Ben Cristovao – Asio | rap / pop | | rychlý rap, freestyle noty v UltraStar | Whisper nebo CZ web | rychlá slova, nejistá výška tónu |
| 9 | J. J. Ryba – Česká mše vánoční: Hej, mistře | sbor a sólisté | | sbor, více hlasů zároveň, archaická čeština | CZ web nebo Whisper | separace hlasu, sbor vs. sólo |
| 10 | Michal David – Discopříběh | pop (80. léta), rychlé tempo | | rychlé tempo, syntezátory | LRCLIB nebo CZ web | opakování `(2x)` |

## Anglické písně

| # | Interpret – Název | Žánr | URL | Co ověřuje | Očekávaný text | Pozor na |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Adele – Someone Like You | balada, klavír | | referenční čistý zpěv | LRCLIB | |
| 2 | Queen – Bohemian Rhapsody | rock, vícehlasé pasáže | | změny tempa, vícehlas | LRCLIB | dlouhé instrumentální části (odpočet v ASS) |
| 3 | Eminem – Lose Yourself | rap | | rychlý rap | LRCLIB | freestyle noty |
| 4 | ABBA – Dancing Queen | pop, vrstvené vokály | | vrstvené vokály | LRCLIB | |
| 5 | Nirvana – Smells Like Teen Spirit | grunge | | nezřetelná výslovnost, hlasité kytary | LRCLIB | |
| 6 | Ed Sheeran – Shape of You | moderní pop | | moderní produkce | LRCLIB | |
| 7 | Bon Jovi – Livin' on a Prayer | rock | | rock, změna tóniny | LRCLIB | |
| 8 | Eagles – Hotel California (Hell Freezes Over, živě) | rock, živá nahrávka | | živá verze, dlouhé intro | LRCLIB | úvodní titulek v ASS (zpěv začíná pozdě) |
| 9 | Pentatonix – Hallelujah | a cappella | | jen hlasy bez nástrojů, separace | LRCLIB | instrumentál téměř prázdný |
| 10 | Whitney Houston – I Will Always Love You | balada | | velký rozsah, dlouhé tóny | LRCLIB | oktávové chyby ve výšce tónu (UltraStar) |

## Očekávané výsledky podle milníků

| Milník | Kritérium na této sadě |
| --- | --- |
| M1 | Všech 20 URL se stáhne jako MP4 (nebo jen zvuk, když web video nenabízí) se správnými tagy |
| M2 | Text se automaticky najde aspoň u 7 z 10 českých písní, v průměru ≥ 85 % slov se `score ≥ 0.3`. U anglických stejný výsledek jako upstream |
| M3 | LRC, ELRC a ASS synchronní na 5 vybraných písních (aspoň 3 české) |
| M4 | MP4 synchronní v toleranci ±50 ms na 5 vybraných písních |
| M5 | UltraStar: výška tónu v ±1 půltónu u ≥ 70 % not na 5 studiových nahrávkách |
