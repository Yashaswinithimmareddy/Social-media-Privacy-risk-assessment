"""
Social Media Privacy Risk Assessment Framework
Questionnaire Configuration & Definitions

This module defines the 44 defensive privacy assessment questions across
10 structured categories. No personal identifiable information (PII) is collected;
only self-reported privacy configurations and exposure behaviors are evaluated.
"""

CATEGORIES = {
    "CAT_A": {
        "id": "CAT_A",
        "name": "Profile Visibility",
        "weight": 0.10,
        "description": "Evaluates account discoverability, search engine indexing, and friend list exposure."
    },
    "CAT_B": {
        "id": "CAT_B",
        "name": "Personal Information",
        "weight": 0.15,
        "description": "Assesses public visibility of contact details, birth date, home, and family info."
    },
    "CAT_C": {
        "id": "CAT_C",
        "name": "Location Privacy",
        "weight": 0.15,
        "description": "Analyzes live location broadcasts, check-ins, travel itinerary exposure, and GPS geotags."
    },
    "CAT_D": {
        "id": "CAT_D",
        "name": "Posts & Content",
        "weight": 0.10,
        "description": "Measures post audience defaults, sensitive workplace document leaks, and personal oversharing."
    },
    "CAT_E": {
        "id": "CAT_E",
        "name": "Friends & Followers",
        "weight": 0.10,
        "description": "Evaluates handling of stranger requests, follower audits, and audience segmentations."
    },
    "CAT_F": {
        "id": "CAT_F",
        "name": "Tagging & Mentions",
        "weight": 0.05,
        "description": "Assesses tagging approvals, facial recognition suggestions, and public mention permissions."
    },
    "CAT_G": {
        "id": "CAT_G",
        "name": "Authentication & Account Security",
        "weight": 0.15,
        "description": "Reviews multi-factor authentication (MFA), password hygiene, login alerts, and active sessions."
    },
    "CAT_H": {
        "id": "CAT_H",
        "name": "Third-Party Apps",
        "weight": 0.05,
        "description": "Measures OAuth permissions, connected legacy apps, social logins, and viral quiz access."
    },
    "CAT_I": {
        "id": "CAT_I",
        "name": "Messaging & Social Engineering",
        "weight": 0.10,
        "description": "Assesses phishing awareness, OTP/verification code hygiene, impersonation vigilance, and scam DM interaction."
    },
    "CAT_J": {
        "id": "CAT_J",
        "name": "Digital Footprint",
        "weight": 0.05,
        "description": "Evaluates historical post cleanup, abandoned account posture, username correlation, and privacy audits."
    }
}

