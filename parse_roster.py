#!/usr/bin/env python3
import re
import csv
import html as htmlmod
from pathlib import Path

IN = Path('roster_page.html')
OUT = Path('roster.csv')
BASE = 'https://hurstathletics.com'

def clean(s):
    return htmlmod.unescape(s).strip()

def parse_with_bs4(content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    blocks = soup.find_all('div', class_='sidearm-roster-player-header-details')
    players = []
    for b in blocks:
        number_tag = b.find('span', class_='sidearm-roster-player-jersey-number')
        number = clean(number_tag.get_text()) if number_tag else ''
        name_tag = b.find('span', class_='sidearm-roster-player-name')
        first = last = ''
        if name_tag:
            spans = name_tag.find_all('span')
            if len(spans) >= 1:
                first = clean(spans[0].get_text())
            if len(spans) >= 2:
                last = clean(spans[1].get_text())

        fields = {}
        for dl in b.find_all('dl'):
            dts = dl.find_all('dt')
            dds = dl.find_all('dd')
            for dt, dd in zip(dts, dds):
                fields[clean(dt.get_text()).rstrip(':')] = clean(dd.get_text())

        players.append({
            'position': fields.get('Position', ''),
            'weight': fields.get('Weight', ''),
            'height': fields.get('Height', ''),
            'hometown': fields.get('Hometown', ''),
            'class': fields.get('Class', ''),
            'highschool': fields.get('High School', ''),
            'number': number,
            'first_name': first,
            'last_name': last,
        })
    return players

def parse_with_regex(content):
    parts = re.split(r'<div[^>]*class="sidearm-roster-player-header-details', content)
    if len(parts) <= 1:
        return []
    players = []
    for part in parts[1:]:
        txt = part
        number_m = re.search(r'<span[^>]*class="sidearm-roster-player-jersey-number"[^>]*>(.*?)</span>', txt, re.S)
        number = clean(number_m.group(1)) if number_m else ''

        name_m = re.search(r'<span[^>]*class="sidearm-roster-player-name"[^>]*>.*?<span>([^<]+)</span>.*?<span>([^<]+)</span>', txt, re.S)
        first = clean(name_m.group(1)) if name_m else ''
        last = clean(name_m.group(2)) if name_m else ''

        items = re.findall(r'<dt>\s*([^<:]+):\s*</dt>\s*<dd>\s*([^<]+?)\s*</dd>', txt, re.S)
        fields = {k.strip(): v.strip() for k, v in items}

        players.append({
            'position': fields.get('Position', ''),
            'weight': fields.get('Weight', ''),
            'height': fields.get('Height', ''),
            'hometown': fields.get('Hometown', ''),
            'class': fields.get('Class', ''),
            'highschool': fields.get('High School', ''),
            'number': number,
            'first_name': first,
            'last_name': last,
        })
    return players

def extract_profiles(roster_html):
    """Return list of (rp_id, full_url) extracted from roster HTML."""
    profiles = {}
    for m in re.finditer(r'"url"\s*:\s*"([^"]*roster\.aspx\?rp_id=([0-9]+))"', roster_html):
        u = m.group(1)
        rid = m.group(2)
        if u.startswith('http'):
            full = u
        else:
            full = BASE + u if u.startswith('/') else BASE + '/' + u
        profiles[rid] = full

    # fallback: hrefs
    for m in re.finditer(r'href=["\'](/roster\.aspx\?rp_id=([0-9]+))["\']', roster_html):
        u = m.group(1)
        rid = m.group(2)
        if rid not in profiles:
            profiles[rid] = BASE + u

    # return list of tuples sorted by rp_id (numeric)
    return sorted([(int(k), v) for k, v in profiles.items()], key=lambda x: x[0])

def extract_names_from_roster_html(roster_html):
    """Extract mapping rp_id -> (first, last) from LD+JSON on roster page."""
    mapping = {}
    for m in re.finditer(r'\{[^}]*"@type"\s*:\s*"Person"[^}]*"name"\s*:\s*"([^"]+)"[^}]*"url"\s*:\s*"([^"]*rp_id=([0-9]+)[^"]*)"', roster_html, re.S):
        fullname = m.group(1).strip()
        rid = m.group(3)
        parts = fullname.split()
        first = parts[0] if parts else ''
        last = ' '.join(parts[1:]) if len(parts) > 1 else ''
        mapping[int(rid)] = (first, last)
    return mapping

def fetch(url):
    import urllib.request
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode('utf-8', errors='ignore')

def parse_player_page(html_text):
    # parse the player page snippet (similar to html.txt)
    # number
    number_m = re.search(r'<span[^>]*class="sidearm-roster-player-jersey-number"[^>]*>([^<]*)</span>', html_text, re.S)
    number = clean(number_m.group(1)) if number_m else ''
    # name
    name_m = re.search(r'<span[^>]*class="sidearm-roster-player-name"[^>]*>.*?<span>([^<]+)</span>\s*<span>([^<]+)</span>', html_text, re.S)
    first = clean(name_m.group(1)) if name_m else ''
    last = clean(name_m.group(2)) if name_m else ''
    # dt/dd pairs
    items = re.findall(r'<dt>\s*([^<:]+):\s*</dt>\s*<dd>\s*([^<]+?)\s*</dd>', html_text, re.S)
    fields = {k.strip(): v.strip() for k, v in items}

    return {
        'position': fields.get('Position', ''),
        'weight': fields.get('Weight', ''),
        'height': fields.get('Height', ''),
        'hometown': fields.get('Hometown', ''),
        'class': fields.get('Class', ''),
        'highschool': fields.get('High School', ''),
        'number': number,
        'first_name': first,
        'last_name': last,
    }

def main():
    roster_html = IN.read_text(encoding='utf-8')
    profiles = extract_profiles(roster_html)
    if not profiles:
        print('No player profiles found in roster HTML')
        return

    name_map = extract_names_from_roster_html(roster_html)

    players = []
    for i, (rid, url) in enumerate(profiles):
        try:
            print(f'Fetching {url} ({i+1}/{len(profiles)})')
            page = fetch(url)
            p = parse_player_page(page)
            # if roster page JSON had name, use it
            if rid in name_map:
                fn, ln = name_map[rid]
                if fn:
                    p['first_name'] = fn
                if ln:
                    p['last_name'] = ln
            players.append(p)
        except Exception as e:
            print('Error fetching', url, e)

    fieldnames = ['position','weight','height','hometown','class','highschool','number','first_name','last_name']
    with OUT.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in players:
            writer.writerow(p)

    print(f'Wrote {len(players)} players to {OUT}')

if __name__ == '__main__':
    main()
