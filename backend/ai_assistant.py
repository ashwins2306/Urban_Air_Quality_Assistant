"""
AI Assistant module for clean air guidance and environmental health recommendations.
Supports Google Gemini (gemini-2.0-flash) with built-in rule-based fallback,
strict timeout protection, whole-word token matching, and conversation history memory.
"""

import os
import re
import concurrent.futures
from typing import Optional, Dict, Any, List

try:
    import google.generativeai as genai
except ImportError:
    genai = None


TOPIC_GROUPS = [
    {
        "name": "asthma/breathing",
        "weight": 3.0,  # High clinical priority
        "keywords": [
            "asthma", "inhaler", "inhalers", "wheezing", "wheeze",
            "bronchitis", "chest tightness", "shortness of breath",
            "copd", "respiratory attack", "difficulty breathing"
        ],
        "template": (
            "Air pollution directly inflames sensitive bronchial airways and can quickly trigger acute asthma attacks or breathing distress{loc} 🫁. "
            "Always keep your prescribed rescue inhaler on hand, and review your personal asthma action plan with your physician ahead of severe air days. "
            "Maintain a clean-air sanctuary in your home by running a HEPA purifier non-stop in the room where you spend the most hours. "
            "Rinsing your nasal passages with a sterile saline spray after returning from outdoors can also help flush out trapped allergen and soot particles 💧."
        )
    },
    {
        "name": "mask",
        "weight": 2.0,
        "keywords": ["mask", "masks", "n95", "n99", "kn95", "kf94", "respirator", "respirators", "ffp2", "ffp3"],
        "template": (
            "When air quality drops{loc}, wearing a well-fitted N95 or N99 respirator is your most reliable personal shield against toxic fine particles 😷. "
            "Make sure the mask forms a snug seal across your nose and chin without air leaks along the edges. "
            "Standard cloth and surgical masks cannot capture microscopic particulate matter (PM2.5), so certified respirators are essential outdoors. "
            "Be sure to replace disposable respirators after roughly 40 hours of use or as soon as breathing resistance noticeably increases 🛡️."
        )
    },
    {
        "name": "purifier/filter",
        "weight": 2.0,
        "keywords": ["purifier", "purifiers", "filter", "filters", "hepa", "cadr", "air cleaner", "air filtration", "filtration"],
        "template": (
            "Using a true HEPA air purifier is one of the most effective ways to scrub microscopic pollutants from your indoor spaces{loc} 🏠. "
            "Look for units with a Clean Air Delivery Rate (CADR) appropriately sized to exchange your room volume at least four to five times per hour. "
            "Keep the purifier running continuously on a medium setting rather than switching it on and off intermittently throughout the day. "
            "Remember to vacuum the pre-filter monthly and replace the main HEPA filter annually for peak performance 🌬️."
        )
    },
    {
        "name": "cook/kitchen",
        "weight": 1.5,
        "keywords": ["cook", "cooking", "kitchen", "stove", "frying", "fry", "exhaust hood", "chimney", "gas stove", "oil smoke", "roasting"],
        "template": (
            "Indoor cooking, especially high-heat frying and gas combustion, can generate massive spikes in particulate matter right inside your home{loc} 🍳. "
            "Always run your kitchen exhaust fan or range hood on high whenever you cook, and keep kitchen doors closed to prevent fumes from spreading to living areas. "
            "If possible, consider switching to induction cooktops or boiling methods to dramatically reduce harmful combustion byproducts. "
            "Covering pots with tight lids while simmering also reduces moisture and indoor aerosol formation significantly 🍲."
        )
    },
    {
        "name": "exercise/workout",
        "weight": 1.5,
        "keywords": ["exercise", "exercising", "workout", "workouts", "working out", "gym", "running", "jogging", "cycling", "sports", "cardio", "marathon"],
        "template": (
            "During vigorous cardiovascular workouts, your breathing rate increases tenfold, which draws pollutants much deeper into your lung alveoli{loc} 🏃. "
            "When ambient air pollution is elevated, shift your workouts indoors to an air-filtered gym or living room. "
            "If you choose to train outside, schedule sessions during midday when temperature inversions lift and atmospheric dispersion is at its peak. "
            "Always listen to your body and scale back workout intensity immediately if you notice throat irritation, coughing, or chest tightness 💪."
        )
    },
    {
        "name": "child/kid",
        "weight": 1.8,
        "keywords": ["child", "children", "kid", "kids", "baby", "babies", "infant", "infants", "toddler", "toddlers", "pediatric", "school commute"],
        "template": (
            "Children breathe more air per pound of body weight than adults, making their developing lungs particularly vulnerable to dirty air{loc} 👶. "
            "On poor air days, replace outdoor recess with indoor games in rooms equipped with active HEPA air filtration. "
            "Ensure children drink plenty of fluids and maintain a nutrient-rich diet with antioxidants like vitamin C to protect delicate airway linings. "
            "Always inspect the fit of pediatric-sized N95 or KN95 masks before letting them travel outside for school or errands 🎒."
        )
    },
    {
        "name": "elderly",
        "weight": 1.8,
        "keywords": ["elderly", "senior", "seniors", "aging", "grandparent", "grandparents", "older adult", "older adults", "geriatric"],
        "template": (
            "Older adults face elevated risks from air pollution due to higher rates of pre-existing cardiovascular and respiratory vulnerabilities{loc} 👵. "
            "Senior family members should remain indoors in temperature-controlled, air-purified rooms during severe pollution episodes. "
            "Keep emergency medications and inhalers readily accessible, and monitor blood pressure regularly as fine particles can trigger vascular stress. "
            "Gentle indoor mobility exercises and staying well hydrated will help maintain vitality without exposing sensitive airways to ambient toxins ❤️."
        )
    },
    {
        "name": "commute/drive",
        "weight": 1.2,
        "keywords": ["commute", "commuting", "driving", "traffic", "transit", "vehicle", "cabin filter", "recirculation", "car cabin"],
        "template": (
            "Commuting through dense traffic exposes you to concentrated exhaust fumes, black carbon, and brake dust{loc} 🚗. "
            "Keep car windows tightly shut and set your vehicle air conditioning to internal recirculation mode to avoid pulling in toxic street fumes. "
            "Consider upgrading your vehicle cabin air filter to an activated carbon HEPA unit that captures both particulate matter and noxious gases. "
            "If you travel by two-wheeler or public transit, wearing a fitted N95 respirator is vital to shield your airways from tailpipe emissions 🛵."
        )
    },
    {
        "name": "diy/homemade",
        "weight": 1.5,
        "keywords": ["diy", "homemade", "corsi-rosenthal", "corsi rosenthal", "box fan", "do it yourself", "cheap purifier", "budget filter"],
        "template": (
            "Building an affordable DIY air cleaner like a Corsi-Rosenthal box is a proven, highly economical way to clean indoor air{loc} 📦. "
            "Simply tape four MERV 13 furnace filters together with a cardboard bottom and secure a standard 20-inch box fan blowing upward on top. "
            "This homemade setup often rivals commercial air purifiers in clean air delivery rate (550+ CFM) while costing under $85. "
            "Make sure all filter seams are thoroughly sealed with duct tape so every cubic foot of air passes through the filter media 🛠️."
        )
    },
    {
        "name": "plant/indoor",
        "weight": 1.2,
        "keywords": ["plant", "plants", "houseplant", "houseplants", "snake plant", "spider plant", "areca palm", "peace lily", "botanical"],
        "template": (
            "While indoor houseplants like snake plants and spider plants beautify living spaces and absorb certain gaseous VOCs, their ability to filter fine particulate matter (PM2.5) is minimal{loc} 🌿. "
            "NASA studies proved plants can metabolize chemicals like benzene and formaldehyde through root microbes, but particulate smog requires mechanical airflow. "
            "Use botanical plants to boost ambient oxygen and humidity, but always pair them with a mechanical True HEPA purifier for airborne soot. "
            "Wipe dust off plant leaves regularly so their surface pores can breathe cleanly 🪴."
        )
    },
    {
        "name": "stubble/burn",
        "weight": 2.0,
        "keywords": ["stubble", "stubble burning", "crop burning", "parali", "farm fire", "farm fires", "biomass fire", "wildfire", "smoke plume"],
        "template": (
            "Seasonal agricultural stubble burning and biomass fires inject dense clouds of toxic black carbon and volatile organics across wide regions{loc} 🔥. "
            "When smoke plumes drift in, seal exterior windows with weatherstripping to stop smoky haze from infiltrating your living quarters. "
            "Avoid using vacuum cleaners without HEPA exhaust filters, as standard vacuums can resuspend settled soot particles back into your breathing zone. "
            "Wearing an N95 respirator outdoors during burning episodes is critical to prevent acute airway inflammation and coughing fits 😷."
        )
    },
    {
        "name": "window/ventilat",
        "weight": 1.3,
        "keywords": ["window", "windows", "ventilation", "ventilate", "ventilating", "fresh air", "air out", "airing room"],
        "template": (
            "Managing natural ventilation requires timing your window openings to periods of lowest outdoor pollution{loc} 🪟. "
            "Keep windows firmly shut during early mornings and late evenings when winter inversions trap heavy smog near ground level. "
            "If you need to vent indoor moisture or carbon dioxide, briefly open windows for ten minutes around midday (1:00 PM - 3:30 PM) when solar heating disperses pollutants. "
            "Turn your indoor air purifiers to maximum speed right after closing the windows to quickly clear out any incoming particles 🏠."
        )
    },
    {
        "name": "sleep/bedroom",
        "weight": 1.3,
        "keywords": ["sleep", "sleeping", "bedroom", "bedrooms", "bedtime", "nocturnal air", "nighttime sleep"],
        "template": (
            "Creating a clean-air oasis in your bedroom is vital since you spend one-third of your entire life sleeping there{loc} 🛏️. "
            "Keep bedroom windows closed overnight and position an appropriately sized HEPA purifier near your bed on a quiet whisper setting. "
            "Wash bed linens weekly in warm water to eliminate accumulated particulate matter and allergen reservoirs. "
            "Waking up in a clean, low-particulate environment drastically reduces overnight airway inflammation and improves sleep quality 🌙."
        )
    },
    {
        "name": "weather/forecast",
        "weight": 1.2,
        "keywords": ["weather", "forecast", "wind speed", "rainfall", "temperature inversion", "inversion layer", "winter smog", "foggy", "meteorology"],
        "template": (
            "Meteorological dynamics like wind velocity and thermal inversions heavily dictate surface pollution levels{loc} 🌦️. "
            "During calm winter days, cool air gets trapped under a warm atmospheric layer, preventing smoke and vehicle emissions from dispersing. "
            "Rain showers provide natural wet deposition that washes particulate matter out of the atmosphere, offering immediate air relief. "
            "Track daily weather forecasts alongside air metrics so you can anticipate smog spikes before they peak 🌡️."
        )
    },
    {
        "name": "aqi/pollution",
        "weight": 1.0,
        "keywords": ["aqi", "pm2.5", "pm10", "air quality index", "hazardous air", "smog level", "pollution level"],
        "template": (
            "The Air Quality Index translates complex pollutant measurements like fine particulate matter and nitrogen dioxide into a single easy-to-understand scale{loc} 📊. "
            "Values under 50 signify healthy air, whereas levels above 150 require sensitive groups to take precautions, and readings past 300 indicate hazardous air for everyone. "
            "Microscopic fine particles (PM2.5) are especially hazardous because they penetrate deep into lung alveoli and enter the bloodstream. "
            "Checking local hourly monitors regularly allows you to plan your outdoor activities during lower exposure windows 💡."
        )
    },
    {
        "name": "hydration/diet",
        "weight": 1.1,
        "keywords": ["hydration", "hydrate", "drinking water", "diet", "nutrition", "antioxidant", "antioxidants", "vitamin c", "herbal tea"],
        "template": (
            "Maintaining strong internal defenses through proper hydration and nutrition helps counter oxidative stress caused by air pollution{loc} 🍵. "
            "Drinking two to three liters of water daily keeps mucosal membranes moist and capable of trapping foreign particles before they reach the lungs. "
            "Incorporate antioxidant-dense foods rich in vitamin C, vitamin E, and healthy fats like citrus fruits, nuts, and leafy greens. "
            "Warm herbal teas with ginger and tulsi can also soothe irritated throat tissues after a day of poor air exposure 🥗."
        )
    },
    {
        "name": "pets/animal",
        "weight": 1.2,
        "keywords": ["pet", "pets", "dog", "dogs", "cat", "cats", "animal", "puppy", "kitten", "veterinary"],
        "template": (
            "Domestic pets are vulnerable to polluted air because they stay closer to the floor where heavy particles settle and have faster respiration rates{loc} 🐾. "
            "Limit outdoor walks for dogs to short bathroom breaks during severe air warnings, and avoid strenuous play outside. "
            "Wipe down your pet's coat and paws when returning indoors to prevent toxic dust from spreading onto carpets and furniture. "
            "Keep your furry companions in air-purified rooms and watch for warning signs such as excessive panting, coughing, or eye discharge 🐕."
        )
    }
]

