"""
Generate synthetic training data for Ozempic complaint classification.
Mix of Adverse Events and Product Complaints.
"""

def generate_training_data():
    """Generate labeled training examples for Ozempic complaints."""

    training_data = [
        # Adverse Events (10 examples)
        {
            "complaint": "Patient started Ozempic 0.5mg weekly and after 3 weeks developed severe nausea and vomiting. Unable to keep food down. Doctor advised to stop medication.",
            "label": "Adverse Event",
            "reasoning": "Reports patient experiencing adverse drug reactions (nausea, vomiting) following Ozempic administration."
        },
        {
            "complaint": "I've been using Ozempic for 2 months and noticed a lump in my neck. My doctor found a thyroid nodule and is concerned about thyroid cancer.",
            "label": "Adverse Event",
            "reasoning": "Describes potential serious adverse reaction (thyroid nodule) possibly related to semaglutide use, requires medical evaluation."
        },
        {
            "complaint": "After my 4th Ozempic injection, I had severe abdominal pain and was hospitalized with pancreatitis. Blood amylase was elevated.",
            "label": "Adverse Event",
            "reasoning": "Reports serious adverse event (pancreatitis) with hospitalization following Ozempic use, confirmed by lab findings."
        },
        {
            "complaint": "Patient experienced extreme fatigue, dizziness and blood sugar dropped to 45 mg/dL while on Ozempic 1mg. ER visit required.",
            "label": "Adverse Event",
            "reasoning": "Describes hypoglycemic event requiring emergency care, a known adverse reaction to GLP-1 agonists."
        },
        {
            "complaint": "Started Ozempic 3 weeks ago. Developed severe injection site reaction with redness, swelling, and pain that lasted 5 days. Skin became infected.",
            "label": "Adverse Event",
            "reasoning": "Reports adverse reaction at injection site with infection, a medical complication from drug administration."
        },
        {
            "complaint": "I've had persistent diarrhea and stomach cramps for 6 weeks since starting Ozempic. Lost 15 pounds due to inability to eat.",
            "label": "Adverse Event",
            "reasoning": "Describes ongoing gastrointestinal adverse effects impacting patient's nutritional status and quality of life."
        },
        {
            "complaint": "Patient on Ozempic developed acute kidney injury. Creatinine increased from 1.0 to 3.2. Likely related to dehydration from GI side effects.",
            "label": "Adverse Event",
            "reasoning": "Reports serious adverse event (acute kidney injury) potentially related to Ozempic-induced dehydration."
        },
        {
            "complaint": "After injecting Ozempic, I had an allergic reaction with hives, facial swelling, and difficulty breathing. Used EpiPen and went to ER.",
            "label": "Adverse Event",
            "reasoning": "Describes serious allergic reaction (anaphylaxis) requiring emergency treatment following drug administration."
        },
        {
            "complaint": "My vision became blurry after starting Ozempic 2mg. Eye doctor said I have diabetic retinopathy that worsened rapidly.",
            "label": "Adverse Event",
            "reasoning": "Reports worsening of diabetic retinopathy possibly related to rapid glucose control from Ozempic, a known risk."
        },
        {
            "complaint": "I experienced severe depression and suicidal thoughts after 2 months on Ozempic. Had to be hospitalized in psychiatric unit.",
            "label": "Adverse Event",
            "reasoning": "Reports serious psychiatric adverse events requiring hospitalization, potentially related to medication use."
        },

        # Product Complaints (10 examples)
        {
            "complaint": "My Ozempic pen won't inject. The dose dial turns but when I press the button nothing comes out. The pen seems defective.",
            "label": "Product Complaint",
            "reasoning": "Describes mechanical malfunction of the pen device, not a patient safety issue but a product quality defect."
        },
        {
            "complaint": "The dose counter on my Ozempic pen is stuck between 0.5 and 1.0. I can't tell what dose I'm getting. Pen mechanism appears broken.",
            "label": "Product Complaint",
            "reasoning": "Reports product defect with dose counter mechanism affecting accurate dosing but no adverse patient reaction mentioned."
        },
        {
            "complaint": "Received Ozempic pen and the cap was already broken. Packaging was damaged during shipping. Concerned about sterility.",
            "label": "Product Complaint",
            "reasoning": "Describes packaging and shipping damage raising sterility concerns, a product quality issue without patient harm reported."
        },
        {
            "complaint": "The needle that came with my Ozempic pen won't attach properly. Tried multiple needles from the box, none fit correctly.",
            "label": "Product Complaint",
            "reasoning": "Reports manufacturing defect with needle compatibility, a product quality issue not involving patient adverse effects."
        },
        {
            "complaint": "My Ozempic pen leaked medication all over after I inserted the needle. Lost half the dose. This is the second pen with this problem.",
            "label": "Product Complaint",
            "reasoning": "Describes repeated product defect causing medication waste, a quality issue without reported patient harm."
        },
        {
            "complaint": "The instructions in my Ozempic box are in the wrong language. I received Spanish instructions but don't speak Spanish. Can't understand how to use it.",
            "label": "Product Complaint",
            "reasoning": "Reports labeling error with incorrect language instructions, a regulatory compliance issue without adverse patient event."
        },
        {
            "complaint": "Ozempic pen arrived at my pharmacy but it wasn't refrigerated. Box was warm to touch. Pharmacist said it may be ineffective now.",
            "label": "Product Complaint",
            "reasoning": "Describes cold chain failure affecting product quality and potency, not a direct adverse reaction to the medication."
        },
        {
            "complaint": "The expiration date on my Ozempic pen is smudged and unreadable. Can't tell if it's still good to use or expired.",
            "label": "Product Complaint",
            "reasoning": "Reports labeling defect with illegible expiration date, a quality control issue affecting product usability."
        },
        {
            "complaint": "My Ozempic pen has visible particles floating in the solution. Looks contaminated. Haven't used it yet but concerned about safety.",
            "label": "Product Complaint",
            "reasoning": "Describes visible contamination or particulate matter indicating potential manufacturing defect, reported before use."
        },
        {
            "complaint": "The dose selector on my Ozempic pen is extremely stiff and hard to turn. Takes significant force to dial up the dose. Different from my previous pens.",
            "label": "Product Complaint",
            "reasoning": "Reports mechanical defect with pen operation affecting ease of use, a product quality issue without patient harm."
        },
    ]

    return training_data


