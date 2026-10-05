# Defensive Threat Model: Social Media Privacy & Identity Exposure

## 1. Executive Summary
This threat model analyzes the exposure surfaces of individual users on mainstream social media platforms. It adopts a **defensive posture**, mapping digital footprints and user behaviors to adversary reconnaissance tactics and social engineering methodologies.

---

## 2. Protected Assets

| Asset ID | Asset Name | Description & Sensitivity |
| :--- | :--- | :--- |
| **A-01** | **Primary Account Access** | Control over social identity, messaging channels, and account management tokens. |
| **A-02** | **Personal Identity Information** | Full legal name, date of birth, mother's maiden name, and home address. |
| **A-03** | **Direct Contact Channels** | Verified mobile phone number and primary personal email address. |
| **A-04** | **Physical Location Privacy** | Real-time presence, residential location, vacation schedules, and daily routines. |
| **A-05** | **Private Communications & Media** | Direct message histories, unlisted family photos, and confidential documents. |
| **A-06** | **Social Trust Graph** | Friends list, professional hierarchy, and family associations. |

---

## 3. Threat Actors & Capabilities

| Threat Actor | Motivation | Capabilities & Tactics |
| :--- | :--- | :--- |
| **OSINT Harvester / Data Broker** | Commercial monetization, automated profiling | Automated scrapers, cross-platform username correlation (Sherlock/Maigret), search engine indexing. |
| **Opportunistic Scammer / Phisher** | Financial fraud, account theft | Mass DM spam, credential phishing lures ("Is that you in this video?"), OTP forwarding scams. |
| **Targeted Spear-Phisher / Social Engineer** | Corporate espionage, executive impersonation | Deep reconnaissance using family trees, workplace badges, boarding pass barcodes, and travel itineraries. |
| **Physical Burglary / Stalker Threat** | Real-world physical crime, harassment | Pattern-of-life analysis via live venue check-ins, routine workout routes, and advance vacation broadcasts. |

---

## 4. Threat Matrix: Asset Exposure & Defensive Controls

### T-01: Credential Stuffing & Account Takeover
- **Target Asset:** A-01 (Account Access)
- **Vulnerability/Exposure:** Single-factor authentication (Password only) combined with password reuse across third-party websites.
- **Threat Scenario:** A breach at an unrelated e-commerce website leaks password hashes. Adversaries run automated credential stuffing attacks against the social media account.
- **Potential Impact:** High. Unauthorized account takeover, unauthorized messaging to friends, identity theft.
- **Existing Control:** Basic platform password complexity requirements.
- **Recommended Hardening:** Enable app-based Multi-Factor Authentication (TOTP / Hardware Security Key) and utilize a dedicated password manager for unique 16+ character passphrases.

---

### T-02: SIM-Swapping & Telecommunication Hijacking
- **Target Asset:** A-01, A-03 (Phone & Account Access)
- **Vulnerability/Exposure:** Mobile phone number publicly displayed on user bio or contact button.
- **Threat Scenario:** An adversary harvests the phone number, conducts OSINT to gather birthday and full name, and deceives the mobile carrier into porting the SIM card to the attacker's device.
- **Potential Impact:** Critical. Interception of SMS two-factor authentication codes and complete account hijacking across financial and social accounts.
- **Existing Control:** Carrier PIN codes (often bypassable via social engineering).
- **Recommended Hardening:** Remove mobile phone numbers from public visibility; switch from SMS-based MFA to Authenticator Apps (TOTP).

---

### T-03: Real-Time Burglary & Physical Interception
- **Target Asset:** A-04 (Location Privacy)
- **Vulnerability/Exposure:** Publishing real-time venue check-ins and public countdowns to upcoming vacations.
- **Threat Scenario:** Adversaries identify that the residence is completely vacant during an announced two-week overseas holiday.
- **Potential Impact:** High. Physical home burglary, property theft, or physical stalking at predictable daily gym/running routes.
- **Existing Control:** None at platform layer.
- **Recommended Hardening:** Adopt delayed posting policies (publish vacation highlights only after returning home); disable camera EXIF geotagging; avoid recurring route posts.

---

### T-04: Security Question Enumeration via Nostalgia Lures
- **Target Asset:** A-02, A-06 (Identity & Trust Graph)
- **Vulnerability/Exposure:** Publicly participating in viral hashtag challenges (e.g., "My first car", "High school mascot", "Mother's maiden name hint").
- **Threat Scenario:** Adversaries query bank or email account recovery flows, cross-referencing public quiz responses to answer automated security questions.
- **Potential Impact:** High. Password resets triggered without direct credential theft.
- **Existing Control:** Rate limiting on password resets.
- **Recommended Hardening:** Treat security questions as secondary passwords by supplying random alphanumeric strings stored in password managers; avoid viral nostalgia surveys.

---

### T-05: OAuth Supply Chain & Overprivileged Token Abuse
- **Target Asset:** A-01, A-05 (Account & Communications)
- **Vulnerability/Exposure:** Connecting dozens of third-party mobile games, personality quizzes, and viral utilities via "Sign in with Social Profile".
- **Threat Scenario:** A third-party developer's database is compromised or sold. Stored OAuth tokens allow unauthorized access to user contacts and profile details.
- **Potential Impact:** Moderate to High. Silent long-term data exfiltration under valid API permissions.
- **Existing Control:** Periodic platform token expiration.
- **Recommended Hardening:** Enforce the Principle of Least Privilege: conduct a quarterly audit of connected OAuth applications and revoke all unused integrations.

---

## 5. Defensive Risk Heatmap Summary

| Threat ID | Threat Name | Likelihood | Impact | Overall Inherent Risk | Residual Risk (Post-Hardening) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **T-01** | Account Takeover (No MFA) | HIGH | CRITICAL | **CRITICAL** | LOW |
| **T-02** | SIM-Swap via Public Phone | MEDIUM | CRITICAL | **HIGH** | LOW |
| **T-03** | Vacant Home Burglary (Location) | MEDIUM | HIGH | **HIGH** | LOW |
| **T-04** | Security Question Reset | HIGH | MEDIUM | **HIGH** | LOW |
| **T-05** | OAuth Third-Party Token Breach | MEDIUM | MEDIUM | **MODERATE** | LOW |
| **T-06** | Historical OSINT Correlation | HIGH | LOW | **MODERATE** | LOW |