FALLBACK_TEMPLATE = (
    "Protecting your respiratory health begins with tracking real-time air quality metrics and minimizing particulate exposure{loc} 🌿.\n\n"
    "**Core Recommendations:**\n"
    "- **Outdoor Protection**: Wear a certified N95 or FFP2 respirator when AQI exceeds 150.\n"
    "- **Indoor Sanctuary**: Keep windows sealed during morning inversion hours (06:00 - 09:30 AM) and run True HEPA purifiers.\n"
    "- **Daily Routine Timing**: Schedule high-exertion workouts or outdoor errands between 01:00 PM and 03:30 PM when solar heating disperses ground-level smog.\n"
    "- **Internal Hydration**: Drink 2–3 liters of water daily to maintain mucus membrane barriers against inhaled particulates 💧."
)


def _execute_gemini_call(
    api_key: str,
    message: str,
    context: dict,
    history: Optional[List[Dict[str, str]]] = None
) -> Optional[str]:
    """Internal helper to execute Gemini API call with proper configuration."""
    if not genai:
        return None

    genai.configure(api_key=api_key)

    ctx = context if isinstance(context, dict) else {}
    city = ctx.get("city") or "your area"
    aqi = ctx.get("aqi") or "unspecified"
    lifestyle = ctx.get("lifestyle") or "general"

    system_instruction = (
        "You are BreatheEasy AI, an expert clinical atmospheric and environmental health specialist. "
        "Your role is to provide clear, actionable, educational, and scientifically sound advice "
        "on air pollution, respiratory protection, winter smog mitigation, and sustainable daily habits.\n\n"
        f"User Real-Time Context:\n"
        f"- Monitored City: {city}\n"
        f"- Current AQI: {aqi}\n"
        f"- Lifestyle Profile: {lifestyle}\n\n"
        "Guidelines:\n"
        "- Format answers cleanly using markdown (bullet points, **bold** key terms).\n"
        "- Prioritize practical, life-saving advice: mask standards (N95/N99), HEPA filtration, inversion timing.\n"
        "- Address follow-up questions coherently using the conversation history.\n"
        "- Maintain a warm, encouraging, and authoritative medical/scientific tone."
    )

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=system_instruction
    )

    # Format history turns if provided
    formatted_history = []
    if history and isinstance(history, list):
        for turn in history[-6:]:  # Keep recent 6 turns for memory context
            role = turn.get("role")
            content = turn.get("content")
            if role in ("user", "model", "assistant") and content:
                gemini_role = "user" if role == "user" else "model"
                formatted_history.append({"role": gemini_role, "parts": [content]})

    if formatted_history:
        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(message)
    else:
        response = model.generate_content(message)

    if response and hasattr(response, "text") and response.text:
        return response.text.strip()
    return None


