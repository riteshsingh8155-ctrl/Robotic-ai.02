import os
import requests
from smartapi import SmartConnect
import pyotp

# GitHub/Replit ke "Secrets" se uthayega
API_KEY = os.getenv("API_KEY")
CLIENT_CODE = os.getenv("CLIENT_CODE")
PASSWORD = os.getenv("PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

try:
    send_telegram("🤖 Bot Start ho raha hai...")
    totp_input = input("Angel App ka 6 digit TOTP code daal: ")
    
    smartApi = SmartConnect(api_key=API_KEY)
    data = smartApi.generateSession(CLIENT_CODE, PASSWORD, totp_input)

    if data['status']:
        print("Login Success")
        send_telegram("✅ Login Success ho gaya bhai!")
    else:
        print("Login Fail:", data['message'])

except Exception as e:
    print("Error:", e)
name: Frontstage Pages

on:
  workflow_dispatch:
  pull_request:
    paths:
      - ".github/workflows/frontstage-pages.yml"
      - "apps/presentation/dashboard/**"
      - "apps/presentation/site/**"
      - "docs/showcases/**"
      - "docs/assets/long-running-loop-openviking-trajectory.png"
      - "docs/assets/long-running-loop-ml-experiment-trajectory.png"
      - "examples/export-frontstage-share-bundle.mjs"
      - "examples/frontstage-share-bundle-smoke.mjs"
      - "examples/goal-channel-frontstage-fixture.py"
      - "examples/showcase-catalog-smoke.py"
      - "examples/status.example.json"
  push:
    branches:
      - main
    paths:
      - ".github/workflows/frontstage-pages.yml"
      - "apps/presentation/dashboard/**"
      - "apps/presentation/site/**"
      - "docs/showcases/**"
      - "docs/assets/long-running-loop-openviking-trajectory.png"
      - "docs/assets/long-running-loop-ml-experiment-trajectory.png"
      - "examples/export-frontstage-share-bundle.mjs"
      - "examples/frontstage-share-bundle-smoke.mjs"
      - "examples/goal-channel-frontstage-fixture.py"
      - "examples/showcase-catalog-smoke.py"
      - "examples/status.example.json"

permissions:
  actions: read
  contents: read
  pages: write
  id-token: write

concurrency:
  group: frontstage-pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v7

      - name: Set up Node
        uses: actions/setup-node@v6
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: apps/presentation/dashboard/package-lock.json

      - name: Use stable npm
        run: npm install -g npm@11

      - name: Install dashboard dependencies
        working-directory: apps/presentation/dashboard
        run: npm ci --include=dev --no-audit --no-fund --registry=https://registry.npmjs.org

      - name: Validate public showcase catalog
        run: python3 examples/showcase-catalog-smoke.py

      - name: Validate public-safe frontstage bundle
        working-directory: apps/presentation/dashboard
        run: npm run smoke:frontstage-share-bundle

      - name: Export Pages frontstage artifact
        working-directory: apps/presentation/dashboard
        run: npm run export:frontstage-share -- --base /loopx/ --out-dir ../../../output/frontstage-pages

      - name: Configure Pages
        if: github.event_name != 'pull_request'
        uses: actions/configure-pages@v6
        with:
          enablement: true

      - name: Upload Pages artifact
        if: github.event_name != 'pull_request'
        uses: actions/upload-pages-artifact@v5
        with:
          path: output/frontstage-pages/site

  deploy:
    if: github.event_name != 'pull_request'
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to Pages
        id: deployment
        uses: actions/deploy-pages@v5
