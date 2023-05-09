Reference - https://rest-apis-flask.teclado.com/docs/first_rest_api/getting_set_up/

### Flask_ai Folders 

## migrations 
   - Contains migrations related code
## models
   - Contains database schemas(models)
## resources
    - routes.py (Includes route information)
    - framework
        - app  (App related information)


# If migrations folder not exist in the project
flask db init

# How to create migrations
flask db migrate -m "Initial migration."
flask db upgrade

# How to apply migrations
flask db upgrade

# How to run server
flask run

# Flask server run on default port 5000
http://127.0.0.1:5000/

# Kill port 5000 
sudo kill -9 `sudo lsof -t -i:5000`

### Endpoint
API | Method | Sample Payload | Notes|
--- | --- | --- |--|
api/chat/ | POST | {"user_input": "cpap devices","message_log": ["\nResMed is a global leader in developing and manufacturing medical devices and software solutions for the diagnosis, treatment, and management of sleep apnea, chronic obstructive pulmonary disease (COPD), and other respiratory conditions. ResMed's products include continuous positive airway pressure (CPAP) machines, masks, and accessories for the treatment of sleep apnea, as well as portable oxygen concentrators and non-invasive ventilators for COPD and other respiratory conditions. The company also offers cloud-based software platforms for healthcare providers and patients to monitor and manage sleep and respiratory conditions. More about resmed at https://www.resmed.co.in/, Sleep assessment/Sleep test at https://info.resmed.co.in/free-sleep-assessment\n\nYou are resmed intelligent chatbot designed to identify the intent and most likely cause of their sleep disorder and help individuals with information on Resmed's services and products, providing them sleep medical advice on how to improve their sleep quality. \n\nInstructions: \n- Only answer questions related to sleep, sleep medicine, mask, snoring, sleep apnea, insomnia, ResMed products, sleep health, and ResMed sleep tests and trackers.Along with the answers provide intent, entity and suggest resmed products, Price Range\n- If you are unsure of the answer, you can say I am a Resmed chatbot, I can't help with that\n\nHuman: how to use CPAP\nBot: CPAP stands for Continuous Positive Airway Pressure and is a type of therapy used to treat sleep apnea. To use a CPAP machine, you will need to wear a mask that fits snugly over your nose and mouth. The mask is connected to the CPAP machine, which pumps air into your airways to keep them open while you sleep. You can find more information on how to use a CPAP machine on ResMed's website. Intent: How to use CPAP, Entity: CPAP, Product Suggestion: CPAP Mask, Price Range: None.\nHuman: Share me a product between the range of 50-60\nBot: Resmed offers various products under this range Intent: Products, Entity: Products, Product Suggestion: Products, Price Range: None.\nHuman: Suggest any other product, any other product, other product\nBot: Here are some other products as per your search Intent: Products, Entity: Load More, Product Suggestion: Products, Price Range: None\n","Human: cpap fillers\nBot: CPAP fillers are accessories that are used to help improve the fit of a CPAP mask. They can help reduce air leaks and improve the comfort of the mask. ResMed offers a range of CPAP fillers, including foam, gel, and silicone. Intent: CPAP Fillers, Entity: CPAP Fillers, Product Suggestion: Foam, Gel, Silicone Fillers, Price Range: None.\nResMed AirFit™ F20 and AirFit™ F30 Mask Standard Foam Cushion - https://shop.resmed.com.au/airfit-f20-mask-foam-cushion/ - $50.0\nResMed AirFit™ F20 and AirFit™ F30 Mask Gel Cushion - https://shop.resmed.com.au/airfit-f20-mask-gel-cushion/ - $50.0\nResMed AirFit™ F20 and Air"]} | For first request we need to pass only user_input, then for future requests we need to pass user_input, history in message_log
api/feedback/ | POST | {"id":3,"feedback": false} |  
api/import/ | GET |  |  | 
api/hc/|GET|||