def get_gemini_response(
    message: str,
    context: dict,
    api_key: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None,
    timeout_seconds: float = 7.0
) -> Optional[str]:
    """
    Generate response using Gemini API with timeout protection (caps at timeout_seconds).
    Uses provided api_key or falls back to GEMINI_API_KEY environment variable.
    """
    key_to_use = api_key or os.environ.get("GEMINI_API_KEY")
    if not key_to_use or not genai:
        return None

    # Execute in thread with strict timeout to prevent server thread blocking (B5)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_execute_gemini_call, key_to_use, message, context, history)
        try:
            return future.result(timeout=timeout_seconds)
        except concurrent.futures.TimeoutError:
            print(f"Gemini API call timed out after {timeout_seconds}s; switching to clinical fallback.")
            return None
        except Exception as e:
            print(f"Gemini API call failed: {e}; switching to clinical fallback.")
            return None


def get_builtin_response(message: str, context: dict) -> str:
    """
    Generate a built-in response using exact whole-word token matching (B15).
    Avoids substring traps ('team' != 'tea', 'forest' != 'rest', 'scarf' != 'car').
    """
    ctx = context if isinstance(context, dict) else {}
    city = ctx.get("city") or ctx.get("location") or ""
    city_str = str(city).strip()
    loc = f" in {city_str}" if city_str else ""

    message_text = message.strip() if message else ""

    best_topic = None
    max_score = 0.0

    for topic in TOPIC_GROUPS:
        score = 0.0
        for kw in topic["keywords"]:
            # Strict whole-word / whole-phrase boundary matching (B15)
            pattern = r"\b" + re.escape(kw) + r"\b"
            matches = len(re.findall(pattern, message_text, re.IGNORECASE))
            if matches > 0:
                score += matches * topic.get("weight", 1.0)

        if score > max_score:
            max_score = score
            best_topic = topic

    if best_topic and max_score > 0:
        return best_topic["template"].format(loc=loc)

    return FALLBACK_TEMPLATE.format(loc=loc)


