# ni5arga: Post-Blog Vulnerability Disclosures

**Researcher:** [@ni5arga](https://x.com/ni5arga) (nisarga) — 19-year-old security researcher
**Full blog post:** [ni5arga.com/blog/posts/hacking-cbse](https://ni5arga.com/blog/posts/hacking-cbse/) (published May 22, 2026)

---

## What's Already Blogged

ni5arga's [blog post](https://ni5arga.com/blog/posts/hacking-cbse/) documents five vulnerabilities discovered on **February 25, 2026** and reported to CERT-In under ref **CERTIn-16590126**:

1. **Hardcoded master password** in the Angular JS bundle
2. **Client-side OTP validation** — server sends OTP in the auth response, browser checks locally
3. **No route guards** — entire app navigable without authentication
4. **Password change without old password** — `ChangePassword` API never sends `oldpassword`
5. **Systemic IDOR** — every API trusts `ValuatorID` from client-side storage

These are well-documented in his blog. **This page covers only what came after.**

---

## Post-Blog Timeline (May 27–31, 2026)

### 🔴 Finding 6: Full CRUD + Shell Access on CBSE Prod Servers
**Date:** May 29, 2026
**Tweet:** [x.com/i/status/2060320391617499380](https://x.com/i/status/2060320391617499380)

ni5arga (with @thetirthparmar) demonstrated **full create, read, update, delete access plus shell access** to CBSE's production OnMark server — the same server referenced in [CBSE's own circular](https://archive.is/dGw1Q).

- Proof archive: [archive.is/bPH2U](https://archive.is/bPH2U)
- Additional archives: [archive.is/lkI1x](https://archive.is/lkI1x), [archive.is/UWp2h](https://archive.is/UWp2h)
- Reported to CERT-In, Education Ministry (GoI), and CBSE before disclosure

**Bad Apple demo:** [x.com/i/status/2060329287367147795](https://x.com/i/status/2060329287367147795) — Played the Bad Apple video on the CBSE production site as proof of control.

---

### 🔴 Finding 7: Super Admin Access on OnMark University Portal
**Date:** May 29, 2026
**Tweets:**
- [x.com/i/status/2060508071072592306](https://x.com/i/status/2060508071072592306)
- [x.com/i/status/2060508201439875477](https://x.com/i/status/2060508201439875477)
- [x.com/i/status/2060508407522857172](https://x.com/i/status/2060508407522857172)

Another OnMark subdomain was compromised, this time granting **super admin access** to a portal handling exam evaluation at **multiple universities**.

Capabilities obtained:
- **Evaluate/grade answer sheets**
- **Edit any user's password**
- **View full user list**
- **Create new user accounts**
- **Send mass SMS and email** to all evaluators/students

> "another integral onmark subdomain has been pwn'ed, this time we managed to get super admin access of the portal. seems like it is tasked with evaluation of exams at various universities."

CERT-In informed before posting. This reveals the vulnerability is **not CBSE-specific** — it's systemic across the entire OnMark platform used by multiple institutions.

---

### 🔴 Finding 8: Exposed AWS S3 Bucket — Answer Sheets & Question Papers
**Date:** May 31, 2026
**Tweet:** [x.com/i/status/2060941174949433445](https://x.com/i/status/2060941174949433445) (476K+ views)

CBSE's AWS S3 bucket was left **completely unauthenticated**:

- `ListObjectsV2` works **without any authentication**
- Bucket root is **publicly listable**
- Contains **2026 answer sheets and question papers** as scanned images
- Allows **pagination and enumeration** of all media
- **Multiple institutions** share the same bucket

> "CBSE people didn't configure their AWS bucket properly and now we can paginate & enumerate all their media which has 2026 answersheets & question papers. ListObjectsV2 works without any auth and the bucket root is listable too — anyone on the internet can download any scanned booklet — across institutions. Multiple institutions are using the same bucket, insanely insecure."

This is arguably the most damaging disclosure — it means **anyone on the internet** could download any student's scanned answer booklet without any authentication whatsoever, across multiple institutions using the OnMark/Coempt infrastructure.

---

## CBSE's Response

**May 31, 2026** — CBSE issued an official statement from HQ acknowledging a security breach and deploying cybersecurity teams:

> [CBSE HQ statement](https://x.com/ni5arga/status/2061042510211027189)

ni5arga's reaction: [x.com/i/status/2061042510211027189](https://x.com/i/status/2061042510211027189)

On CERT-In's response: [x.com/i/status/2060987304681115795](https://x.com/i/status/2060987304681115795)

> "CERT just sends me a boilerplate 'thank you' reply every time and it's frustrating to say the least."

---

## What This Tells Us

| Finding | Blogged? | Scope | Severity |
|---------|---------|-------|----------|
| Hardcoded master password | ✅ Yes | CBSE OSM portal | Critical |
| Client-side OTP | ✅ Yes | CBSE OSM portal | Critical |
| No route guards | ✅ Yes | CBSE OSM portal | High |
| Password change w/o old | ✅ Yes | CBSE OSM portal | Critical |
| Systemic IDOR | ✅ Yes | CBSE OSM portal | Critical |
| CRUD + Shell on prod | ❌ New | CBSE production | Critical |
| Super admin (university) | ❌ New | OnMark platform-wide | Critical |
| Exposed S3 bucket | ❌ New | Multi-institutional | Critical |

**The post-blog findings escalate the scope dramatically:**
- **Blog findings:** CBSE-specific, require some technical knowledge to exploit
- **Post-blog findings:** Platform-wide (OnMark), some require **zero technical skill** (the S3 bucket is publicly listable), and affect **multiple institutions** beyond CBSE

The S3 disclosure alone means every student's answer sheet across every institution using this infrastructure was downloadable by anyone on the internet.

---

## Media Coverage

ni5arga's blog has been covered by:
- [India Today](https://www.indiatoday.in/education-today/news/story/cbse-osm-portal-vulnerability-claims-surface-with-teens-detailed-blog-post-2917243-2026-05-26)
- [BBC News](https://www.bbc.com/news/articles/cy42e8eljpno)
- [NDTV](https://www.ndtv.com/education/cbse-osm-portal-had-critical-vulnerabilities-ethical-hacker-told-ndtv-he-alerted-board-months-earlier-11550090)
- [ThePrint](https://theprint.in/feature/19-student-hacked-cbses-osm-portal-vulnerabilities/2942305/)
- [IFF Blog](https://internetfreedom.in/when-the-exam-itself-can-be-hacked-iff-writes-to-the-ministry-of-education-and-cert-in-on-the-cbse-on-screen-marking-disclosure/)
- [Medianama](https://www.medianama.com/2026/05/223-cert-in-vulnerabilities-cbse-online-marking-portal/)
- And [14 more outlets](https://ni5arga.com/blog/posts/hacking-cbse/#media-coverage)
