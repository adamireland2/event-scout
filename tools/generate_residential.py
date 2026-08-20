#!/usr/bin/env python3
"""Generate residential/index.html from cre/index.html.

The CRE app is the source of truth. This script swaps the branding,
theme colors, AI instructions, categories, and demo data to produce
the Residential edition. Run from the repo root:

    python3 tools/generate_residential.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "cre" / "index.html"
DST = ROOT / "residential" / "index.html"

CONFIG = """/*__CONFIG_START__*/
const APP_ID="residential";
const APP_NAME="Event Scout Residential";
const APP_EMOJI="\U0001F3E1";
const APP_TAGLINE="Residential real estate events that close deals";
/*__CONFIG_END__*/"""

PROMPT = """/*__PROMPT_START__*/
const SYSTEM_PROMPT=`You are an elite event intelligence agent. Your sole mission is to find in-person events, conferences, and networking opportunities that will put your principal directly in front of RESIDENTIAL REAL ESTATE decision makers who buy — or influence the purchase of — specialty tax incentive studies.

## WHO YOU WORK FOR
Your principal runs a specialty tax consulting practice selling: Cost Segregation Studies, 45L Energy Efficient Home Credits, 179D Deductions (for multifamily 4+ stories), and ITC (Investment Tax Credit for solar/energy on residential projects). This app focuses on the RESIDENTIAL side of real estate.

## GEOGRAPHY
Home base: San Francisco Bay Area / San Jose, California. Also include major US cities. Always flag Bay Area events first.

## DECISION MAKERS TO FIND
Tier 1 (Direct Buyers): Homebuilders (production and custom), multifamily developers and owners, build-to-rent operators, single-family rental (SFR) portfolio investors, apartment syndicators, land developers, residential solar developers.
Tier 2 (Referral Sources): CPAs/tax partners serving real estate investors, real estate attorneys, wealth advisors, residential lenders and mortgage bankers, property managers, 1031 exchange intermediaries.
Tier 3 (Strategic): Home builders association (NAHB/BIA/HBA) leaders, apartment association leaders, REIA organizers, economic development officials.

## CRITICAL RULE: IN-PERSON EVENTS ONLY
ONLY recommend events with a physical venue. NEVER recommend webinars, virtual, online, Zoom, Teams, livestream, or digital events. If you cannot confirm a physical venue, SKIP IT.

## MEMBER ORGANIZATIONS
When member organizations are provided, search their websites and event calendars directly. Flag these as "Member Organization Event".

## OUTPUT FORMAT — STRICT JSON
You MUST output your results as a JSON array. No other text before or after. Each event is an object:
[
  {
    "name": "Event Name",
    "date": "Month Day, Year",
    "location": "City, State — Venue Name",
    "organizer": "Organizer Name",
    "link": "https://...",
    "format": "Conference",
    "cost": "$XX or TBD or Invite-only",
    "priority": "must-attend" | "strong-fit" | "worth-considering",
    "why": "2-3 sentence explanation",
    "decision_makers": "Who will be there",
    "services": ["Cost Seg", "45L", "179D", "ITC"],
    "actions": ["Register by X", "Review speakers", "etc"],
    "member_org": false
  }
]

ONLY output valid JSON. No markdown, no commentary, no preamble. Just the JSON array.

## BEHAVIORAL RULES
1. IN-PERSON ONLY. 2. Verify events are real. 3. Quality over quantity. 4. Name names from speaker lists. 5. Flag sponsorship/speaking opportunities in actions. 6. Bundle events in same city. 7. Map to specific service lines. 8. Search member org calendars when provided.`;
/*__PROMPT_END__*/"""

CATEGORIES = """/*__CATEGORIES_START__*/
const CATEGORIES=[
  {id:"builders",icon:"\U0001F3E0",label:"Homebuilders & Developers",desc:"NAHB, BIA/HBA, and homebuilding industry events",base:"Find the best in-person homebuilding industry conferences and builder association (NAHB, BIA, HBA) networking events where I can meet production homebuilders, custom builders, and residential land developers"},
  {id:"multifamily",icon:"\U0001F3E2",label:"Multifamily & Build-to-Rent",desc:"Apartment, BTR, and multifamily investment conferences",base:"Find in-person multifamily, apartment industry, and build-to-rent conferences and networking events where I can meet multifamily developers, owners, and syndicators"},
  {id:"investors",icon:"\U0001F4BC",label:"RE Investors & REIA",desc:"Real estate investor associations and SFR events",base:"Find in-person real estate investor association (REIA) meetings, single-family rental investment conferences, and residential real estate investor networking events"},
  {id:"tax",icon:"\U0001F4CA",label:"Tax & CPA Conferences",desc:"CPA society events, tax conferences, and accounting networking",base:"Find in-person CPA society events, tax conferences, and accounting industry networking events"},
  {id:"all",icon:"\U0001F50D",label:"Full Scan — All Residential",desc:"Comprehensive search across all residential categories",base:"Do a comprehensive scan of all high-value in-person events for my tax incentive consulting business across homebuilding, multifamily, build-to-rent, residential investing, and tax/accounting. Top 8-10 ranked by deal value"},
];
/*__CATEGORIES_END__*/"""

DEMO = """/*__DEMO_START__*/
const DEMO_EVENTS=[
  {name:"PCBC — Pacific Coast Builders Conference",date:"June 24-25, 2026",location:"San Francisco, CA — Moscone Center",organizer:"California Building Industry Association",link:"https://www.pcbc.com",format:"Conference",cost:"$395",priority:"must-attend",why:"The West Coast's largest homebuilding conference, in your home market. Production builders, multifamily developers, and land developers all attend — every one a 45L and cost segregation prospect.",decision_makers:"Production homebuilders, multifamily developers, land developers, building product executives",services:["45L","Cost Seg"],actions:["Register early for best rate","Review exhibitor list for target builders"],member_org:false},
  {name:"BIA Bay Area Builder Awards Gala",date:"October 8, 2026",location:"Santa Clara, CA — Hyatt Regency",organizer:"Building Industry Association Bay Area",link:"https://www.biabayarea.org",format:"Gala / Networking",cost:"$225",priority:"must-attend",why:"The Bay Area homebuilding industry's biggest networking night. Principals from every active local builder attend, and sponsorships put your name in front of the whole room.",decision_makers:"Homebuilder principals, division presidents, residential developers",services:["45L","Cost Seg"],actions:["Consider event sponsorship","Book table before September"],member_org:true},
  {name:"IMN Single Family Rental Forum (West)",date:"December 3-5, 2026",location:"Scottsdale, AZ — Westin Kierland",organizer:"IMN",link:"https://www.imn.org",format:"Conference",cost:"$1,500+",priority:"strong-fit",why:"The premier gathering of SFR and build-to-rent portfolio investors. Attendees own thousands of rental homes each — large-scale cost segregation opportunities in a single conversation.",decision_makers:"SFR portfolio owners, build-to-rent operators, RE private equity",services:["Cost Seg"],actions:["Build meeting list in advance","Attend the BTR track"],member_org:false},
  {name:"NorCal REIA Monthly Meeting",date:"September 9, 2026",location:"Sacramento, CA — DoubleTree Sacramento",organizer:"Norcal REIA",link:"https://www.norcalreia.com",format:"Meetup",cost:"$25",priority:"strong-fit",why:"Consistent monthly room of active residential investors — flippers, landlords, and syndicators. Low cost, high repeat value, and a natural fit for a cost segregation education talk.",decision_makers:"Residential investors, landlords, apartment syndicators",services:["Cost Seg"],actions:["Offer to speak on tax savings","Bring referral one-pagers"],member_org:false},
  {name:"Multifamily Executive Conference",date:"September 29 - October 1, 2026",location:"Las Vegas, NV — Bellagio",organizer:"Zonda",link:"https://www.mfexec.com",format:"Conference",cost:"$1,095",priority:"worth-considering",why:"Senior multifamily executives — developers, owners, and operators of large apartment portfolios. Strong fit for cost segregation and 179D on 4+ story projects.",decision_makers:"Multifamily developers, apartment owners/operators, REIT executives",services:["Cost Seg","179D","45L"],actions:["Review speaker lineup","Schedule 1:1s with target developers"],member_org:false},
];
/*__DEMO_END__*/"""

# Indigo -> emerald theme swap (hex values appear in CSS and inline styles)
COLOR_MAP = {
    "6366f1": "10b981",
    "8b5cf6": "059669",
    "7c3aed": "047857",
    "a78bfa": "34d399",
    "a5b4fc": "6ee7b7",
    "c7d2fe": "a7f3d0",
    "eef2ff": "ecfdf5",
    "4f46e5": "059669",
    "4338ca": "065f46",
    "faf5ff": "f0fdf4",
    "rgba(99,102,241": "rgba(16,185,129",
}

HEAD_MAP = {
    "<title>Event Scout CRE — Commercial Real Estate Events</title>":
        "<title>Event Scout Residential — Residential Real Estate Events</title>",
    'content="Event Scout CRE"': 'content="Event Scout Residential"',
    'content="AI-powered commercial real estate event intelligence for tax incentive professionals."':
        'content="AI-powered residential real estate event intelligence for tax incentive professionals."',
    "\U0001F3D9️": "\U0001F3E1",  # cityscape emoji -> house emoji (favicon)
    "Checking Bisnow, NAIOP, ULI...": "Checking NAHB, BIA, IMN...",
}


def swap_block(text, start_marker, end_marker, replacement):
    pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.S)
    if not pattern.search(text):
        raise SystemExit(f"Marker block not found: {start_marker}")
    return pattern.sub(lambda _: replacement, text, count=1)


def main():
    text = SRC.read_text(encoding="utf-8")
    text = swap_block(text, "/*__CONFIG_START__*/", "/*__CONFIG_END__*/", CONFIG)
    text = swap_block(text, "/*__PROMPT_START__*/", "/*__PROMPT_END__*/", PROMPT)
    text = swap_block(text, "/*__CATEGORIES_START__*/", "/*__CATEGORIES_END__*/", CATEGORIES)
    text = swap_block(text, "/*__DEMO_START__*/", "/*__DEMO_END__*/", DEMO)
    for old, new in HEAD_MAP.items():
        text = text.replace(old, new)
    for old, new in COLOR_MAP.items():
        text = text.replace(old, new).replace(old.upper(), new)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(text, encoding="utf-8")
    print(f"Wrote {DST} ({len(text)} bytes)")


if __name__ == "__main__":
    main()
