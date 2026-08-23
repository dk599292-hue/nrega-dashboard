import requests
from bs4 import BeautifulSoup
import json
import re

TA_MAPPING = {
    "AKALTARI": "SURYKANT TIGER", "AMALDHIHA": "SAPNA BANJARE", "AMERIAKBARI": "SAPNA BANJARE",
    "AMERIKAPA": "SAPNA BANJARE", "ATTRA": "ROHIT SAHU", "BAIMA": "KAMINI VERMA",
    "BAMHU": "PURWA GUPTA", "BANAKDIH": "PRIYA YADAV", "BANKA": "SURYKANT TIGER",
    "BARTOURI": "JAWAHAR KHANDE", "BASHA": "SURYKANT TIGER", "BASIYA": "RAJENDRA KOSHLE",
    "BELTARA": "SURYKANT TIGER", "BELTUKRI": "SAPNA BANJARE", "BHADI": "PURWA GUPTA",
    "BHAISBOD": "PRIYA YADAV", "BHARARI": "VIKAS RATHOR", "BHARVIDIH": "LALIT KUMAR SURYAVANSHI",
    "BHATGAON": "JAWAHAR KHANDE", "BHILMI": "VIKAS RATHOR", "BHOJPURI": "ROHIT SAHU",
    "BITKULIN": "PURWA GUPTA", "BITKULID": "JAWAHAR KHANDE", "BODSARA": "SAPNA BANJARE",
    "BUNDELA": "JAWAHAR KHANDE", "CHAKARBHANTA": "PRIYA YADAV", "CHORHADEWARI": "PURWA GUPTA",
    "DAGANIYA": "PURWA GUPTA", "DAGORI": "VIKAS RATHOR", "DEWKIRARI": "JAWAHAR KHANDE",
    "DHAMNI": "RAJENDRA KOSHLE", "DHAURABHANTA": "ROHIT SAHU", "DHEKA": "KAMINI VERMA",
    "DHOOMA": "KAMINI VERMA", "DHOURAMUDA": "SURYKANT TIGER", "DURGADIH": "SAPNA BANJARE",
    "GADVAT": "PINKY RATHOR", "GATOURI": "PINKY RATHOR", "GHOGHARA": "SAPNA BANJARE",
    "GIDHOURI": "SURYKANT TIGER", "GODHI": "ROHIT SAHU", "GONDAIYA": "PINKY RATHOR",
    "GUMA": "JAWAHAR KHANDE", "HARDHI": "ROHIT SAHU", "HARDIKALA": "RAJENDRA KOSHLE",
    "HATHNI": "JAWAHAR KHANDE", "HIRRI": "ROHIT SAHU", "JALSO": "PINKY RATHOR",
    "JHAL": "JAWAHAR KHANDE", "JHALPHA": "ROHIT SAHU", "KACHAR": "LALIT KUMAR SURYAVANSHI",
    "KADAR": "RAJENDRA KOSHLE", "KADARI": "SURYKANT TIGER", "KARHI": "SAPNA BANJARE",
    "KARMA": "PURWA GUPTA", "KAWANCHI": "RAJENDRA KOSHLE", "KAYA": "RAJENDRA KOSHLE",
    "KHAIRAD": "PURWA GUPTA", "KHAIRAL": "KAMINI VERMA", "KHAIRKHUNDI": "LALIT KUMAR SURYAVANSHI",
    "KHAMHARDIH": "RAJENDRA KOSHLE", "KOHROUNDA": "SAPNA BANJARE", "KORBI": "SURYKANT TIGER",
    "KORMI": "RAJENDRA KOSHLE", "KUNWA": "RAJENDRA KOSHLE", "LAGRA": "KAMINI VERMA",
    "LAKHRAM": "PINKY RATHOR", "LIMHA": "SURYKANT TIGER", "LIMTARI": "PRIYA YADAV",
    "LOPHANDI": "LALIT KUMAR SURYAVANSHI", "MADANPUR": "LALIT KUMAR SURYAVANSHI",
    "MAGRUCHLA": "PRIYA YADAV", "MAHMAND": "PRIYA YADAV", "MANGALAP": "SAPNA BANJARE",
    "MANIKPUR": "KAMINI VERMA", "MANJOORPAHARI": "VIKAS RATHOR", "MATIYARI": "PURWA GUPTA",
    "MOHBATTHA": "ROHIT SAHU", "MOHDA": "ROHIT SAHU", "MOHRA": "PURWA GUPTA",
    "MOHTARA": "SAPNA BANJARE", "MOHTARAI": "PINKY RATHOR", "MUDHIPAR": "ROHIT SAHU",
    "MURKUTA": "SAPNA BANJARE", "NAGOI": "KAMINI VERMA", "NAGPURA": "PRIYA YADAV",
    "NAGRODHI": "RAJENDRA KOSHLE", "NAVGWA": "PINKY RATHOR", "NEPANIYA": "ROHIT SAHU",
    "NEVSA": "VIKAS RATHOR", "PARSADABH": "JAWAHAR KHANDE", "PARSADASE": "PINKY RATHOR",
    "PARSAHI": "KAMINI VERMA", "PASID": "SAPNA BANJARE", "PATTHARKHAN": "PRIYA YADAV",
    "PENDRAWA": "PINKY RATHOR", "PENDRAWAD": "ROHIT SAHU", "PENDRIDIH": "ROHIT SAHU",
    "PHARHADA": "KAMINI VERMA", "PIRAIYA": "SAPNA BANJARE", "PODIH": "RAJENDRA KOSHLE",
    "PONDIS": "KAMINI VERMA", "POUNSARA": "LALIT KUMAR SURYAVANSHI", "POUNSARI": "SAPNA BANJARE",
    "RAHNGI": "ROHIT SAHU", "RAMPUR": "VIKAS RATHOR", "RAMTALA": "PINKY RATHOR",
    "SALKHA": "SURYKANT TIGER", "SAMBALPURI": "ROHIT SAHU", "SARDHA": "RAJENDRA KOSHLE",
    "SARWANDEVRI": "LALIT KUMAR SURYAVANSHI", "SARWANI": "PRIYA YADAV", "SELAR": "PURWA GUPTA",
    "SEMARTALA": "LALIT KUMAR SURYAVANSHI", "SEMRA": "LALIT KUMAR SURYAVANSHI",
    "SENDRI": "PINKY RATHOR", "SENWAR": "PRIYA YADAV", "SEWTI": "JAWAHAR KHANDE",
    "SILPAHRI": "KAMINI VERMA", "SINGHARI": "LALIT KUMAR SURYAVANSHI", "TEKAR": "SURYKANT TIGER",
    "TELSARA": "PRIYA YADAV", "UCHCHABHATTI": "PURWA GUPTA", "UDANTAL": "VIKAS RATHOR",
    "UDGAN": "JAWAHAR KHANDE", "UMARIYA": "JAWAHAR KHANDE", "URTUM": "SURYKANT TIGER"
}

