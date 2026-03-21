# Event Scout — Google Play Store Publishing Guide

## What You Have

Your project folder (`event-scout-pwa/`) contains everything needed:

```
event-scout-pwa/
├── index.html          ← The app (same one from your desktop)
├── manifest.json       ← Tells Android what your app is called, its icon, etc.
├── sw.js               ← Service worker (makes the app work offline)
└── icons/
    ├── icon-72.png
    ├── icon-96.png
    ├── icon-128.png
    ├── icon-144.png
    ├── icon-152.png
    ├── icon-192.png
    ├── icon-384.png
    ├── icon-512.png
    ├── icon-maskable-192.png
    └── icon-maskable-512.png
```

## The 5-Step Process

### Step 1: Host the app on the web (free — 10 minutes)

The app needs to live at a public HTTPS URL. **GitHub Pages** is free and takes 10 minutes.

1. Go to **github.com** and create a free account (or sign in)
2. Click the **+** button in the top-right → **New repository**
3. Name it `event-scout` (or whatever you want)
4. Set it to **Public**
5. Click **Create repository**
6. On the next page, click **"uploading an existing file"**
7. Drag your entire `event-scout-pwa` folder contents into the upload area:
   - `index.html`
   - `manifest.json`
   - `sw.js`
   - The `icons/` folder with all the PNGs
8. Click **Commit changes**
9. Go to **Settings** → **Pages** (in the left sidebar)
10. Under "Source", select **main** branch and click **Save**
11. Wait 1-2 minutes. Your app is now live at:
    `https://YOUR-USERNAME.github.io/event-scout/`

**Test it:** Open that URL on your phone's Chrome browser. You should see the Event Scout app. If it works, move on.

---

### Step 2: Verify the PWA is valid (2 minutes)

Before building the Android package, confirm everything is set up right:

1. Go to **pwabuilder.com**
2. Paste your GitHub Pages URL: `https://YOUR-USERNAME.github.io/event-scout/`
3. Click **Start**
4. PWABuilder will scan your app and show a scorecard
5. You need green checks on:
   - ✅ Manifest found
   - ✅ Service worker detected
   - ✅ Icons present
   - ✅ HTTPS
6. If anything is yellow/red, PWABuilder will tell you exactly what to fix

---

### Step 3: Generate the Android package (5 minutes)

Still on PWABuilder:

1. Click the **"Package for stores"** button
2. Click **"Android"**
3. Fill in the form:
   - **Package ID:** `com.yourcompany.eventscout` (use your actual company domain reversed)
   - **App name:** `Event Scout`
   - **App version:** `1.0.0`
   - **Host:** `YOUR-USERNAME.github.io`
   - **Start URL:** `/event-scout/`
   - **Theme color:** `#6366f1`
   - **Background color:** `#f8fafc`
   - **Signing key:** Select **"New"** — PWABuilder generates one for you
     - ⚠️ **SAVE THIS KEY FILE.** You need it for every future update. Store it somewhere safe (Google Drive, etc.)
