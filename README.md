# worldtour.exsports.fi

EXS World Tour -pelin sivusto: esittely, ohje ja maailmanlista. Staattinen sivusto, joka julkaistaan GitHub Pagesilla.

## Rakenne

- `build.py` tuottaa HTML-sivut. Muokkaa sivujen sisältöä tässä tiedostossa, älä `index.html`-tiedostoissa, ja aja `python build.py`.
- `assets/css/tokens.css` ja `assets/css/bundle.css` tulevat pelin suunnittelujärjestelmästä (EXS World Tour, Viimeinen valo -teema). `assets/css/site.css` on sivuston oma asettelu.
- `assets/fonts/` Barlow-fontit woff2-muodossa (SIL Open Font License).
- `tools/check.py` tarkistaa sisäiset linkit; GitHub Actions ajaa sen ennen julkaisua.
- `lista/` ja `s/` näyttävät nyt esimerkkidataa. Oikea data tulee Firebase-rajapinnasta, kun World Rankin tekninen kokeilu on valmis (pelirepo: `Docs/plans/2026-10-01-sivusto-ja-world-rank.md`).

## Julkaisu GitHub Pagesiin

1. Luo GitHub-repo `EXSportsOy/worldtour` ja työnnä tämä kansio sen `main`-haaraan.
2. Repon asetuksissa Pages › Build and deployment › Source: **GitHub Actions**.
3. Pages › Custom domain: `worldtour.exsports.fi`, ja rastita **Enforce HTTPS**, kun sertifikaatti on myönnetty.
4. DNS: lisää `exsports.fi`-vyöhykkeelle CNAME-tietue `worldtour` → `exsportsoy.github.io`.
5. Organisaation asetuksissa Pages › Verified domains: vahvista `exsports.fi`, jos sitä ei ole vielä tehty. Se estää alidomainin kaappauksen.

Jokainen push `main`-haaraan julkaisee sivuston työnkululla `.github/workflows/pages.yml`.

## Tietoturva

- Sivustolla ei ole eikä saa olla avaimia, joilla voi kirjoittaa tuloksia. Kaikki kirjoitus tapahtuu Cloud Runin tarkistuspalvelusta.
- CSP on `<meta>`-tagissa, koska GitHub Pages ei salli omia HTTP-otsakkeita. Kun Firebase-kirjautuminen lisätään, laajenna `connect-src` ja `script-src` sen osoitteisiin.
- Ylläpitonäkymä ja tilin poisto toteutetaan Firebase Hostingiin, jossa otsakkeet voi asettaa. Tämä sivusto linkittää niihin.
- Jakolinkkien esikatselu (og-tagit suorituskohtaisesti) vaatii palvelimen: `/s/<tunnus>`-osoitteet ohjataan Cloud Runiin, kun se on pystyssä.