def clean_name(name):
    return re.sub(r'[^A-Z]', '', name.upper())

URL = "https://vbgramgrep.dord.gov.in/VBGRAMG/dpc_sms_new.aspx?payload=bQyXd5YvpCRvEbmbPOYSEwETM7TTGZlQBI5C1Kz91hbfTupyDSrtq9n09VegDZziyytgG-GFw_vnrMspnzdDv7oEkEvWnm9jZme8j2p1c_DLhozD3mP_4r9euLZn8MVR7U9lGsA1G_8f9o8s3l7dZ2GjJ2CX5oYj--3eS6WxI7KvrPJ9FoqBzW3hfIhCfWPGEPLzRs8DmkJ3pTs8ZUawzAwGxVf40z5sGeHV0lnx0a5ynnvq2NSQm5P7SHJFeXTNQcjG3mOlmXVJh43bvIXIgcGG_UWjMsxR6HqoaypgO3SLjP6EUV1-CQ2gTG4zm6A5a2EVyBw9z5qGeLoBV6K5Ew"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

try:
    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')

    data = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all(['td', 'th'])
            texts = [c.text.strip() for c in cols]
            
            if len(texts) >= 5 and texts[0].isdigit():
                gp = texts[1]
                if gp.lower() in ['total', 'grand total', 'sum'] or len(gp) < 2:
                    continue

                numbers = [re.sub(r'\D', '', t) for t in texts[2:] if re.sub(r'\D', '', t) != '']
                
                labour_val = int(numbers[-2]) if len(numbers) >= 2 else (int(numbers[0]) if len(numbers) == 1 else 0)
                mrs_val = int(numbers[-1]) if len(numbers) >= 1 else 0

                gp_cleaned = clean_name(gp)
                ta_name = "-"
                
                if gp_cleaned in TA_MAPPING:
                    ta_name = TA_MAPPING[gp_cleaned]
                else:
                    for key, val in TA_MAPPING.items():
                        if key in gp_cleaned or gp_cleaned in key:
                            ta_name = val
                            break

                data.append({
                    "gp": gp,
                    "ta": ta_name,
                    "labour": labour_val,
                    "mrs": mrs_val
                })

    with open('live_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Success: Processed {len(data)} Gram Panchayats.")

except Exception as e:
    print(f"Error fetching data: {e}")