QUESTIONS = [
    # ------------------ CATEGORY A: Profile Visibility ------------------
    {
        "id": "q1",
        "category": "CAT_A",
        "question": "What is the primary visibility setting of your main social media profile?",
        "options": [
            {"value": "PUBLIC", "label": "Public (anyone can view profile, bio, and timeline)", "risk_score": 10},
            {"value": "FRIENDS_OF_FRIENDS", "label": "Friends of Friends (semi-public discovery)", "risk_score": 5},
            {"value": "FRIENDS_ONLY", "label": "Friends / Followers Only (restricted visibility)", "risk_score": 2},
            {"value": "PRIVATE", "label": "Completely Private (approved followers only)", "risk_score": 0}
        ],
        "explanation": "Public profiles allow OSINT analysts, data brokers, and threat actors to harvest public details without requesting permission."
    },
    {
        "id": "q2",
        "category": "CAT_A",
        "question": "Is your profile set to be indexed by external search engines (Google, Bing)?",
        "options": [
            {"value": "YES", "label": "Yes (my name and profile link appear in web search results)", "risk_score": 10},
            {"value": "NOT_SURE", "label": "Not Sure (default platform settings apply)", "risk_score": 6},
            {"value": "NO", "label": "No (search engine indexing is explicitly disabled)", "risk_score": 0}
        ],
        "explanation": "Search engine indexing makes your profile cached and searchable across third-party identity intelligence scrapers."
    },
    {
        "id": "q3",
        "category": "CAT_A",
        "question": "Who can see your complete list of friends, connections, or followers?",
        "options": [
            {"value": "PUBLIC", "label": "Public (anyone on the internet can see my contacts)", "risk_score": 10},
            {"value": "FRIENDS", "label": "Friends Only (visible to my connections)", "risk_score": 4},
            {"value": "ONLY_ME", "label": "Only Me / Private (hidden from everyone)", "risk_score": 0}
        ],
        "explanation": "Public friend lists enable spear phishing by letting attackers identify and impersonate close friends, colleagues, or supervisors."
    },
    {
        "id": "q4",
        "category": "CAT_A",
        "question": "Who can view and download your full-resolution profile photo and past avatar albums?",
        "options": [
            {"value": "PUBLIC", "label": "Public (accessible to anyone without login)", "risk_score": 8},
            {"value": "FRIENDS", "label": "Friends Only (locked to connections)", "risk_score": 3},
            {"value": "RESTRICTED", "label": "Protected / Avatar guard enabled", "risk_score": 0}
        ],
        "explanation": "High-resolution avatars can be harvested for reverse image searching and facial synthesis/deepfake cloning."
    },

    # ------------------ CATEGORY B: Personal Information ------------------
    {
        "id": "q5",
        "category": "CAT_B",
        "question": "Is your mobile phone number visible anywhere on your public profile or bio?",
        "options": [
            {"value": "YES", "label": "Yes (visible to anyone visiting profile)", "risk_score": 10},
            {"value": "NOT_SURE", "label": "Not Sure", "risk_score": 6},
            {"value": "NO", "label": "No (strictly hidden or never linked)", "risk_score": 0}
        ],
        "explanation": "Public phone numbers expose users to SIM swapping, vishing, SMS smishing attacks, and cross-platform identity linking."
    },
    {
        "id": "q6",
        "category": "CAT_B",
        "question": "Is your personal email address displayed on your profile or public contact button?",
        "options": [
            {"value": "YES", "label": "Yes (publicly visible)", "risk_score": 9},
            {"value": "NOT_SURE", "label": "Not Sure", "risk_score": 5},
            {"value": "NO", "label": "No (hidden or separate pseudonymous address)", "risk_score": 0}
        ],
        "explanation": "Personal email exposure directly fuels credential stuffing attempts and targeted spear phishing campaigns."
    },
    {
        "id": "q7",
        "category": "CAT_B",
        "question": "How is your date of birth displayed on your profile?",
        "options": [
            {"value": "FULL_BIRTHDAY", "label": "Full Birth Date (Day, Month, and Birth Year)", "risk_score": 10},
            {"value": "DAY_MONTH_ONLY", "label": "Day and Month only (Year is hidden)", "risk_score": 4},
            {"value": "HIDDEN", "label": "Hidden / Private (only visible to me)", "risk_score": 0}
        ],
        "explanation": "Full birth dates provide a crucial data element for identity theft, bank security questions, and credit fraud."
    },
    {
        "id": "q8",
        "category": "CAT_B",
        "question": "Do you publicly list your home address, specific neighborhood, or hometown street?",
        "options": [
            {"value": "YES", "label": "Yes (specific residential location or street)", "risk_score": 10},
            {"value": "CITY_ONLY", "label": "General City or Country only", "risk_score": 4},
            {"value": "NO", "label": "No home address details are shared", "risk_score": 0}
        ],
        "explanation": "Granular residential details undermine physical privacy and can be cross-referenced with public property deeds."
    },
    {
        "id": "q9",
        "category": "CAT_B",
        "question": "Do you publicly display your relationship status, spouse, or tag immediate family members?",
        "options": [
            {"value": "YES", "label": "Yes (family tree and relationship publicly tagged)", "risk_score": 8},
            {"value": "SOMETIMES", "label": "Occasional mentions without tagged relations", "risk_score": 4},
            {"value": "NO", "label": "No family or relationship information shared", "risk_score": 0}
        ],
        "explanation": "Family connections provide answers to account recovery security questions (e.g., mother's maiden name, siblings' names)."
    },

    # ------------------ CATEGORY C: Location Privacy ------------------
    {
        "id": "q10",
        "category": "CAT_C",
        "question": "Do you broadcast real-time location or use live location sharing features on social posts?",
        "options": [
            {"value": "YES", "label": "Yes (frequently broadcast live or instant location)", "risk_score": 10},
            {"value": "SOMETIMES", "label": "Occasionally during special events or outings", "risk_score": 6},
            {"value": "NO", "label": "Never (live location sharing is disabled)", "risk_score": 0}
        ],
        "explanation": "Real-time location sharing reveals when you are away from home and allows physical stalking or home burglary targeting."
    },
    {
        "id": "q11",
        "category": "CAT_C",
        "question": "When you check in at venues (restaurants, gyms, cafes), when do you publish the post?",
        "options": [
            {"value": "IMMEDIATELY", "label": "Immediately while I am still at the venue", "risk_score": 10},
            {"value": "SOMETIMES_LATER", "label": "Sometimes while present, sometimes after departure", "risk_score": 5},
            {"value": "AFTER_LEAVING", "label": "Only after leaving the venue or trip (delayed posting)", "risk_score": 1},
            {"value": "NEVER_CHECKIN", "label": "Never check in to venues", "risk_score": 0}
        ],
        "explanation": "Delayed posting ensures you have already moved on before your whereabouts become public knowledge."
    },
    {
        "id": "q12",
        "category": "CAT_C",
        "question": "Do you announce future vacation dates or upcoming travel itineraries publicly in advance?",
        "options": [
            {"value": "YES", "label": "Yes (post countdowns, tickets, or travel dates ahead of time)", "risk_score": 10},
            {"value": "SOMETIMES", "label": "Sometimes mention upcoming trips casually", "risk_score": 6},
            {"value": "NO", "label": "Never (travel photos are only posted after returning home)", "risk_score": 0}
        ],
        "explanation": "Advertising upcoming absence signals an unoccupied residence to opportunistic criminals."
    },
    {
        "id": "q13",
        "category": "CAT_C",
        "question": "Do your regular posts or stories reveal predictable daily routines (exact gym, running route, commute)?",
        "options": [
            {"value": "YES", "label": "Yes (frequent recurring route or time-stamped check-ins)", "risk_score": 9},
            {"value": "SOMETIMES", "label": "Occasional workout or commute photos", "risk_score": 5},
            {"value": "NO", "label": "No predictable schedule or routine locations are shared", "risk_score": 0}
        ],
        "explanation": "Predictable behavioral patterns create physical interception risks and enable targeted in-person social engineering."
    },
    {
        "id": "q14",
        "category": "CAT_C",
        "question": "Is automatic GPS/camera geotagging enabled for photos uploaded to social media?",
        "options": [
            {"value": "YES", "label": "Yes (camera auto-embeds GPS latitude/longitude)", "risk_score": 9},
            {"value": "NOT_SURE", "label": "Not Sure (default camera settings)", "risk_score": 6},
            {"value": "NO", "label": "No (location permissions disabled for camera app)", "risk_score": 0}
        ],
        "explanation": "Embedded EXIF GPS metadata can reveal exact home coordinates down to a few meters if uploaded unstripped."
    },

    # ------------------ CATEGORY D: Posts & Content ------------------
    {
        "id": "q15",
        "category": "CAT_D",
        "question": "What is the default audience setting configured for your new posts?",
        "options": [
            {"value": "PUBLIC", "label": "Public (anyone can view)", "risk_score": 10},
            {"value": "FRIENDS", "label": "Friends / Connections Only", "risk_score": 3},
            {"value": "CUSTOM_LISTS", "label": "Custom Restricted Lists / Close Friends only", "risk_score": 0}
        ],
        "explanation": "Setting default post audience to 'Public' creates accidental leaks for everyday personal moments."
    },
    {
        "id": "q16",
        "category": "CAT_D",
        "question": "Have you ever posted photos showing company badges, boarding passes, or computer screens?",
        "options": [
            {"value": "YES", "label": "Yes (posted badge, flight barcode, or desk workspace)", "risk_score": 10},
            {"value": "SOMETIMES", "label": "Casual desk photos where screens or papers might appear", "risk_score": 6},
            {"value": "NEVER", "label": "Never (carefully inspect background before posting)", "risk_score": 0}
        ],
        "explanation": "Boarding pass barcodes contain passenger name records (PNRs); employee badges expose facility access codes and IDs."
    },
    {
        "id": "q17",
        "category": "CAT_D",
        "question": "Do you post photos identifying minors, young children, or vulnerable family members with full names?",
        "options": [
            {"value": "YES", "label": "Yes (photos with names and school uniforms/locations)", "risk_score": 9},
            {"value": "SOMETIMES", "label": "Occasional family photos without specific school details", "risk_score": 4},
            {"value": "NO", "label": "No (minors' faces and identities are protected or kept private)", "risk_score": 0}
        ],
        "explanation": "Sharenting exposes children to digital kidnapping, unauthorized image syndication, and unconsented digital footprints."
    },
    {
        "id": "q18",
        "category": "CAT_D",
        "question": "Do you ever share answers to common security questions in viral hashtag games (first car, childhood pet)?",
        "options": [
            {"value": "YES", "label": "Yes (frequently participate in nostalgic trend prompts)", "risk_score": 9},
            {"value": "SOMETIMES", "label": "Have participated in one or two in the past", "risk_score": 5},
            {"value": "NEVER", "label": "Never (aware these match password recovery questions)", "risk_score": 0}
        ],
        "explanation": "Viral social surveys are commonly crafted by OSINT harvesters to crowd-source answers to account reset questions."
    },

    # ------------------ CATEGORY E: Friends & Followers ------------------
    {
        "id": "q19",
        "category": "CAT_E",
        "question": "How do you handle friend or follow requests from unfamiliar profiles with no mutual friends?",
        "options": [
            {"value": "ACCEPT_MOST", "label": "Accept Most (to grow network or reach)", "risk_score": 10},
            {"value": "SOMETIMES", "label": "Accept if the profile looks attractive or intriguing", "risk_score": 6},
            {"value": "VERIFY_FIRST", "label": "Investigate carefully before deciding", "risk_score": 3},
            {"value": "REJECT_UNKNOWN", "label": "Reject or ignore unfamiliar requests by default", "risk_score": 0}
        ],
        "explanation": "Fake sockpuppet profiles are standard reconnaissance tools used to bypass 'Friends-Only' privacy filters."
    },
    {
        "id": "q20",
        "category": "CAT_E",
        "question": "How frequently do you audit your followers/friends list to remove inactive or suspicious contacts?",
        "options": [
            {"value": "NEVER", "label": "Never audited my connections list", "risk_score": 9},
            {"value": "RARELY", "label": "Rarely (maybe once every few years)", "risk_score": 5},
            {"value": "REGULARLY", "label": "Regularly (at least every 6 months)", "risk_score": 0}
        ],
        "explanation": "Compromised friend accounts can remain silent in your network, covertly monitoring private posts."
    },
    {
        "id": "q21",
        "category": "CAT_E",
        "question": "Do you segment your audience using 'Close Friends' or custom privacy circles for intimate updates?",
        "options": [
            {"value": "NEVER", "label": "Never (all connections see everything)", "risk_score": 8},
            {"value": "SOMETIMES", "label": "Occasionally for sensitive personal stories", "risk_score": 4},
            {"value": "ALWAYS", "label": "Consistently use segmented lists for personal posts", "risk_score": 0}
        ],
        "explanation": "Granular audience segmentation restricts sensitive life events to trusted real-world inner circles."
    },
    {
        "id": "q22",
        "category": "CAT_E",
        "question": "Who can send you direct private messages without pre-filtering or approval?",
        "options": [
            {"value": "ANYONE", "label": "Anyone on the platform (inbox is completely open)", "risk_score": 8},
            {"value": "FILTERED_REQUESTS", "label": "Anyone, but unknown messages go to a filtered request queue", "risk_score": 3},
            {"value": "FRIENDS_ONLY", "label": "Only confirmed connections can send direct messages", "risk_score": 0}
        ],
        "explanation": "Unfiltered direct messaging opens avenues for spear-phishing payloads and malicious credential-harvesting links."
    },

    # ------------------ CATEGORY F: Tagging & Mentions ------------------
    {
        "id": "q23",
        "category": "CAT_F",
        "question": "Is 'Tag Review' (reviewing tagged posts/photos before they appear on your profile) enabled?",
        "options": [
            {"value": "NO", "label": "No (tagged posts appear automatically on my timeline)", "risk_score": 10},
            {"value": "NOT_SURE", "label": "Not Sure", "risk_score": 6},
            {"value": "YES", "label": "Yes (I must approve all tags before they appear)", "risk_score": 0}
        ],
        "explanation": "Without tag review, other users' posts can expose your location and activities even if you personally maintain strict silence."
    },
    {
        "id": "q24",
        "category": "CAT_F",
        "question": "Who is permitted to tag you in their photos, videos, and status updates?",
        "options": [
            {"value": "EVERYONE", "label": "Anyone on the platform can tag me", "risk_score": 9},
            {"value": "FRIENDS_ONLY", "label": "Only confirmed friends can tag me", "risk_score": 3},
            {"value": "NO_ONE", "label": "No one can tag me without my explicit authorization", "risk_score": 0}
        ],
        "explanation": "Unrestricted tagging allows spammers and malicious actors to link your profile to fraudulent scams and adult spam."
    },
    {
        "id": "q25",
        "category": "CAT_F",
        "question": "Is platform automated facial recognition / tag suggestion enabled for your face?",
        "options": [
            {"value": "ENABLED", "label": "Enabled (platform automatically detects and suggests tagging my face)", "risk_score": 8},
            {"value": "NOT_SURE", "label": "Not Sure", "risk_score": 5},
            {"value": "DISABLED", "label": "Disabled / Opted out of biometric facial recognition", "risk_score": 0}
        ],
        "explanation": "Biometric face grouping facilitates cross-photo indexing and passive visual tracking across unrelated accounts."
    },
    {
        "id": "q26",
        "category": "CAT_F",
        "question": "Who is allowed to @mention your username in public comments, stories, and threads?",
        "options": [
            {"value": "EVERYONE", "label": "Everyone (unrestricted mentions)", "risk_score": 7},
            {"value": "PEOPLE_I_FOLLOW", "label": "Only people I follow or know", "risk_score": 2},
            {"value": "NO_ONE", "label": "Mentions are disabled or heavily restricted", "risk_score": 0}
        ],
        "explanation": "Public mentions can be abused in mass phishing drops and harassment bot campaigns to bait quick notification clicks."
    },

    # ------------------ CATEGORY G: Authentication & Account Security ------------------
    {
        "id": "q27",
        "category": "CAT_G",
        "question": "Is Multi-Factor Authentication (MFA / 2FA) enabled on your social media account?",
        "options": [
            {"value": "DISABLED", "label": "No (Password only)", "risk_score": 10},
            {"value": "SMS_ONLY", "label": "Yes, via SMS / Text Message verification code", "risk_score": 4},
            {"value": "APP_OR_HARDWARE", "label": "Yes, using Authenticator App (TOTP) or Hardware Security Key", "risk_score": 0}
        ],
        "explanation": "MFA blocks over 90% of automated credential stuffing attacks; app-based authenticator codes protect against SIM swapping."
    },
    {
        "id": "q28",
        "category": "CAT_G",
        "question": "Is your social media account password completely unique from your other online accounts?",
        "options": [
            {"value": "REUSED", "label": "No (reused across multiple websites or email)", "risk_score": 10},
            {"value": "SLIGHT_VARIATION", "label": "Slight variation of a common base password", "risk_score": 6},
            {"value": "COMPLETELY_UNIQUE", "label": "Completely unique and strong password", "risk_score": 0}
        ],
        "explanation": "Password reuse means a breach on a random forum or shop immediately puts your primary social accounts at risk."
    },
    {
        "id": "q29",
        "category": "CAT_G",
        "question": "Do you use a dedicated password manager to generate and store high-entropy passwords?",
        "options": [
            {"value": "NO", "label": "No (memorize passwords or write them down)", "risk_score": 9},
            {"value": "BROWSER", "label": "Basic web browser built-in password autofill", "risk_score": 4},
            {"value": "PASSWORD_MANAGER", "label": "Dedicated password manager (Bitwarden, 1Password, KeePass)", "risk_score": 0}
        ],
        "explanation": "Dedicated password managers ensure compliance with password uniqueness and eliminate predictable human patterns."
    },
    {
        "id": "q30",
        "category": "CAT_G",
        "question": "Are unrecognized login alerts (instant notification on logins from new devices/IPs) turned on?",
        "options": [
            {"value": "NO", "label": "No (disabled or never checked)", "risk_score": 9},
            {"value": "NOT_SURE", "label": "Not Sure", "risk_score": 5},
            {"value": "YES", "label": "Yes (configured to send immediate email and push alerts)", "risk_score": 0}
        ],
        "explanation": "Login alerts provide rapid incident warning, allowing you to terminate an unauthorized session before takeover completes."
    },
    {
        "id": "q31",
        "category": "CAT_G",
        "question": "How often do you inspect your active logged-in sessions and revoke old connected devices?",
        "options": [
            {"value": "NEVER", "label": "Never inspected logged-in sessions", "risk_score": 8},
            {"value": "RARELY", "label": "Only when something strange happens", "risk_score": 4},
            {"value": "REGULARLY", "label": "Regularly audit and clear old sessions every few months", "risk_score": 0}
        ],
        "explanation": "Stale sessions on old laptops, school workstations, or borrowed phones can grant lingering unauthorized access."
    },

    # ------------------ CATEGORY H: Third-Party Apps ------------------
    {
        "id": "q32",
        "category": "CAT_H",
        "question": "Do you use 'Sign in with Social Account' (OAuth) on external games, websites, or apps?",
        "options": [
            {"value": "FREQUENTLY", "label": "Frequently (used on dozens of sites for convenience)", "risk_score": 9},
            {"value": "OCCASIONALLY", "label": "Occasionally on a few trusted productivity apps", "risk_score": 4},
            {"value": "RARELY_OR_NEVER", "label": "Rarely or never (prefer isolated individual credentials)", "risk_score": 0}
        ],
        "explanation": "Each connected OAuth application creates a potential supply chain bridge into your primary identity."
    },
    {
        "id": "q33",
        "category": "CAT_H",
        "question": "How frequently do you audit and revoke permissions for connected third-party applications?",
        "options": [
            {"value": "NEVER", "label": "Never reviewed connected apps list", "risk_score": 10},
            {"value": "RARELY", "label": "Once every few years", "risk_score": 5},
            {"value": "REGULARLY", "label": "Regularly prune permissions (Principle of Least Privilege)", "risk_score": 0}
        ],
        "explanation": "Zombie app integrations retain API access tokens indefinitely until explicitly revoked by the account owner."
    },
    {
        "id": "q34",
        "category": "CAT_H",
        "question": "Have you granted connected applications read/write access to your contacts, private messages, or posts?",
        "options": [
            {"value": "YES", "label": "Yes (granted broad permissions during app setup)", "risk_score": 10},
            {"value": "NOT_SURE", "label": "Not Sure what permissions were granted", "risk_score": 6},
            {"value": "NO", "label": "Strictly limited to basic email verification or denied", "risk_score": 0}
        ],
        "explanation": "Over-privileged OAuth tokens violate the Principle of Least Privilege and expose private communication history."
    },
    {
        "id": "q35",
        "category": "CAT_H",
        "question": "Do you play viral mini-games, personality quizzes, or aging filters on social platforms?",
        "options": [
            {"value": "YES", "label": "Yes (frequently try trending interactive quizzes)", "risk_score": 9},
            {"value": "SOMETIMES", "label": "Occasionally in the past", "risk_score": 5},
            {"value": "NEVER", "label": "Never (avoid third-party data harvesting quizzes)", "risk_score": 0}
        ],
        "explanation": "Viral quizzes frequently serve as data collection frontends, gathering user profiles and friend-graph intelligence."
    },

    # ------------------ CATEGORY I: Messaging & Social Engineering ------------------
    {
        "id": "q36",
        "category": "CAT_I",
        "question": "If a friend sends an unexpected DM with a link saying 'Is that you in this video?', what do you do?",
        "options": [
            {"value": "CLICK_IMMEDIATELY", "label": "Click immediately out of curiosity or alarm", "risk_score": 10},
            {"value": "INSPECT_URL", "label": "Look at the URL first, click if it looks somewhat familiar", "risk_score": 5},
            {"value": "VERIFY_OUT_OF_BAND", "label": "Never click; contact friend via alternate channel to verify", "risk_score": 0}
        ],
        "explanation": "Urgent emotional lures are the hallmark of social media credential harvester and browser malware distribution."
    },
    {
        "id": "q37",
        "category": "CAT_I",
        "question": "Would you forward a 6-digit SMS verification code to a contact claiming they sent it to you by accident?",
        "options": [
            {"value": "YES_HELP", "label": "Yes, I would help them retrieve their code", "risk_score": 10},
            {"value": "HESITATE", "label": "Might hesitate, but share if they sound very convincing", "risk_score": 6},
            {"value": "NEVER", "label": "Never (recognize this as an account takeover / MFA interception attack)", "risk_score": 0}
        ],
        "explanation": "Verification codes are meant exclusively for account holders; sharing one is direct participation in account takeover."
    },
    {
        "id": "q38",
        "category": "CAT_I",
        "question": "If a known contact contacts you on a newly created profile claiming an emergency, do you verify?",
        "options": [
            {"value": "TRUST_URGENCY", "label": "Trust them if the situation sounds urgent", "risk_score": 9},
            {"value": "REPLY_IN_DM", "label": "Ask them questions in the same DM to verify", "risk_score": 5},
            {"value": "CALL_OUT_OF_BAND", "label": "Verify via phone call or in-person before taking action", "risk_score": 0}
        ],
        "explanation": "Impersonation fraud creates false urgency to bypass critical thinking and scam contacts out of money or credentials."
    },
    {
        "id": "q39",
        "category": "CAT_I",
        "question": "Do you engage with unexpected direct messages promising free gift cards, crypto rewards, or brand collabs?",
        "options": [
            {"value": "ENGAGE_OFTEN", "label": "Yes, often click and fill out details to see if it's real", "risk_score": 10},
            {"value": "SOMETIMES", "label": "Occasionally check if from a verified-looking handle", "risk_score": 6},
            {"value": "IGNORE_AND_BLOCK", "label": "Immediately report, block, and ignore unsolicited offers", "risk_score": 0}
        ],
        "explanation": "Unsolicited giveaway DMs are primary entry points for advance-fee scams, crypto drainers, and phishing."
    },

    # ------------------ CATEGORY J: Digital Footprint ------------------
    {
        "id": "q40",
        "category": "CAT_J",
        "question": "Have you reviewed, archived, or deleted public posts and tweets made 3 or more years ago?",
        "options": [
            {"value": "NEVER", "label": "Never (my entire historical timeline is publicly open)", "risk_score": 9},
            {"value": "RARELY", "label": "Only when an old memory pops up", "risk_score": 5},
            {"value": "REGULARLY", "label": "Regularly audit and prune or bulk-privatize old posts", "risk_score": 0}
        ],
        "explanation": "Historical posts reveal past employers, schools, relationships, and evolving life details that enrich OSINT dossiers."
    },
    {
        "id": "q41",
        "category": "CAT_J",
        "question": "Do you have old, abandoned social accounts (MySpace, Tumblr, old Instagram) still active online?",
        "options": [
            {"value": "YES_MULTIPLE", "label": "Yes, multiple old accounts with forgotten passwords", "risk_score": 9},
            {"value": "MAYBE_ONE", "label": "Maybe one or two unmanaged accounts", "risk_score": 5},
            {"value": "SECURED_OR_DELETED", "label": "All dormant accounts have been deleted or secured with MFA", "risk_score": 0}
        ],
        "explanation": "Abandoned accounts lack active security monitoring and often retain outdated passwords from historical credential leaks."
    },
    {
        "id": "q42",
        "category": "CAT_J",
        "question": "Do you reuse the exact same username or handle across public forums, gaming, and professional profiles?",
        "options": [
            {"value": "SAME_EVERYWHERE", "label": "Identical handle across all gaming, social, and work platforms", "risk_score": 9},
            {"value": "SOME_OVERLAP", "label": "Some variation, but easily recognizable link", "risk_score": 5},
            {"value": "SEGREGATED", "label": "Strictly segregated pseudonyms and isolated identities", "risk_score": 0}
        ],
        "explanation": "Handle reuse enables OSINT tools like Sherlock and Maigret to instantly correlate your complete cross-platform presence."
    },
    {
        "id": "q43",
        "category": "CAT_J",
        "question": "How often do you proactively audit platform privacy settings after major terms of service updates?",
        "options": [
            {"value": "NEVER", "label": "Never recheck privacy settings once created", "risk_score": 8},
            {"value": "YEARLY", "label": "Only when headlines warn about privacy changes", "risk_score": 4},
            {"value": "REGULARLY", "label": "Conduct routine privacy checks every quarter", "risk_score": 0}
        ],
        "explanation": "Social platforms regularly introduce new sharing features and reset default toggles during platform updates."
    },
    {
        "id": "q44",
        "category": "CAT_J",
        "question": "Have you ever downloaded and inspected your personal data archive from the platform?",
        "options": [
            {"value": "NEVER", "label": "Never downloaded or inspected my data archive", "risk_score": 7},
            {"value": "AWARE_BUT_NOT_DONE", "label": "Aware the feature exists, but haven't done it", "risk_score": 4},
            {"value": "DOWNLOADED_AND_REVIEWED", "label": "Yes, downloaded and reviewed stored telemetry and ad categories", "risk_score": 0}
        ],
        "explanation": "Data archives reveal how platforms track location telemetry, search queries, and third-party ad profiling categories."
    }
]

# Quick lookup map by question ID
QUESTION_MAP = {q["id"]: q for q in QUESTIONS}

# Weights map by category ID
CATEGORY_WEIGHTS = {cat_id: cat["weight"] for cat_id, cat in CATEGORIES.items()}
