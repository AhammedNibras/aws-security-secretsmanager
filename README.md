# Securing Secrets with AWS Secrets Manager Lab

## Overview

- Deploy insecure web app that lists S3 buckets using hardcoded AWS credentials.
- Attempt GitHub push and get blocked by secret scanning.
- Store credentials in AWS Secrets Manager.
- Update app to retrieve secrets securely via boto3.
- Clean Git history and make code public safely.

![Image](http://learn.nextwork.org/overjoyed_silver_glamorous_cape_gooseberry/uploads/aws-security-secretsmanager_r7s8t9u0)

---

## What This Project Covers

Hands-on security lab showing insecure credential storage and AWS Secrets Manager fix.

- **Goal of hardcoded credentials** - Start with web app using `config.py` with plain AWS keys to list S3 buckets.
- **Goal of GitHub scanning** - See push blocked when secrets detected in code.
- **Goal of Secrets Manager** - Centralize credentials, retrieve at runtime.
- Kill chain: code leak → scanning block → secure storage → clean history.

---

## Why Secure Secrets

Exposed AWS keys in GitHub = instant account compromise. Single leaked AccessKeyId lets attackers delete S3 data, spin up EC2, rack up bills.

This lab shows:

- **Insecure approach**: Hardcode → push → blocked (but damage already in local commits).
- **Secure approach**: Secrets Manager + Git rebase = production-ready secure app.

---

## 1. Project Setup

**Log into AWS Console** (IAM Admin, pick region with S3 buckets).

**Clone & Run Insecure App**:

```
git clone https://github.com/AhammedNibras/aws-security-secretsmanager.git
cd aws-security-secretsmanager
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

**Add real AWS keys to config.py** (create IAM access key, Local code use case).

- Go to IAM → select your IAM user → navigate to Access keys → click Create access key.

- Download the access keys or securely note them down to update later in `config.py`.

```
nano config.py
```

- Paste the **Access Key ID**, **Secret Access Key**, and the **AWS region** you are currently using into their respective fields.

**Test**: `python3 app.py` → http://0.0.0.0:8000 → "View My S3 Buckets" shows bucket names.

![Image](http://learn.nextwork.org/overjoyed_silver_glamorous_cape_gooseberry/uploads/aws-security-secretsmanager_wghjteykut)

---

## 2. Make Code Public (Get Blocked)

**Fork repo** on GitHub: **[aws-security-secretsmanager](https://github.com/AhammedNibras/aws-security-secretsmanager)**.

**Push with secrets**:

```
git init # or skip if exists
git remote set-url origin https://github.com/YOUR_USERNAME/aws-security-secretsmanager.git
git add .
git commit -m "Add hardcoded AWS credentials"
git push -u origin main
```

**Result**: GitHub blocks → "Push cannot contain secrets" (scans for AWS key patterns).

![Image](http://learn.nextwork.org/overjoyed_silver_glamorous_cape_gooseberry/uploads/aws-security-secretsmanager_o2p3q4r5)

---

## 3. Store Credentials in Secrets Manager

**AWS Console** → Secrets Manager → Store new secret:

- **Secret type**: Other type of secret
- **Key/value**: `AWS_ACCESS_KEY_ID`/`your-key`, `AWS_SECRET_ACCESS_KEY`/`your-secret`, `AWS_REGION`/`your-region`
- **Secret name**: `aws-access-key`
- Copy **Python 3 sample code**.

![Image](http://learn.nextwork.org/overjoyed_silver_glamorous_cape_gooseberry/uploads/aws-security-secretsmanager_h2i3j4k5)

---

## 4. Update App to Use Secrets Manager

**Replace config.py** with AWS Secrets Manager Python 3 sample code + this block:

```
    return json.loads(secret)

# Retrieve credentials from Secrets Manager
credentials = get_secret()

# Extract the values; if AWS_REGION isn't in the secret, use the region from the session
AWS_ACCESS_KEY_ID = credentials.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = credentials.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = credentials.get("AWS_REGION", boto3.session.Session().region_name or "us-east-2")
```

![Image](http://learn.nextwork.org/overjoyed_silver_glamorous_cape_gooseberry/uploads/aws-security-secretsmanager_v0w1x2y3)

**Update config.py** by adding `import json` at the beginning of the python script

**Test**: `python3 app.py` → lists S3 buckets (now from Secrets Manager).

---

## 5. Clean Git History & Push Secure Version

```
git add config.py
git commit -m "Use AWS Secrets Manager for credentials"
git rebase -i --root
```

- Mark "Add hardcoded AWS credentials" commit as 'drop'

![Image](http://learn.nextwork.org/overjoyed_silver_glamorous_cape_gooseberry/uploads/aws-security-secretsmanager_t5u6v7w8)

- Resolve conflicts: keep Secrets Manager version

```
git push -u origin main
```

**Verify**: GitHub shows clean `config.py` (no keys), history scrubbed.

---

## 6. Cleanup

- Stop app: Ctrl+C

```
deactivate # Exit venv
```

- Delete IAM access key
- Delete Secrets Manager secret
- Delete fork repo

```
rm -rf aws-security-secretsmanager
```

---

## Files in This Repository

- `app.py` - FastAPI app listing S3 buckets.
- `config.py` - Secure secrets retrieval (final version).
- `requirements.txt` - Dependencies (boto3, fastapi, uvicorn).

---

## Skills Demonstrated

**AWS**: Secrets Manager, IAM keys, S3, boto3.  
**DevOps**: Git rebase, GitHub secret scanning, virtualenv.  
**Security**: Never commit secrets, runtime retrieval, history rewriting.
