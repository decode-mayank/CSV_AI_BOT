import os
import openai
from dotenv import load_dotenv
import csv
import pandas as pd

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_type():
    df = pd.read_csv("products.csv")
    for index, row in df.iterrows():
        # breakpoint()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""You need to get the category of the product, whether it is a Product/Accessory. I will pass a product name with description and breadcrumb of product, for each product get the category of the product. Understand the input and get the category accordingly.
                    Input: ResMed AirFit™ N20 for Her Mask Headgear, Replacement headgear for her Miraage FX
                    Mirage FX for Her features a form-fitting SoftEgde headgear which is flexible and light, with a contoured edge that's kind to your face. It comes in a stylish pink colour, smaller in size, to best fit your face, Home > Sleep Apnea > CPAP Accessories > CPAP Mask Headgear > ResMed Mirage FX For Her Headgear
                    Bot: Accessory
                    Input: OptiPillows Starter Kit, Optipillows is used to treat Snoring and mild to moderate Obstructive Sleep Apnea. The only EPAP device that has adjustable pressures. Includes 3 cushion sizes, headgear and adjustable EPAP valve. For use at home or travelling
                    OptiPillows is an EPAP (Expiratory Positive Airway Pressure) nasal mask for the treatment of Snoring but may also treat mild to moderate obstructive Sleep Apnea.How it works:During inspiration the valve opens allowing you to breathe in easily. When you exhale, the valve closes and redirects the expired air through a narrow opening on the side of the valve. This creates Expiratory Positive Airway Pressure (EPAP) in the mouth which helps keep the upper airways open and prevents Snoring and Sleep Apnea. For better experience, expiratory pressure can be adjusted by rotating the sleeve to change expiratory resistance, Home > Sleep Apnea > CPAP Alternatives > OptiPillows Starter Kit
                    Bot: Product
                    Input: {row['product']}, {row['description']}, {row['breadcrumb']}""",
            temperature=0,
            max_tokens=50
        )
        response_list = response.choices[0].text.split("Bot:", 1)[1].strip()
        response_text = ''.join(response_list)
        df.at[index, 'type'] = response_text
        df.to_csv('products.csv', index=False)


def generate_tags():
    df = pd.read_csv("products.csv")
    for index, row in df.iterrows():
        # breakpoint()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"""Act as Tag extracter, I will pass a product with description, category and its breadcrumb. Read and get me the list of all tags as per the details shared. For each product atleast generate some 5 tags which could also act as entity. Don't add Home as a tag
                    Input: ResMed AirFit™ N20 for Her Mask Headgear, Replacement headgear for her Miraage FX
                    Mirage FX for Her features a form-fitting SoftEgde headgear which is flexible and light, with a contoured edge that's kind to your face. It comes in a stylish pink colour, smaller in size, to best fit your face, Sleep Apnea, Home > Sleep Apnea > CPAP Accessories > CPAP Mask Headgear > ResMed Mirage FX For Her Headgear
                    Bot: Headgear|Sleep Apnea|CPAPMask
                    Input: OptiPillows Starter Kit, Optipillows is used to treat Snoring and mild to moderate Obstructive Sleep Apnea. The only EPAP device that has adjustable pressures. Includes 3 cushion sizes, headgear and adjustable EPAP valve. For use at home or travelling
                    OptiPillows is an EPAP (Expiratory Positive Airway Pressure) nasal mask for the treatment of Snoring but may also treat mild to moderate obstructive Sleep Apnea.How it works:During inspiration the valve opens allowing you to breathe in easily. When you exhale, the valve closes and redirects the expired air through a narrow opening on the side of the valve. This creates Expiratory Positive Airway Pressure (EPAP) in the mouth which helps keep the upper airways open and prevents Snoring and Sleep Apnea. For better experience, expiratory pressure can be adjusted by rotating the sleeve to change expiratory resistance, Snoring, Home > Sleep Apnea > CPAP Alternatives > OptiPillows Starter Kit
                    Bot: Starter Kit|EPAP|Snoring|OptPillows

                    Input: {row['product']}, {row['description']}, {row['category']}, {row['breadcrumb']}""",
            temperature=0,
            max_tokens=100
        )
        response_list = response.choices[0].text.split("Bot:", 1)[1].strip()
        response_text = ''.join(response_list)
        df.at[index, 'tags'] = response_text
        df.to_csv('products.csv', index=False)


if __name__ == '__main__':
    generate_type()
    generate_tags()