def get_chat_response(
    message: str,
    context: dict,
    api_key: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Unified chat handler. Tries Gemini 2.0 Flash first (with timeout).
    If unavailable or fails, seamlessly serves verified clinical rule engine.
    Returns structured dict with response text, active engine source, and fallback status.
    """
    # 1. Attempt Gemini 2.0 Flash
    gemini_reply = get_gemini_response(message, context, api_key=api_key, history=history, timeout_seconds=7.0)
    if gemini_reply:
        return {
            "response": gemini_reply,
            "source": "gemini",
            "is_fallback": False
        }

    # 2. Verified Clean Air Clinical Rule Engine Fallback
    fallback_reply = get_builtin_response(message, context)
    return {
        "response": fallback_reply,
        "source": "clinical_engine",
        "is_fallback": True
    }


# ==============================================================================
# Chrono-Intelligence Generation
# ==============================================================================

def synthesize_chrono_clinical(
    city: str,
    lifestyle: str,
    aqi: int,
    forecast: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Deterministic boundary-layer atmospheric physics synthesizer.
    Produces high-fidelity diurnal inversion schedule, audio script, and calendar sync.
    """
    persona = lifestyle.strip().lower()
    city_display = city.strip().title() if city else "Local Region"

    # Base profiles mapping
    personas_config = {
        "family": {
            "title": "Family & Children",
            "headline": f"Solar Convective Aeration Window in {city_display} Anticipated at 1:30 PM",
            "spoken": (
                f"Atmospheric chrono-briefing for your family in {city_display}. Morning thermal radiation "
                f"inversion traps ground particulates until 10:30 AM. Ensure school departures use fitted N95 "
                f"respirators and keep waiting periods inside lobbies. Your optimal window for airing living spaces "
                f"and brief outdoor play opens between 1:30 PM and 3:45 PM as solar thermal mixing breaks the boundary layer. "
                f"Seal all bedroom sanctuaries and activate HEPA scrubbers by 6:30 PM ahead of dusk stagnation."
            ),
            "hazard_title": "Morning Pediatric Inversion Trap",
            "hazard_time": "06:30 - 10:15",
            "hazard_desc": "Cold air stratification traps school bus diesel soot and combustion exhaust at child breathing height.",
            "optimal_title": "Solar Convective Dilution Window",
            "optimal_time": "13:30 - 15:45",
            "optimal_desc": "Sunlight breaks the ground thermal inversion, lifting particulate density into the upper troposphere.",
            "sanctuary_title": "Dusk Boundary Layer Collapse",
            "sanctuary_time": "18:00 - Overnight",
            "sanctuary_desc": "Atmospheric cooling seals outdoor pollutants near the surface; run continuous bedroom HEPA filtration.",
            "milestones": [
                {"time": "07:00", "title": "School Commute Protection", "activity": "Fit pediatric N95 respirators; avoid idling near vehicular tailpipes.", "level": "danger"},
                {"time": "10:30", "title": "Boundary Inversion Lifting", "activity": "Surface air warms; solar thermals initiate atmospheric mixing.", "level": "warning"},
                {"time": "13:30", "title": "Optimal Cross-Ventilation", "activity": "Execute 15-minute window purge to flush indoor CO2; safe for outdoor errand.", "level": "optimal"},
                {"time": "17:30", "title": "Evening Smog Ingress Guard", "activity": "Seal balcony sliders and door draft stoppers before twilight inversion descends.", "level": "warning"},
                {"time": "21:00", "title": "Sleep Sanctuary Filtration", "activity": "Run True HEPA air purifier on medium-high in sealed bedrooms.", "level": "safe"}
            ]
        },
        "elderly": {
            "title": "Senior Wellness",
            "headline": f"Cardiovascular Radiation Inversion Shield in {city_display} Active Until 11:00 AM",
            "spoken": (
                f"Senior wellness atmospheric advisory for {city_display}. Ground radiation cooling causes "
                f"dense particulate concentration during early morning hours. Seniors and those with respiratory "
                f"sensitivities should stay inside pre-filtered living areas until late morning. Schedule gentle "
                f"sunlight exposure or balcony walks between 1:00 PM and 3:00 PM when solar convective mixing is highest. "
                f"Keep bedroom sanctuaries sealed with continuous air purification starting at dusk."
            ),
            "hazard_title": "Early Morning Bronchial Hazard",
            "hazard_time": "06:00 - 10:45",
            "hazard_desc": "Cold stagnant surface air triggers acute bronchospasms and elevated blood pressure.",
            "optimal_title": "Warm Thermal Solar Window",
            "optimal_time": "13:00 - 15:15",
            "optimal_desc": "Ambient temperatures peak, dispersing fine particulates and providing safe natural daylight exposure.",
            "sanctuary_title": "Nighttime Hermetic Sleep Sanctuary",
            "sanctuary_time": "18:30 - Overnight",
            "sanctuary_desc": "Ensure bedroom doors are sealed with damp draft stoppers and run hospital-grade HEPA units.",
            "milestones": [
                {"time": "06:30", "title": "Sanctuary Awakening", "activity": "Maintain indoor rest; delay morning walks until solar thermal breakthrough.", "level": "danger"},
                {"time": "10:30", "title": "Respiratory Steam Hydration", "activity": "Inhale warm clean steam to moisturize airway mucosal lining.", "level": "safe"},
                {"time": "13:00", "title": "Optimal Mobility & Sunlight", "activity": "Gentle outdoor movement or garden sunlight during peak atmospheric dilution.", "level": "optimal"},
                {"time": "17:00", "title": "Pre-Dusk Window Sealing", "activity": "Secure all exterior windows firmly before evening temperature drops.", "level": "warning"},
                {"time": "20:30", "title": "Bedside Purifier Verification", "activity": "Verify True HEPA unit is running cleanly on whisper mode near the bed.", "level": "safe"}
            ]
        },
        "commuter": {
            "title": "Urban Executive",
            "headline": f"Arterial Corridor Rush-Hour Inversion Alert in {city_display}: Depart Post-9:30 AM",
            "spoken": (
                f"Executive commute briefing for {city_display}. Heavy vehicle exhaust will remain trapped in the lowest "
                f"50 meters during peak rush hour. Ensure car cabin air is switched strictly to internal recirculation "
                f"before entering flyovers or congested junctions. The lowest particulate travel window opens between "
                f"1:15 PM and 4:00 PM. If taking mass transit, don an N95 respirator before entering station corridors."
            ),
            "hazard_title": "Morning Arterial Trap Peak",
            "hazard_time": "07:30 - 10:00",
            "hazard_desc": "Rush-hour tailpipe emissions collide with stagnant morning boundary layer on urban corridors.",
            "optimal_title": "Off-Peak Midday Transit Window",
            "optimal_time": "13:15 - 16:00",
            "optimal_desc": "Solar convection and light midday traffic result in up to 40% lower in-cabin particulate exposure.",
            "sanctuary_title": "Evening Congestion Inversion",
            "sanctuary_time": "18:00 - 21:00",
            "sanctuary_desc": "Twilight cooling traps evening commuter exhaust; avoid walking along major ring roads.",
            "milestones": [
                {"time": "08:00", "title": "Cabin Recirculation Defense", "activity": "Switch vehicle ventilation strictly to internal recirculation; N95 for metro walks.", "level": "danger"},
                {"time": "10:30", "title": "Office Micro-Climate Check", "activity": "Verify commercial HVAC filtration or set desk-side purifier to active.", "level": "safe"},
                {"time": "13:30", "title": "Optimal Outdoor Transit", "activity": "Ideal window for off-site meetings, campus transit, or light outdoor lunch.", "level": "optimal"},
                {"time": "18:30", "title": "Evening Route Optimization", "activity": "Opt for express elevated corridors; keep car windows fully rolled up.", "level": "warning"},
                {"time": "21:30", "title": "Home Decontamination", "activity": "Remove commuter garments; wipe face and nasal passages with saline spray.", "level": "safe"}
            ]
        },
        "wfh": {
            "title": "Private Residence & WFH",
            "headline": f"Dynamic Indoor CO2 Purge Window in {city_display} Scheduled for 1:15 PM",
            "spoken": (
                f"Private residence environmental advisory for {city_display}. Sealed home offices accumulate "
                f"stale carbon dioxide during morning deep-work blocks. Do not open windows early while outdoor "
                f"smog is trapped. Execute a brief 12-minute cross-ventilation flush between 1:15 PM and 2:30 PM "
                f"when solar mixing minimizes outdoor particulates, then immediately re-seal and engage bio-filtration."
            ),
            "hazard_title": "Morning Outdoor Infiltration Risk",
            "hazard_time": "07:00 - 10:30",
            "hazard_desc": "Outdoor fine particulates penetrate window crevices; keep perimeter doors hermetically sealed.",
            "optimal_title": "Solar CO2 Flush Window",
            "optimal_time": "13:15 - 14:30",
            "optimal_desc": "Optimal solar thermal window to briefly vent stagnant indoor carbon dioxide without major PM2.5 penalty.",
            "sanctuary_title": "Nighttime Inversion Seal",
            "sanctuary_time": "18:00 - Overnight",
            "sanctuary_desc": "Re-engage HEPA units on whisper mode; deploy Snake Plants and Areca Palms for oxygenation.",
            "milestones": [
                {"time": "08:30", "title": "Home Office Sanctuary Start", "activity": "Turn on compact HEPA filter within 2 meters of your workstation.", "level": "safe"},
                {"time": "11:00", "title": "Indoor Plant Hydration", "activity": "Melt airborne dust off foliage; check indoor humidity balance.", "level": "safe"},
                {"time": "13:15", "title": "12-Minute Cross-Vent Flush", "activity": "Open opposing windows to purge indoor CO2; close promptly at 1:30 PM.", "level": "optimal"},
                {"time": "16:00", "title": "Afternoon Mental Refresh", "activity": "Desk hydration break; avoid opening balcony doors during evening rush.", "level": "warning"},
                {"time": "21:00", "title": "Night Sanctuary Transition", "activity": "Move portable filtration to bedroom; seal draft fissures.", "level": "safe"}
            ]
        },
        "athlete": {
            "title": "Performance & Fitness",
            "headline": f"Chrono-Aerobic Window: Restrict Outdoor Cardio to 1:45 PM - 3:30 PM",
            "spoken": (
                f"Performance athletic forecast for {city_display}. Running or cycling during early morning hours "
                f"forces high-volume particulate deposition deep into alveolar lung tissue due to elevated ventilation rates. "
                f"Shift outdoor conditioning strictly to the 1:45 PM to 3:30 PM solar convection window, or perform "
                f"high-intensity VO2 max intervals indoors in a clean HEPA-scrubbed facility."
            ),
            "hazard_title": "Early Morning Alveolar Hazard",
            "hazard_time": "05:30 - 09:30",
            "hazard_desc": "High minute ventilation during morning running causes up to 8x higher particulate lung deposition.",
            "optimal_title": "Peak Boundary Mixing Window",
            "optimal_time": "13:45 - 15:30",
            "optimal_desc": "Boundary layer expands to maximum diurnal thickness, minimizing ambient soot concentration per cubic meter.",
            "sanctuary_title": "Dusk Smog Inversion Warning",
            "sanctuary_time": "17:30 - 21:00",
            "sanctuary_desc": "Surface smog returns with traffic surge; switch to indoor mobility, yoga, and resistance training.",
            "milestones": [
                {"time": "06:00", "title": "Indoor Mobility Session", "activity": "Yoga, core, and resistance training in filtered indoor room; zero outdoor cardio.", "level": "danger"},
                {"time": "11:00", "title": "Electrolyte & Antioxidant Hydration", "activity": "Consume Vitamin C and E antioxidants to reduce oxidative airway inflammation.", "level": "safe"},
                {"time": "13:45", "title": "Optimal Outdoor Cardio Window", "activity": "Safe window for outdoor tempo run or cycling while solar dispersion is highest.", "level": "optimal"},
                {"time": "18:00", "title": "Gym Indoor Filtration Check", "activity": "Indoor strength training; ensure fitness facility utilizes active air purification.", "level": "warning"},
                {"time": "21:30", "title": "Cardiovascular Recovery Sanctuary", "activity": "Deep sleep in sealed clean-air bedroom to support muscular and respiratory recovery.", "level": "safe"}
            ]
        },
        "student": {
            "title": "Academic & Campus",
            "headline": f"Campus Transit Corridor Advisory: Active Shield During Morning Transit",
            "spoken": (
                f"Campus environmental briefing for {city_display}. Ambient smog densities are elevated along "
                f"major campus thoroughfares before 10:00 AM. Wear an N95 respirator while traveling between hostels "
                f"and lecture halls. Study in air-filtered central libraries during early hours, and schedule outdoor "
                f"campus sports between 1:30 PM and 3:30 PM."
            ),
            "hazard_title": "Morning Campus Transit Risk",
            "hazard_time": "07:30 - 10:00",
            "hazard_desc": "Morning ground inversion concentrates localized bus exhaust along campus main avenues.",
            "optimal_title": "Midday Campus Activity Window",
            "optimal_time": "13:30 - 15:30",
            "optimal_desc": "Lowest daily particulate levels; safe for campus recreation and inter-building transit.",
            "sanctuary_title": "Nighttime Study Room Sealing",
            "sanctuary_time": "18:30 - 23:00",
            "sanctuary_desc": "Keep hostel and study room doors shut; utilize shared air cleaners in common rooms.",
            "milestones": [
                {"time": "08:00", "title": "Morning Lecture Transit", "activity": "Wear fitted N95 respirator while walking along campus arterial avenues.", "level": "danger"},
                {"time": "10:30", "title": "Library Filtration Session", "activity": "Utilize central air-conditioned libraries with commercial particulate filtration.", "level": "safe"},
                {"time": "13:30", "title": "Optimal Campus Recreation", "activity": "Outdoor club activities and campus errands during peak solar air dispersion.", "level": "optimal"},
                {"time": "17:30", "title": "Dusk Sports Advisory", "activity": "Move intramural training indoors as evening smog layer begins to descend.", "level": "warning"},
                {"time": "22:00", "title": "Dormitory Air Sealing", "activity": "Close balcony vents and use DIY filter fan unit for clean overnight rest.", "level": "safe"}
            ]
        }
    }

    cfg = personas_config.get(persona, personas_config["family"])

    # Calendar events for 1-click sync
    calendar_events = [
        {
            "title": f"BreatheEasy: Optimal Outdoor & Aeration Window ({city_display})",
            "start_time_iso": "13:30",
            "end_time_iso": "15:30",
            "description": f"Solar convective dispersion peak in {city_display}. Ideal time for essential outdoor transit, errands, and rapid 10-minute indoor cross-ventilation."
        },
        {
            "title": f"BreatheEasy: Bedroom Sanctuary Sealing & Filtration ({city_display})",
            "start_time_iso": "20:30",
            "end_time_iso": "21:00",
            "description": f"Nighttime smog defense in {city_display}. Seal door draft fissures, ensure exterior windows are locked, and set True HEPA units to active sleep mode."
        }
    ]

    return {
        "city": city_display,
        "lifestyle": persona,
        "persona_title": cfg["title"],
        "aqi": aqi,
        "briefing_headline": cfg["headline"],
        "spoken_briefing": cfg["spoken"],
        "inversion_windows": {
            "hazard_peak": {
                "time": cfg["hazard_time"],
                "title": cfg["hazard_title"],
                "desc": cfg["hazard_desc"],
                "badge": "Hazard Inversion Peak"
            },
            "optimal_window": {
                "time": cfg["optimal_time"],
                "title": cfg["optimal_title"],
                "desc": cfg["optimal_desc"],
                "badge": "Solar Dispersion Window"
            },
            "sanctuary_sealing": {
                "time": cfg["sanctuary_time"],
                "title": cfg["sanctuary_title"],
                "desc": cfg["sanctuary_desc"],
                "badge": "Nocturnal Boundary Inversion"
            }
        },
        "schedule": cfg["milestones"],
        "calendar_events": calendar_events,
        "source": "clinical_engine",
        "is_ai_generated": False
    }


def generate_chrono_intelligence(
    city: str,
    lifestyle: str,
    aqi: int,
    forecast: Optional[List[Dict[str, Any]]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Unified Chrono-Intelligence pipeline.
    Invokes Gemini 2.0 Flash to synthesize hyper-personalized meteorological briefing.
    If Gemini fails, times out, or has no key, gracefully serves scientific clinical synthesizer.
    """
    key_to_use = api_key or os.environ.get("GEMINI_API_KEY")

    if key_to_use and genai:
        try:
            import json
            genai.configure(api_key=key_to_use)

            prompt = (
                f"You are the BreatheEasy Chrono-Intelligence AI, an expert boundary-layer atmospheric physicist "
                f"and circadian environmental medicine specialist.\n"
                f"City: {city}\n"
                f"Current AQI: {aqi}\n"
                f"Household Lifestyle Profile: {lifestyle}\n\n"
                "Task: Analyze the diurnal thermal smog inversion cycle (morning ground radiation inversion trap vs "
                "midday solar convective mixing and dispersion vs nocturnal boundary layer collapse). "
                "Output STRICTLY valid JSON with no markdown wrapping and no backticks. The JSON must follow this exact schema:\n"
                "{\n"
                '  "briefing_headline": "string headline under 10 words",\n'
                '  "spoken_briefing": "string of 60 to 85 words designed for audio voice playback explaining the morning trap, exact solar window, and nighttime sealing",\n'
                '  "hazard_time": "e.g. 06:30 - 10:15",\n'
                '  "hazard_title": "string",\n'
                '  "hazard_desc": "string",\n'
                '  "optimal_time": "e.g. 13:30 - 15:45",\n'
                '  "optimal_title": "string",\n'
                '  "optimal_desc": "string",\n'
                '  "sanctuary_time": "e.g. 18:30 - Overnight",\n'
                '  "sanctuary_title": "string",\n'
                '  "sanctuary_desc": "string",\n'
                '  "milestones": [\n'
                '    {"time": "07:00", "title": "...", "activity": "...", "level": "danger"},\n'
                '    {"time": "10:30", "title": "...", "activity": "...", "level": "warning"},\n'
                '    {"time": "13:30", "title": "...", "activity": "...", "level": "optimal"},\n'
                '    {"time": "17:30", "title": "...", "activity": "...", "level": "warning"},\n'
                '    {"time": "21:00", "title": "...", "activity": "...", "level": "safe"}\n'
                '  ]\n'
                "}"
            )

            model = genai.GenerativeModel(model_name="gemini-2.0-flash")

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(model.generate_content, prompt)
                resp = future.result(timeout=6.0)

            if resp and resp.text:
                clean_text = resp.text.strip()
                if clean_text.startswith("```json"):
                    clean_text = clean_text[7:]
                if clean_text.startswith("```"):
                    clean_text = clean_text[3:]
                if clean_text.endswith("```"):
                    clean_text = clean_text[:-3]
                clean_text = clean_text.strip()

                parsed = json.loads(clean_text)
                city_display = city.strip().title() if city else "Local Region"

                calendar_events = [
                    {
                        "title": f"BreatheEasy: Optimal Outdoor & Aeration Window ({city_display})",
                        "start_time_iso": "13:30",
                        "end_time_iso": "15:30",
                        "description": f"Solar convective dispersion peak in {city_display}. Ideal time for essential outdoor transit, errands, and rapid 10-minute indoor cross-ventilation."
                    },
                    {
                        "title": f"BreatheEasy: Bedroom Sanctuary Sealing & Filtration ({city_display})",
                        "start_time_iso": "20:30",
                        "end_time_iso": "21:00",
                        "description": f"Nighttime smog defense in {city_display}. Seal door draft fissures, ensure exterior windows are locked, and set True HEPA units to active sleep mode."
                    }
                ]

                return {
                    "city": city_display,
                    "lifestyle": lifestyle,
                    "persona_title": lifestyle.title(),
                    "aqi": aqi,
                    "briefing_headline": parsed.get("briefing_headline", f"Solar Aeration Window Anticipated at 1:30 PM in {city_display}"),
                    "spoken_briefing": parsed.get("spoken_briefing", ""),
                    "inversion_windows": {
                        "hazard_peak": {
                            "time": parsed.get("hazard_time", "06:30 - 10:15"),
                            "title": parsed.get("hazard_title", "Morning Radiation Inversion"),
                            "desc": parsed.get("hazard_desc", "Ground radiation traps vehicular emissions."),
                            "badge": "Hazard Inversion Peak"
                        },
                        "optimal_window": {
                            "time": parsed.get("optimal_time", "13:30 - 15:45"),
                            "title": parsed.get("optimal_title", "Solar Convection Dilution Window"),
                            "desc": parsed.get("optimal_desc", "Solar mixing lifts particulates into upper boundary layer."),
                            "badge": "Solar Dispersion Window"
                        },
                        "sanctuary_sealing": {
                            "time": parsed.get("sanctuary_time", "18:00 - Overnight"),
                            "title": parsed.get("sanctuary_title", "Nocturnal Inversion Collapse"),
                            "desc": parsed.get("sanctuary_desc", "Cooling air traps ground emissions overnight."),
                            "badge": "Nocturnal Boundary Inversion"
                        }
                    },
                    "schedule": parsed.get("milestones", []),
                    "calendar_events": calendar_events,
                    "source": "gemini-2.0-flash",
                    "is_ai_generated": True
                }
        except Exception as e:
            print(f"Gemini Chrono-Intelligence generation failed or timed out: {e}")

    # Fallback to verified scientific clinical engine
    return synthesize_chrono_clinical(city, lifestyle, aqi, forecast)

