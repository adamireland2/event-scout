# Getting Event Scout on the Google Play Store — Step by Step

This guide assumes zero coding experience. Everything technical that *could* be
prepared in advance is already in this folder. What remains are the steps only
you can do, because they require your Google account and identity.

**Good news you should know first:** both apps are already "true installable
apps" today, without the Play Store. On an Android phone, open the app's web
address in Chrome and tap **Install app** in the ⋮ menu (on iPhone: Safari →
Share → **Add to Home Screen**). It gets its own icon, opens full-screen with
no browser bar, and works like any app. The Play Store steps below are only
needed if you want people to find and install it *from the store*.

---

## What's in this folder

| File | What it's for |
|---|---|
| `cre/screenshots/*.png` | 4 phone screenshots (1080×1920) for the CRE listing |
| `cre/feature-graphic.png` | The 1024×500 banner Google requires |
| `cre/listing.md` | Ready-to-paste store listing text for CRE |
| `residential/…` | The same three things for the Residential app |
| `assetlinks-template.json` | Proof-of-ownership file (explained in Step 5) |

The 512×512 app icons Google asks for already exist in the repo:
`icons/icon-512.png` (CRE) and `icons-residential/icon-512.png` (Residential).

---

## Step 1 — Make sure the apps are live on the web

The Play Store version of a web app is a thin Android wrapper that loads your
live website, so the site must be online first.

1. Go to your repo on GitHub → **Settings** → **Pages**.
2. Under "Build and deployment", set Source to **Deploy from a branch**,
   branch **main**, folder **/ (root)**, and save.
3. After a minute or two, your apps are live at:
   - `https://adamireland2.github.io/event-scout/cre/`
   - `https://adamireland2.github.io/event-scout/residential/`
4. Open both on your phone and confirm they work. Add `?demo=1` to the end of
   either address to see them filled with sample data.

## Step 2 — Create a Google Play Developer account (you only)

1. Go to https://play.google.com/console/signup
2. Sign in with your Google account, choose **Personal** account type.
3. Pay the one-time **$25 USD** registration fee and complete identity
   verification (Google asks for an ID document; approval usually takes a few
   days).

⚠️ **Honest heads-up:** personal developer accounts created after November
2023 must run a **closed test with at least 12 testers for 14 days** before
Google allows publishing publicly. Friends/family/colleagues with Android
phones count. Plan for this — it's Google's rule, not something we can skip.

## Step 3 — Package each app with PWABuilder (free, no coding)

PWABuilder is a free Microsoft tool that turns a web app into a real Android
app file (`.aab`) you upload to Google.

1. Go to https://www.pwabuilder.com
2. Paste `https://adamireland2.github.io/event-scout/cre/` and click **Start**.
3. When scoring finishes, click **Package for Stores** → **Android** →
   **Google Play**.
4. Fill the form:
   - **Package ID:** `io.github.adamireland2.eventscout.cre`
   - **App name:** `Event Scout CRE`  — **Short name:** `Scout CRE`
   - Leave signing on "Create new" (PWABuilder generates the signing key).
5. Download the ZIP. Inside are:
   - the `.aab` file → this gets uploaded to Google in Step 6
   - `assetlinks.json` → needed in Step 5
   - a `signing.keystore` + passwords file → **save this somewhere safe
     forever** (Google can't replace it; losing it means you can't update the
     app).
6. Repeat 2–5 for `https://adamireland2.github.io/event-scout/residential/`
   with Package ID `io.github.adamireland2.eventscout.residential` and name
   `Event Scout Residential`.

## Step 4 — Why there's a proof-of-ownership file

Android needs proof that the app and the website belong to the same person,
or the app opens with a browser bar at the top. That proof is a small file
served at **exactly** this address:

```
https://adamireland2.github.io/.well-known/assetlinks.json
```

Note that this is the **root** of `adamireland2.github.io` — NOT inside
`/event-scout/`. (The `.well-known` folder already in this repo can't satisfy
this, because Google only looks at the domain root. This is a GitHub Pages
quirk for project sites.)

## Step 5 — Publish the proof file

1. On GitHub, create a **new repository** named exactly:
   `adamireland2.github.io` (public).
2. In it, create a file at path `.well-known/assetlinks.json`.
3. Paste the contents of the `assetlinks.json` files PWABuilder gave you for
   **both** apps, merged into one list — use `assetlinks-template.json` in
   this folder as the model: it's already structured for two apps; just
   replace each `REPLACE_WITH_SHA256_FROM_PWABUILDER` with the fingerprint
   from the matching PWABuilder download.
4. Enable GitHub Pages on that new repo too (Settings → Pages → main branch).
5. Check the file loads at the address above.

## Step 6 — Create the listings in Play Console

For each app (CRE first, then Residential):

1. In https://play.google.com/console click **Create app** → name it, choose
   **App** (not game), **Free**.
2. **Store listing:** copy-paste everything from `listing.md` in this folder;
   upload the 512 icon, `feature-graphic.png`, and the 4 screenshots.
3. **Privacy policy URL:** `https://adamireland2.github.io/event-scout/privacy.html`
4. **Data safety form:** answer that the app does **not collect or share user
   data** — the API key and search history live only on the user's device
   (that's exactly what the privacy policy says). Where it asks about data
   sent off-device, note that searches go directly to Anthropic's API at the
   user's own request using the user's own key.
5. **Content rating questionnaire:** business/productivity app, no
   objectionable content → rating "Everyone".
6. **App content → Ads:** No ads.
7. Under **Testing → Closed testing**, create a release, upload the `.aab`
   from Step 3, and add your 12+ testers' email addresses.
8. After 14 days of testing, apply for **Production** access and roll out.

## Step 7 — After it's live

- Updating the app's *content or features* = just updating this website (the
  Play app is a window onto the live site — users get changes automatically,
  no store re-submission).
- You only re-run PWABuilder + upload a new `.aab` if you change the app's
  name, icon, or web address.

---

## Costs summary

| Item | Cost |
|---|---|
| GitHub Pages hosting | Free |
| PWABuilder packaging | Free |
| Google Play developer account | $25 once |
| Per-search AI cost (Budget mode) | ~$0.03–0.10, paid by whoever's API key is used |
