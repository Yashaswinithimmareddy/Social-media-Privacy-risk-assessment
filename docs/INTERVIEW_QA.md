# Cybersecurity & Privacy Engineering Interview Preparation Guide
**10 High-Impact Technical Questions & Expert Student Answers**

---

### Question 1: Explain your project.
**Candidate Answer:**
"I built the **Social Media Privacy Risk Assessment Framework**, a defensive cybersecurity platform that quantifies, analyzes, and remediates social media exposure and digital footprint vulnerabilities. 

In cybersecurity, we often focus on perimeter firewalls and encryption, but human behavioral exposure on social platforms represents a massive unmonitored attack surface. My framework evaluates self-reported privacy settings across 10 critical vectors—including Profile Visibility, Personal Contact Information, Location Privacy, Account Security, Third-Party OAuth Apps, and Social Engineering susceptibility—using a 44-question assessment engine.

The system processes these responses through a normalized risk scoring pipeline that computes category-wise and overall exposure scores from 0 to 100, assigns standardized risk tiers (Low, Moderate, High, Critical), detects specific technical findings, and generates prioritized remediation steps. 

A standout feature is the **Privacy Improvement Simulator**, which allows users to interactively test hardening actions—such as privatizing phone numbers or enabling MFA—and visually see the simulated risk reduction in real time. Crucially, the entire system is built on **Privacy by Design**: it never collects real phone numbers, passwords, or emails, and performs zero intrusive web scraping, evaluating exposure purely through defensive risk modeling."

---

### Question 2: What is the fundamental difference between Privacy and Security, and how does your project demonstrate that?
**Candidate Answer:**
"A common misconception is that strong security equals strong privacy. **Security** is focused on the confidentiality, integrity, and availability (CIA) of systems and data—protecting accounts against unauthorized access or breaches. **Privacy**, on the other hand, governs how personal information is collected, disclosed, shared, and utilized when authorized.

In my project, this contrast is explicitly demonstrated: an individual can have a 30-character complex passphrase, a hardware security key, and active login alerts—giving them a near-perfect Account Security score. However, if that same individual publicly broadcasts their phone number, live venue check-ins, and full date of birth on their bio, their Personal Information and Location Privacy scores are critically vulnerable. 

High account security does not stop an OSINT investigator or stalker from legally scraping public details to launch spear-phishing or SIM-swapping attacks. My framework evaluates both dimensions independently."

---

### Question 3: How does an individual's digital footprint contribute to cyber threats, and how does your framework categorize it?
**Candidate Answer:**
"A digital footprint consists of two components: **active footprints** (information deliberately shared, such as posts, tweets, and comments) and **passive footprints** (data gathered via platform telemetry, IP addresses, and browsing patterns). 

In my framework, Category J focuses specifically on the active historical footprint. Threat actors use OSINT tools like Sherlock and SpiderFoot to map historical posts dating back 5 to 10 years. Old posts often leak past employers, high school names, pet names, and former residential cities—which directly match automated password recovery security questions. Furthermore, dormant abandoned accounts on older platforms frequently retain compromised credentials from historical breaches. My framework assesses post archiving cadence, username reuse across platforms, and dormant account hygiene to minimize this reconnaissance surface."

---

### Question 4: How does oversharing on social media enable targeted social engineering attacks?
**Candidate Answer:**
"Social engineering attacks rely on credibility, urgency, and context. Publicly available social media data provides the reconnaissance material needed to build high-fidelity pretexts. 

For instance, if an employee posts an office desk photo showing a company lanyard or internal monitor, an adversary learns internal software names and company terminology. If they broadcast that they are boarding an international flight, an attacker can launch an executive impersonation attack against their accounting department or family, claiming an urgent financial emergency while knowing the victim is in transit and unable to answer their phone. 

My framework evaluates behaviors like accepting stranger requests, posting travel itineraries in advance, and responding to emotional direct messages, helping users understand that exposure fuels adversary deception."

---

### Question 5: How does your risk scoring engine calculate the overall score, and why did you choose that weighting model?
**Candidate Answer:**
"The scoring engine operates in three stages:
1. **Feature Extraction:** Raw responses are converted into standardized penalty scores from 0 to 10 based on predefined risk weights.
2. **Category-Wise Normalization:** Scores for each category (CAT_A through CAT_J) are summed against their respective question counts and scaled to a standard 0 to 100 range.
3. **Composite Weighted Risk Score:** The overall score is computed using normalized weights:
   - Account Security (15%), Location Privacy (15%), and Personal Information (15%) receive the highest weights because their compromise leads directly to account takeover, physical danger, or identity theft.
   - Profile Visibility (10%), Posts/Content (10%), Friends Controls (10%), and Social Engineering (10%) represent moderate attack vectors.
   - Tagging (5%), Third-Party Apps (5%), and Digital Footprint (5%) represent targeted exposure vectors.

