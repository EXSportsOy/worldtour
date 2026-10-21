# worldtour.exsports.fi

EXS World Tour -pelin sivusto: esittely, ohje ja maailmanlista. Staattinen sivusto, joka julkaistaan Firebase Hostingiin (siirtymävaiheessa myös GitHub Pagesiin).

## Rakenne

- `build.py` tuottaa HTML-sivut. Muokkaa sivujen sisältöä tässä tiedostossa, älä `index.html`-tiedostoissa, ja aja `python build.py`.
- `assets/css/tokens.css` ja `assets/css/bundle.css` tulevat pelin suunnittelujärjestelmästä (EXS World Tour, Viimeinen valo -teema). `assets/css/site.css` on sivuston oma asettelu.
- `assets/fonts/` Barlow-fontit woff2-muodossa (SIL Open Font License).
- `tools/check.py` tarkistaa sisäiset linkit; GitHub Actions ajaa sen ennen julkaisua.
- `lista/` ja `s/` näyttävät nyt esimerkkidataa. Oikea data tulee Firebase-rajapinnasta, kun World Rankin tekninen kokeilu on valmis (pelirepo: `Docs/plans/2026-10-01-sivusto-ja-world-rank.md`).

## Julkaisu Firebase Hostingiin

Sivusto julkaistaan pelin Firebase-projektin `exs-worldtour` oletussivustolle `exs-worldtour` (kohde `worldtour` tiedostoissa `firebase.json` ja `.firebaserc`). Samassa projektissa ovat pelin Auth, Firestore, telemetrian Realtime Database ja tuleva tilipalvelu `exs-accounts` (Cloud Run, `europe-west1`); niiden asetukset ovat pelirepon `firebase/`-hakemistossa. Tästä reposta julkaistaan vain Hosting.

Firebase Hosting -sivustolla on yksi julkaisu kerrallaan. Pelirepon `firebase/firebase.json` sisältää tilisivun (`web/dist`) Hosting-asetuksen samalle sivustolle, joten sitä ei saa julkaista erikseen: `firebase deploy` ilman `--only`-rajausta pelirepossa korvaisi tämän sivuston. Tilisivu ja `/api/**`-ohjaus Cloud Runiin yhdistetään tämän repon julkaisuun, kun tilipalvelu avataan.

Kertaluonteinen käyttöönotto:

1. Palvelutili GitHub Actionsille: Google Cloud Console (projekti `exs-worldtour`) › IAM › Service accounts › luo tili roolilla **Firebase Hosting Admin** (esikatselukanaville lisäksi **API Keys Viewer**), luo sille JSON-avain ja lisää se repon salaisuudeksi `FIREBASE_SERVICE_ACCOUNT_WORLDTOUR`. Vaihtoehtoisesti `firebase init hosting:github` tekee saman; nimeä salaisuus silloin uudelleen.
2. Aja työnkulku `.github/workflows/firebase-hosting.yml` käsin (Actions › Run workflow). Sivusto näkyy osoitteessa `https://exs-worldtour.web.app/`.
3. Hosting › `exs-worldtour` › Add custom domain: `worldtour.exsports.fi`. Lisää Firebasen antamat DNS-tietueet `exsports.fi`-vyöhykkeelle ja poista vanha CNAME `worldtour` → `exsportsoy.github.io`. Firebase myöntää sertifikaatin automaattisesti.
4. Kun Firebase näyttää verkkotunnuksen tilaksi Connected: poista `.github/workflows/pages.yml` ja `CNAME`, kytke GitHub Pages pois repon asetuksista ja päivitä evästesivun ja tietosuojaselosteen maininnat GitHub Pagesista.

Push `main`-haaraan julkaisee pääkanavan. Saman repon PR:t saavat 7 päivää voimassa olevan esikatseluosoitteen, jonka linkki tulee PR:n kommenttiin.

Paikallinen esikatselu Firebasen otsakkeilla: `npx firebase-tools emulators:start --only hosting` (http://127.0.0.1:5000/).

## Tietoturva

- Sivustolla ei ole eikä saa olla avaimia, joilla voi kirjoittaa tuloksia. Kaikki kirjoitus tapahtuu Cloud Runin tarkistuspalvelusta.
- CSP ja muut turvaotsakkeet asetetaan `firebase.json`-tiedostossa. Sama CSP on myös `<meta>`-tagissa siirtymävaiheen GitHub Pagesia varten. Kun Firebase-kirjautuminen lisätään, laajenna `connect-src` ja `script-src` molempiin.
- Ylläpitonäkymä ja tilin poisto toteutetaan tähän samaan Firebase Hosting -sivustoon.
- Jakolinkkien esikatselu (og-tagit suorituskohtaisesti) vaatii palvelimen: `/s/<tunnus>`-osoitteet ohjataan Cloud Runiin `firebase.json`-tiedoston `rewrites`-säännöllä, kun palvelu on pystyssä. Sääntöä ei voi lisätä etukäteen, koska julkaisu epäonnistuu, jos palvelua ei ole.
