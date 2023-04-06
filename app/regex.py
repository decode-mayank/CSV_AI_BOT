import pandas as pd 
import re

df = pd.read_csv("app_products.csv")

keyword_patterns = [r'\bSleep Apnea\b', r'\bInsomnia\b', r'\bCPAP\b',r'\bSD card\b',
                    r'\bsnoring\b',r'\bMask frame\b',r'\bMask\b',r'\bbattery\b',
                    r'\bheadgear\b',r'\bBestsellers\b',r'\bResmed Airfit\b',r'\bconverter\b',
                    r'\bDreampad\b',r'\bRe-timer\b',r'\bAirfit\b',r'\bAirtouch\b',r'\bAirmini\b'
                    r'\bAirflow\b',r'\bpillow\b',r'\bcushion\b',r'\bports cap\b',r'\bconnector\b',
                    r'\bH5i water tub\b',r'\bMask elbow\b',r'\bNasal Mask\b',r'\bBag\b',
                    r'\bResmed HumidX\b',r'\bREMZzz\b', r'\bMask Elbow\b',r'\bAdapter\b',
                    r'\bResmed Nasal pillow\b',r'\bAirsense\b',r'\bTube wrap\b',r'\bHumidX\b',
                    r'\bBongoRx\b',r'\bRPSII\b',r'\bResmed S9\b',r'\bReScan\b',r'\bResmed S8 CPAP\b',
                    r'\bResmed Gecko Nasal pad\b',r'\boptipillow\b',r'\bsmart care\b',r'\bResmed Mirage\b',
                    r'\bSeatec\b',r'\bREMZzz Nasal Padded\b',r'\bResmed Mirage\b',r'\bAirmini device\b',
                    r'\bSleeppositioner\b',r'\bRetimer\b',r'\bNight Light\b',r'\bResmed sleepy time tea\b', 
                    r'\bSmartNora\b',r'\bDodow\b',r'\bSwannies\b',r'\bframe\b',r'\bBluelight\b',
                    r'\bSnorex\b',r'\bRed Night Light\b',r'\bLenses\b',r'\bBlueLightBlock glasses\b',
                    r'\bRed NightLight\b',r'\bTea\b',r'\bCushion\b',r'\bFilters\b',r'\bSound Machine\b',
                    r'\bHeadgear\b',r'\bLight Therapy\b',r'\bSleep Health\b',r'\bsleep health\b',r'\bEye Mask\b',r'\bLed Bulbs\b',
                    r'\bBlocking lenses\b',r'\bonesleeptest\b'
                     ]

pattern = '|'.join(keyword_patterns)

df['tags'] = df['description'].str.findall(pattern, flags=re.IGNORECASE) + df['category'].str.findall(pattern, flags=re.IGNORECASE) + df['product'].str.findall(pattern, flags=re.IGNORECASE)
df['tags'] = df.apply(lambda x: x['breadcrumb'] + "|" + x['product'] + "|" + "|".join(list(set(x['tags']))),axis=1)
df = df.drop(df[df['price'] == 0].index)
df.to_csv("app_products.csv", index=False)