def generate_test_data():
    """Generate test examples for evaluation."""

    test_data = [
        # Adverse Events (10 examples)
        {
            "complaint": "I've been on Ozempic for 6 months and developed gallstones. Had severe right upper quadrant pain and needed surgery to remove gallbladder.",
            "label": "Adverse Event",
            "reasoning": "Reports serious adverse event (cholelithiasis) requiring surgical intervention, a known risk with GLP-1 agonists."
        },
        {
            "complaint": "Patient reported persistent nausea, vomiting and developed aspiration pneumonia after vomiting. Was hospitalized for 5 days.",
            "label": "Adverse Event",
            "reasoning": "Describes serious complication (aspiration pneumonia) resulting from GI adverse effects of Ozempic."
        },
        {
            "complaint": "Heart palpitations started after beginning Ozempic. Heart rate goes up to 120 bpm at rest. Cardiologist found new onset atrial fibrillation.",
            "label": "Adverse Event",
            "reasoning": "Reports cardiac adverse event (new atrial fibrillation) temporally related to Ozempic initiation."
        },
        {
            "complaint": "I had a severe injection site abscess that required incision and drainage. Culture grew staph aureus. Only happened with Ozempic injections.",
            "label": "Adverse Event",
            "reasoning": "Describes serious infection at injection site requiring surgical intervention, an adverse event from drug administration."
        },
        {
            "complaint": "My hair has been falling out excessively since starting Ozempic. Losing handfuls in the shower. Doctor says it's telogen effluvium from the medication.",
            "label": "Adverse Event",
            "reasoning": "Reports adverse effect (alopecia) attributed by physician to Ozempic use, affecting patient quality of life."
        },
        {
            "complaint": "Experienced severe constipation for weeks followed by bowel obstruction. Had to go to ER and was admitted for 3 days while on Ozempic.",
            "label": "Adverse Event",
            "reasoning": "Reports serious GI complication (bowel obstruction) requiring hospitalization, potentially related to Ozempic."
        },
        {
            "complaint": "Patient developed rash all over body, fever of 102F, and elevated liver enzymes after 2nd Ozempic dose. Possible drug hypersensitivity.",
            "label": "Adverse Event",
            "reasoning": "Describes systemic hypersensitivity reaction with organ involvement, a serious adverse drug reaction."
        },
        {
            "complaint": "I feel extremely anxious and jittery since starting Ozempic 1mg. Heart races and can't sleep. Never had anxiety before this medication.",
            "label": "Adverse Event",
            "reasoning": "Reports new onset psychiatric and autonomic symptoms temporally related to starting Ozempic."
        },
        {
            "complaint": "Developed severe muscle pain and weakness. CK level was 8000. Diagnosed with rhabdomyolysis while taking Ozempic and statin.",
            "label": "Adverse Event",
            "reasoning": "Reports serious adverse event (rhabdomyolysis) with lab confirmation, potentially related to drug interaction."
        },
        {
            "complaint": "I had persistent vomiting for 2 weeks on Ozempic and became severely dehydrated. Blood pressure dropped and I passed out. Called 911.",
            "label": "Adverse Event",
            "reasoning": "Describes serious complications (dehydration, hypotension, syncope) from medication adverse effects requiring emergency care."
        },

        # Product Complaints (10 examples)
        {
            "complaint": "My Ozempic pen clicks when I dial the dose but no medication comes out. Tried 3 times with same result. Pen is defective.",
            "label": "Product Complaint",
            "reasoning": "Reports mechanical malfunction preventing medication delivery, a device defect without reported patient harm."
        },
        {
            "complaint": "The label on my Ozempic pen is peeling off and I can't read the lot number or expiration date anymore. Quality control issue.",
            "label": "Product Complaint",
            "reasoning": "Describes labeling defect affecting product identification and traceability, a quality issue."
        },
        {
            "complaint": "Ozempic pen arrived frozen solid despite being shipped with ice packs. Completely frozen, not just cold. Likely ruined.",
            "label": "Product Complaint",
            "reasoning": "Reports cold chain failure with product freezing, affecting medication potency and quality."
        },
        {
            "complaint": "The protective seal on my Ozempic pen was already broken when I opened the box. Package appeared to be previously opened. Contamination risk.",
            "label": "Product Complaint",
            "reasoning": "Describes compromised packaging integrity raising sterility concerns, a product tampering or quality issue."
        },
        {
            "complaint": "Received wrong dose strength. Box says 0.5mg but pen is labeled 1.0mg. Pharmacy dispensing error or manufacturing labeling problem.",
            "label": "Product Complaint",
            "reasoning": "Reports labeling mismatch or dispensing error, a product identification issue without patient use or harm."
        },
        {
            "complaint": "My Ozempic pen's injection button is stuck and won't depress no matter how hard I push. Completely unable to inject dose. Mechanical failure.",
            "label": "Product Complaint",
            "reasoning": "Describes device mechanical failure preventing use, a product defect without adverse patient reaction."
        },
        {
            "complaint": "The Ozempic solution in my pen looks cloudy instead of clear. Haven't used it. Different appearance from my usual pens. Quality concern.",
            "label": "Product Complaint",
            "reasoning": "Reports abnormal product appearance suggesting contamination or degradation, identified before use."
        },
        {
            "complaint": "Pen injector makes a grinding noise when I dial the dose. Sounds broken. Worried it won't deliver the right amount. Just opened brand new pen.",
            "label": "Product Complaint",
            "reasoning": "Describes abnormal device operation suggesting mechanical defect, a quality issue affecting confidence in dosing."
        },
        {
            "complaint": "My Ozempic box contains the wrong needle size. All needles are 8mm but I was prescribed 4mm needles. Can't use these safely.",
            "label": "Product Complaint",
            "reasoning": "Reports incorrect component packaging, a dispensing or product configuration error without patient harm."
        },
        {
            "complaint": "The user manual in my Ozempic kit is for a different Novo Nordisk product (Victoza). Wrong instructions entirely. Major packaging error.",
            "label": "Product Complaint",
            "reasoning": "Describes serious labeling/packaging error with incorrect product instructions, a regulatory compliance issue."
        },
    ]

    return test_data