4. Click **"Generate"**
5. Download the ZIP file. Inside you'll find:
   - An `.aab` file (Android App Bundle — this is what you upload to Google Play)
   - A signing key file
   - An `assetlinks.json` file (you'll need this in Step 4)

---

### Step 4: Set up the Digital Asset Link (2 minutes)

This tells Google that your website and your app are connected.

1. In the ZIP from Step 3, find the `assetlinks.json` file
2. In your GitHub repository, create a folder called `.well-known/`
3. Upload `assetlinks.json` into that folder
4. The file must be accessible at:
   `https://YOUR-USERNAME.github.io/event-scout/.well-known/assetlinks.json`
5. **Test it:** Open that URL in your browser — you should see JSON content

---

### Step 5: Publish to Google Play (30-60 minutes first time)

#### A. Create a Google Play Developer account
1. Go to **play.google.com/console**
2. Sign in with a Google account
3. Pay the **one-time $25 registration fee**
4. Fill in your developer profile (name, address, etc.)
5. Account approval can take 24-48 hours for new accounts

#### B. Create your app listing
1. In the Play Console, click **"Create app"**
2. Fill in:
   - **App name:** Event Scout
   - **Default language:** English (United States)
   - **App or game:** App
   - **Free or paid:** Free (the app is free; users pay for their own API key)
3. Click **Create app**

#### C. Fill in the store listing
Go to **"Main store listing"** and fill in:

- **Short description (80 chars max):**
  `AI-powered event finder for tax incentive professionals`

- **Full description (4000 chars max):**
  ```
  Event Scout uses AI to search dozens of live event calendars and find the
  in-person conferences, networking events, and industry summits where your
  next clients will be.

  Built for professionals who sell specialty tax incentive studies — Cost
  Segregation, 179D/45L Energy Credits, R&D Tax Credits, and ITC — Event
  Scout finds events attended by commercial real estate developers, property
  owners, manufacturers, CPAs, and the decision makers who buy these services.

  HOW IT WORKS:
  • Pick a category (CRE & Construction, Manufacturing, Tax & CPA, Green
    Building, or scan all industries)
  • Choose your date range and target cities
  • The AI searches Bisnow, NAIOP, ULI, AICPA, Eventbrite, and dozens of
    other event calendars in real time
  • Get ranked recommendations with speaker names, attendee profiles, and
    action items

  FEATURES:
  • Search across 18+ US cities
  • Filter by date range (30 days to 6 months, or custom dates)
  • Events ranked by business development value (Must-attend / Strong fit /
    Worth considering)
  • Speaker and decision-maker identification
  • Service line mapping (which of your services fit each event)
  • Sponsorship and speaking opportunity flags

  Requires an Anthropic API key (get one at console.anthropic.com).
  Each search costs approximately $0.10–$0.40 in API credits.
  ```

- **Screenshots:** You'll need 2-8 phone screenshots (1080x1920 pixels).
  Take these by opening the app on your phone and using the built-in screenshot feature.

- **App icon:** Upload the `icon-512.png` from your icons folder.

#### D. Complete the content rating questionnaire
1. Go to **"Content rating"** in the left sidebar
2. Click **Start questionnaire**
3. Answer honestly — this app has no violence, no mature content, etc.
4. It will likely be rated **"Everyone"**

#### E. Set up pricing and distribution
1. Go to **"Countries / regions"**
2. Select the countries you want (at minimum: United States)
3. Confirm the app is **Free**

#### F. Upload the app bundle
1. Go to **"Production"** in the left sidebar
2. Click **"Create new release"**
3. Upload the `.aab` file from Step 3
4. Add release notes: `"Initial release — AI-powered event discovery for tax professionals"`
5. Click **"Review release"**
6. Click **"Start rollout to production"**

#### G. Wait for review
- Google reviews new apps in **1-7 days** (typically 2-3)
- You'll get an email when it's approved
- Once approved, search "Event Scout" in the Play Store and it's live!

---

## Updating the App Later

When you want to change the app (new features, bug fixes):

1. Edit the files in your GitHub repository
2. Commit the changes — GitHub Pages updates automatically
3. The app updates for ALL users within 24 hours (no new APK needed!)

For major updates, you CAN also bump the version in PWABuilder and upload a new `.aab` to the Play Console, but for most changes the web update is instant and automatic.

---

## Custom Domain (Optional but Professional)

Instead of `your-username.github.io/event-scout`, you can use a custom domain like `eventscout.yourcompany.com`:

1. Buy a domain (or use a subdomain of one you own)
2. In GitHub repo Settings → Pages → Custom domain, enter it
3. Set up the DNS records GitHub tells you to
4. Update the manifest.json and PWABuilder package to use the new domain

---

## Cost Summary

| Item | Cost | Frequency |
|------|------|-----------|
| GitHub Pages hosting | Free | Forever |
| Google Play Developer account | $25 | One-time |
| PWABuilder | Free | Forever |
| Anthropic API (per user, per search) | ~$0.10–0.40 | Per search |

---

## Troubleshooting

**PWABuilder says my manifest is missing:**
Make sure `manifest.json` is in the root of your repository (same level as `index.html`), not inside a subfolder.

**The app shows a browser toolbar on Android:**
The `assetlinks.json` file isn't set up correctly. Double-check Step 4.

**Google rejects the app:**
Most common reason: missing privacy policy. Create a simple page that says the app doesn't collect personal data (the API key stays on-device) and link to it in the store listing.

**Users say the app doesn't load:**
They need an internet connection to search for events (the AI needs to call the API). The app shell itself works offline after the first load.