The resulting score is mapped to industry tiers: 0–20 is Low, 21–40 is Moderate, 41–70 is High, and 71–100 is Critical. The weights are configurable, allowing organizations to tailor them to enterprise policies."

---

### Question 6: How did you implement Privacy by Design and Data Minimization in this project?
**Candidate Answer:**
"From day one, the architecture was designed to enforce GDPR Article 5 and Article 25 principles. 
First, **Data Minimization:** rather than asking users to input their actual phone number, home address, or birthday, the questionnaire asks qualitative binary exposure questions: *'Is your phone number visible on your public bio? [YES / NO]'*. This allows risk scoring without ingesting any actual sensitive PII.

Second, **Purpose Limitation and Storage Limitation:** the SQLite database schema strictly stores assessment IDs, numerical category scores, finding tokens, and timestamps. No names, IP addresses, or contact information are stored.

Third, **Right to Erasure (GDPR Article 17):** I implemented a dedicated `DELETE /api/assessment/<id>` endpoint that permanently wipes all traces of an assessment upon user request."

---

### Question 7: Why is SMS-based MFA considered insecure compared to App-Based TOTP or Hardware Security Keys?
**Candidate Answer:**
"SMS-based multi-factor authentication relies on the public switched telephone network (PSTN), which was never designed for cryptographically secure authentication. SMS codes are susceptible to:
1. **SIM-Swapping:** An attacker uses social engineering against mobile telecom support to port the victim's phone number to a rogue SIM card.
2. **SS7 Protocol Vulnerabilities:** Global telecom signaling protocols (SS7) have known routing interception flaws that allow sophisticated actors to intercept SMS traffic.
3. **Phishing Proxies (Evilginx):** Reverse-proxy phishing kits can intercept temporary SMS OTPs in real time.

In my framework, Q27 awards SMS MFA a risk penalty of 4/10, while Authenticator Apps (RFC 6238 TOTP) or FIDO2 hardware keys receive 0/10 risk, guiding users toward phishing-resistant authentication."

---

### Question 8: What are the security risks associated with third-party OAuth application integrations?
**Candidate Answer:**
"When users click *'Sign in with Social Profile'*, OAuth 2.0 grants an access token and refresh token with specific permission scopes (e.g., reading friends lists, email, or publishing posts).

The primary risk is **supply chain compromise and persistence**. If an external mobile game or quiz developer suffers a database breach, attackers can abuse the stored OAuth tokens to access the user's social profile without ever needing their password or triggering MFA. Furthermore, users rarely audit connected apps, creating *zombie integrations* that retain access for years. My framework evaluates third-party app review cadence and excessive permission scopes, enforcing the Principle of Least Privilege."

---

### Question 9: How did you ensure the application itself does not introduce security vulnerabilities (AppSec)?
**Candidate Answer:**
"I implemented defensive application security controls across the stack:
- **HTTP Security Headers:** Implemented middleware enforcing `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and strict `Content-Security-Policy` (CSP) to mitigate cross-site scripting (XSS) and clickjacking.
- **Input Sanitization:** The assessment engine validates and sanitizes all incoming JSON request keys against an explicit whitelist of allowed question tokens, dropping unwhitelisted keys.
- **Local-Only EXIF Inspection:** For the photo metadata inspection tool, files are processed entirely in memory via Pillow. The binary is never written to temporary disk folders or transmitted externally, and the sanitizer cleanly reconstructs pixel arrays to strip metadata."

---

### Question 10: How did you validate and test your framework?
**Candidate Answer:**
"I built a comprehensive automated test suite with **33 unit and integration tests** using `pytest`. 

The tests cover:
- Boundary conditions (verifying score transitions at 20.0, 40.0, and 70.0).
- Extreme profile benchmarks (asserting that a completely private profile scores <= 15 and is marked Low, while a fully public insecure profile scores >= 85 and is marked Critical).
- Specific finding triggers (verifying that phone exposure generates `FIND_PHONE_PUBLIC` with Critical severity).
- Recommendation mapping and priority sorting (Immediate vs Important).
- The simulation engine's point reduction accuracy.
- Database schema inspection to verify zero PII columns exist.
- API endpoints and GDPR data deletion.

In our automated runs, all 33 tests pass in under 1 second with zero warnings."
