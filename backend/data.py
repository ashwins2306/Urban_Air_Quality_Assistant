"""
BreatheEasy Comprehensive Data Module
======================================
This module provides curated, scientifically grounded datasets and impact parameters
for the BreatheEasy clean air and environmental health platform.

Contents:
- CITY_AQI_DATA: Real-time representative air quality metrics, pollutant profiles,
                 health advisories, and targeted quick actions for 16 global metropolitan areas.
- ROOM_TIPS: Granular, room-specific mitigation protocols and low-emission indoor practices.
- DIY_PROJECTS: Open-source, high-efficiency homemade air cleaners and bio-filtration setups.
- PLANTS_DATA: Botanical air purification species evaluated under NASA Clean Air research.
- ALTERNATIVES_DATA: Sustainable behavioral, energy, and appliance swaps with measurable carbon
                     and health co-benefits across 6 core lifestyle sectors.
- COMMUNITY_INITIATIVES: Grassroots neighborhood actions for clean air advocacy and greening.
- PLEDGES: High-impact personal commitments for reducing community and personal pollution.
- ROUTINE_TEMPLATES: Daily circadian routine recommendations tailored to 7 distinct demographic personas.
- IMPACT_FACTORS: Normalized carbon & pollutant emission factors for personal impact calculations.
"""

from typing import Dict, List, Any, Optional

# ==============================================================================
# 1. CITY AQI DATA (Zero Hardcoded City Data - 100% Live Telemetry)
# ==============================================================================

CITY_AQI_DATA: Dict[str, Dict[str, Any]] = {}

# ==============================================================================
# 2. ROOM TIPS (5 Rooms x 5 Tips each)
# ==============================================================================

ROOM_TIPS: Dict[str, List[Dict[str, str]]] = {
    "living": [
        {
            "emoji": "🪟",
            "title": "Dynamic Cross-Ventilation Strategy",
            "difficulty": "easy",
            "description": (
                "Open windows on opposite sides of your living area during low-traffic afternoon windows "
                "to establish natural cross-breezes that flush out indoor airborne pollutants. Always check "
                "your local AQI before opening windows to prevent high outdoor particulate matter from entering. "
                "Pair ventilation with weatherstripped interior doors to isolate polluted zones."
            ),
            "impact_text": "Flushes up to 80% of accumulated indoor VOCs and CO2 within 15 minutes.",
        },
        {
            "emoji": "🌀",
            "title": "Centralized True HEPA Air Purifier Placement",
            "difficulty": "easy",
            "description": (
                "Position your air purifier in the center of the living room at least two feet away from walls "
                "and bulky furniture to allow unrestricted 360-degree intake. Running the unit on a continuous "
                "low-noise fan setting keeps air circulating without kicking up settled dust. Replace HEPA and "
                "activated carbon filter packs every six to eight months depending on usage."
            ),
            "impact_text": "Reduces airborne PM2.5 and fine aerosol concentrations by 85-95%.",
        },
        {
            "emoji": "🛋️",
            "title": "Choose Low-VOC Furnishings and Natural Textiles",
            "difficulty": "medium",
            "description": (
                "Conventional sofas and pressed-wood coffee tables off-gas toxic formaldehyde and polyurethane "
                "fumes for years after manufacturing. Choose solid timber furniture finished with natural beeswax "
                "or plant oils, along with OEKO-TEX certified linen and organic cotton upholstery. This fundamentally "
                "eliminates the primary indoor source of chronic chemical vapors."
            ),
            "impact_text": "Lowers indoor volatile organic compound (TVOC) levels by up to 60%.",
        },
        {
            "emoji": "🧹",
            "title": "Static-Free Damp Microfiber Dusting Routine",
            "difficulty": "easy",
            "description": (
                "Feather dusters and dry cloths simply launch settled fine particles, pet dander, and flame retardants "
                "back into your breathable air. Wipe all coffee tables, TV consoles, and shelves using a slightly damp "
                "microfiber towel that physically traps particulate matter. Vacuum afterward using a sealed-canister "
                "cleaner equipped with an exhaust HEPA filter."
            ),
            "impact_text": "Prevents particle re-suspension and cuts inhalable dust load by 70%.",
        },
        {
            "emoji": "🪴",
            "title": "Living Botanical Air Defense Cluster",
            "difficulty": "easy",
            "description": (
                "Group four to six broad-leaf air-purifying houseplants such as Areca palms and Rubber plants in bright "
                "living room corners. Plant foliage creates micro-convection currents that pull ambient air into the soil "
                "where microbial colonies metabolize volatile chemicals. Keep leaf surfaces clean with a damp cloth so "
                "their stomata continue actively absorbing airborne toxins."
            ),
            "impact_text": "Boosts natural oxygenation and removes residual trace benzene and xylene.",
        },
    ],
    "bedroom": [
        {
            "emoji": "👟",
            "title": "Strict Shoe-Free Sanctuary Policy",
            "difficulty": "easy",
            "description": (
                "Outdoor footwear tracks in toxic roadway heavy metals, pet waste bacteria, industrial coal dust, "
                "and lawn pesticides directly onto bedroom rugs. Place an exterior bristled doormat and an indoor "
                "shoe rack right at the entry to keep outdoor contaminants strictly quarantined. Transitioning to dedicated "
                "indoor slippers prevents coarse and fine particulate buildup near where you sleep."
            ),
            "impact_text": "Reduces tracked-in outdoor toxins and floor particulate matter by 80%.",
        },
        {
            "emoji": "🛏️",
            "title": "Weekly 60°C Hypoallergenic Bedding Thermal Wash",
            "difficulty": "easy",
            "description": (
                "Pillows, duvet covers, and bedsheets harbor millions of dust mites, shed skin cells, and microscopic "
                "airborne spores that trigger nocturnal congestion. Wash all bedding weekly in hot water at 60°C (140°F) "
                "to eradicate dust mites and denature protein allergens completely. Encase mattresses and pillows in zippered "
                "micro-porous allergen barrier covers for long-term defense."
            ),
            "impact_text": "Eliminates 99% of dust mite allergens and significantly eases night asthma.",
        },
        {
            "emoji": "🌙",
            "title": "Overnight Whisper-Quiet HEPA Filtration",
            "difficulty": "easy",
            "description": (
                "Run a dedicated bedroom air purifier continuously on sleep or night mode positioned three to five feet "
                "from your headboard. Keeping the bedroom door mostly closed allows the purifier to establish a clean "
                "micro-climate with ultra-low PM2.5 while you sleep. The continuous clean airflow reduces airway inflammation, "
                "eliminates snoring triggers, and deepens restorative sleep."
            ),
            "impact_text": "Maintains bedroom PM2.5 below 5 µg/m³ for restorative sleep.",
        },
        {
            "emoji": "🕯️",
            "title": "Banish Synthetic Candles, Sprays, and Incense",
            "difficulty": "easy",
            "description": (
                "Burning paraffin wax candles and synthetic incense sticks floods confined bedroom air with soot, benzene, "
                "toluene, and phthalates. Even synthetic plug-in air fresheners emit continuous plumes of neurotoxic fragrance "
                "compounds and formaldehyde. Replace synthetic aromas with pure clean air, or use 100% natural beeswax "
                "candles burned only in ventilated rooms."
            ),
            "impact_text": "Cuts indoor soot and carcinogenic volatile aromatic hydrocarbons by 90%.",
        },
        {
            "emoji": "💧",
            "title": "Maintain 40%-50% Relative Humidity Balance",
            "difficulty": "medium",
            "description": (
                "Dry indoor air dries out sensitive nasal mucous membranes, while excess humidity over 60% fuels rampant "
                "mold colonies and dust mite proliferation. Deploy an ultrasonic cool-mist humidifier filled strictly with "
                "distilled or reverse-osmosis water during dry winter nights. Monitor room moisture with a digital hygrometer "
                "to ensure ambient humidity stays strictly within the healthy 40% to 50% window."
            ),
            "impact_text": "Preserves mucosal barrier defense and stops mold proliferation.",
        },
    ],
    "kitchen": [
        {
            "emoji": "🍳",
            "title": "Always Run Range Hood on High with Back Burner Cooking",
            "difficulty": "easy",
            "description": (
                "Turn on your kitchen range exhaust hood at least two minutes before lighting the stove and cook primarily "
                "on the back burners where exhaust capture is highest. Keep the fan running for ten minutes after cooking "
                "ends to purge lingering ultrafine grease droplets and combustion gases. If your hood recirculates air, "
                "ensure its aluminum grease meshes are degreased monthly and activated carbon pads are replaced regularly."
            ),
            "impact_text": "Captures up to 75% of cooking-generated ultrafine particles and moisture.",
        },
        {
            "emoji": "⚡",
            "title": "Switch from Gas to Induction Cooktops",
            "difficulty": "medium",
            "description": (
                "Burning methane or propane gas generates concentrated pulses of nitrogen dioxide, carbon monoxide, and unburned "
                "benzene right in your breathing zone. Portable or built-in magnetic induction cooktops heat cookware directly "
                "using electromagnetic coils, producing zero combustion byproducts. Induction also cooks twice as fast while "
                "keeping kitchen surfaces cool and significantly safer."
            ),
            "impact_text": "Eliminates 100% of cooking combustion gases (NO2, CO, and benzene).",
        },
        {
            "emoji": "🥑",
            "title": "High-Smoke-Point Cooking Oils & Splatter Traps",
            "difficulty": "easy",
            "description": (
                "Heating low-smoke-point oils like unrefined butter or extra virgin olive oil past their thermal thresholds "
                "causes violent lipid degradation into toxic acrolein and aerosolized PM2.5. Cook with high-stability oils "
                "such as avocado, ghee, or high-oleic safflower oil for high-temperature searing and stir-frying. Always cap "
                "skillets with fine stainless steel mesh splatter screens to trap aerosolized grease droplets before they escape."
            ),
            "impact_text": "Reduces kitchen PM2.5 spikes from 400 µg/m³ to under 30 µg/m³.",
        },
        {
            "emoji": "🍋",
            "title": "Natural Citrus & Vinegar Surface Degreasing",
            "difficulty": "easy",
            "description": (
                "Commercial aerosol oven and degreasing sprays discharge caustic sodium hydroxide, chlorinated solvents, "
                "and synthetic chemical fragrances into kitchen air. Clean countertops and greasy stovetops using a simple solution "
                "of white distilled vinegar, warm water, and citrus peel extracts. Adding baking soda paste creates a non-toxic foaming "
                "scrub that cuts through stubborn grease without irritating your lungs."
            ),
            "impact_text": "Prevents toxic chemical vapor inhalation and leaves zero chemical residue.",
        },
        {
            "emoji": "🧽",
            "title": "Sanitize Sponges & Prevent Hidden Kitchen Mold",
            "difficulty": "easy",
            "description": (
                "Damp kitchen sponges and wet sink undersides are breeding grounds for black mold and bacterial biofilms that "
                "aerosolize spores into the air. Microwave damp cellulose sponges for two minutes or run them through the dishwasher "
                "sanitizing cycle every two days. Fix leaking under-sink pipe couplings immediately to prevent mold colonies "
                "from establishing behind cabinets."
            ),
            "impact_text": "Stops mold spore dispersion and eliminates musty kitchen odors.",
        },
    ],
    "kids": [
        {
            "emoji": "🧸",
            "title": "Low-Level Floor Breathing Zone Clearance",
            "difficulty": "easy",
            "description": (
                "Toddlers and crawling infants breathe air within 10 to 18 inches of the floor where heavy settled particulate "
                "matter and chemical vapors concentrate. Keep nursery floors spotless by vacuuming daily with a sealed HEPA "
                "cleaner and wiping with warm water rather than chemical detergents. Position nursery air purifiers at floor level "
                "rather than up on high shelves to clean the exact zone where children play."
            ),
            "impact_text": "Reduces child inhalation of heavy floor-level micro-dust by up to 70%.",
        },
        {
            "emoji": "🧺",
            "title": "Certified Organic Non-Toxic Play Surfaces",
            "difficulty": "easy",
            "description": (
                "Standard EVA foam play mats and synthetic area rugs often off-gas formamide, phthalate plasticizers, and volatile "
                "flame retardants. Replace synthetic rubber floor mats with OEKO-TEX certified organic cotton play quilts or natural "
                "food-grade silicone mats. These natural alternatives provide gentle cushioning while eliminating direct skin and "
                "respiratory contact with toxic chemicals."
            ),
            "impact_text": "Eliminates child exposure to endocrine-disrupting plasticizers and formamide.",
        },
        {
            "emoji": "🪵",
            "title": "Solid Unfinished Wood Toys and Crib Furniture",
            "difficulty": "medium",
            "description": (
                "Particleboard cribs, MDF dressers, and cheap plastic toys continuously release formaldehyde resins and volatile "
                "plasticizers into nursery air. Furnish children's bedrooms with solid untreated pine, birch, or beech wood treated "
                "with natural food-safe beeswax or plant-based sealants. When assembling new furniture, allow items to off-gas in a "
                "well-ventilated garage or balcony for two weeks before placing them in the child's room."
            ),
            "impact_text": "Cuts nursery formaldehyde concentrations by over 75%.",
        },
        {
            "emoji": "💨",
            "title": "Strict Hygiene for Nursery Humidifiers",
            "difficulty": "easy",
            "description": (
                "Dirty ultrasonic humidifiers act as microbial aerosol generators, spraying mineral white dust, bacteria, and mold "
                "spores directly into children's developing lungs. Clean the water reservoir daily with white vinegar, scrub all internal "
                "gaskets, and refill exclusively with distilled or demineralized water. Never leave stagnant water inside the humidifier "
                "basin when not in active use."
            ),
            "impact_text": "Prevents 'humidifier lung' hypersensitivity pneumonitis and mineral dust inhalation.",
        },
        {
            "emoji": "🚪",
            "title": "Weatherstripped Door Seals & Bedtime AQI Routine",
            "difficulty": "medium",
            "description": (
                "Install silicone bulb weatherstripping around nursery window frames and a flexible silicone draft stopper under the bedroom door. "
                "This isolates the child's room from outside street smog and household cooking fumes drifting through corridors. "
                "Combine this seal with an automated night air purifier running on medium-low to maintain a pristine sleeping environment."
            ),
            "impact_text": "Creates an airtight protective barrier against outside and kitchen pollution.",
        },
    ],
    "office": [
        {
            "emoji": "🧠",
            "title": "CO2 Dilution & Cognitive Air Refreshment",
            "difficulty": "easy",
            "description": (
                "In closed home offices or conference rooms, exhaled carbon dioxide frequently exceeds 1,500 ppm, causing drowsiness, "
                "headaches, and a 30% drop in cognitive performance. Crack an exterior window an inch or open the office door every 45 minutes "
                "to restore fresh oxygen and drop indoor CO2 below 800 ppm. Use a compact NDIR CO2 monitor to track ventilation efficiency "
                "and keep your mind sharp."
            ),
            "impact_text": "Keeps CO2 under 800 ppm, boosting focus, decision-making, and mental stamina.",
        },
        {
            "emoji": "🖨️",
            "title": "Laser Printer & Copier Emission Isolation",
            "difficulty": "medium",
            "description": (
                "Laser printers and toner copiers emit significant clouds of ultrafine carbon black toner particles, volatile organic "
                "chemicals, and ozone during active print cycles. Relocate heavy office printers to a dedicated, ventilated utility closet "
                "or keep them at least eight feet away from your primary desk. Always ventilate the area immediately after executing large print runs."
            ),
            "impact_text": "Prevents direct exposure to ozone and carcinogenic toner nanoparticles.",
        },
        {
            "emoji": "🖥️",
            "title": "Desktop Mini-HEPA Personal Breathing Zone Purifier",
            "difficulty": "easy",
            "description": (
                "Place a compact True HEPA desktop air purifier right beside your computer monitor angled gently toward your face. "
                "This delivers a continuous stream of filtered, particulate-free air directly into your immediate breathing zone "
                "throughout the workday. It also creates a gentle positive pressure zone that deflects ambient dust and allergens away from your face."
            ),
            "impact_text": "Delivers 99.97% clean air directly to your breathing zone while seated.",
        },
        {
            "emoji": "🔌",
            "title": "Electronics Anti-Static Dust Management",
            "difficulty": "easy",
            "description": (
                "Computer cooling fans, monitors, and power supplies generate electrostatic charges that attract and bake airborne dust, "
                "volatilizing flame retardants into the air. Clean computer air intake filters, fan grilles, and tangle-prone cable raceways "
                "monthly using an anti-static soft brush and vacuum nozzle. Keeping electronic components free of dust also improves cooling "
                "efficiency and lengthens device lifespans."
            ),
            "impact_text": "Reduces off-gassed brominated flame retardants and airborne electrical dust.",
        },
        {
            "emoji": "🌱",
            "title": "Desk Flora Air Scrubbers (ZZ & Snake Plants)",
            "difficulty": "easy",
            "description": (
                "Keep low-maintenance air-purifying plants such as Zamioculcas zamiifolia (ZZ plant) and Sansevieria directly on your office "
                "workstation. These resilient species thrive under artificial office fluorescent and LED lighting while naturally scrubbing trace "
                "computer plastics and toner off-gassing. Their natural green foliage also reduces visual eye strain and lowers cortisol stress levels."
            ),
            "impact_text": "Enhances desk air freshness, lowers stress hormones, and absorbs ambient VOCs.",
        },
    ],
}

# ==============================================================================
# 3. DIY PROJECTS (4 Projects)
# ==============================================================================

DIY_PROJECTS: List[Dict[str, Any]] = [
    {
        "emoji": "📦",
        "title": "Corsi-Rosenthal Box Air Cleaner",
        "description": (
            "The Corsi-Rosenthal box is an open-source, high-efficiency do-it-yourself air cleaner engineered "
            "with four MERV 13 furnace filters arranged in a cube around a standard 20-inch box fan. It delivers "
            "Clean Air Delivery Rates (CADR) that match or exceed commercial air purifiers costing hundreds of dollars, "
            "capturing wildfire smoke, allergens, respiratory droplets, and fine particulates at low operating cost."
        ),
        "materials": [
            "1x 20-inch standard electric box fan",
            "4x MERV 13 furnace filters (20x20x2 inch or 20x20x1 inch)",
            "1x 20x20 inch cardboard bottom panel (cut from fan box)",
            "Heavy-duty duct tape or gaffer tape (2-inch wide)",
            "Cardboard circular shroud cutout (enhances fan airflow efficiency by 20%)",
        ],
        "effectiveness": (
            "Removes 90%+ of airborne PM2.5, pollen, and pet dander within 30 minutes; "
            "achieves CADR of 250-300 CFM at approximately one-fifth the cost of commercial units."
        ),
    },
    {
        "emoji": "🥫",
        "title": "Activated Carbon Cannister VOC Scrubber",
        "description": (
            "An active adsorption filtration cylinder engineered from perforated steel mesh canisters packed "
            "with virgin pelletized activated coconut-shell carbon, powered by an energy-efficient inline duct fan. "
            "This project specifically targets volatile organic compounds (VOCs), formaldehyde, gasoline fumes, "
            "cooking odors, and ozone that pass directly through standard mechanical particulate filters."
        ),
        "materials": [
            "1x 4-inch or 6-inch inline centrifugal duct fan (150-200 CFM)",
            "Perforated double-wall cylindrical mesh canister (or nested wire mesh cylinders)",
            "2 kg virgin pelletized activated coconut-shell carbon (4mm pellets, CTC 60+)",
            "Washable polyester pre-filter mesh wrap sleeve",
            "Adjustable stainless steel worm-gear hose clamps and rubber reducer coupling",
        ],
        "effectiveness": (
            "Reduces indoor TVOC concentrations by 70-85% and eliminates stubborn chemical and cooking odors "
            "in enclosed residential spaces up to 350 sq ft."
        ),
    },
    {
        "emoji": "🪟",
        "title": "Electrostatic Micro-Mesh Window Screen Frame",
        "description": (
            "A lightweight custom-fitted window screen insert strung with dual-layer electrostatic PM2.5 filter mesh "
            "and nano-fiber screen cloth. It allows natural cross-ventilation breezes to cool living spaces while "
            "mechanically and electrostatically capturing coarse road dust, pollen, tire wear, and vehicle soot before "
            "they enter your home."
        ),
        "materials": [
            "Extruded aluminum or lightweight pine window screen frame kit (sized to window)",
            "Electrostatic meltblown polypropylene filter mesh (PM2.5 rated)",
            "Rubber spline cord and roller rolling tool",
            "Adhesive EVA foam weatherstripping tape (for perimeter airtightness)",
            "Removable spring clips or magnetic mounting tape strips",
        ],
        "effectiveness": (
            "Blocks up to 65% of ambient outdoor PM10 and 40-50% of PM2.5 while preserving "
            "natural passive airflow and outdoor illumination."
        ),
    },
    {
        "emoji": "🌿",
        "title": "Living Bio-Wall Air Column with Submerged Aeration",
        "description": (
            "A compact vertical hydroponic bio-filter column that mechanically draws room air through the root zones "
            "of resilient air-purifying plants growing in expanded clay pebbles and bio-char. Rhizosphere bacteria "
            "and mycorrhizae actively metabolize formaldehyde, benzene, and nitrates, turning harmful indoor toxins "
            "into organic plant nutrients while naturally balancing room humidity."
        ),
        "materials": [
            "Vertical tiered modular wall planter or slotted 6-inch PVC drainage pipe",
            "Submersible quiet aquarium water pump with cycling timer (5W-10W)",
            "Hydroponic expanded clay pebbles (hydroton) mixed with activated bio-char",
            "Aquarium aeration pump with ceramic air diffuser stone",
            "Selected bio-active plants: Golden Pothos, Spider Plants, and Boston Ferns",
        ],
        "effectiveness": (
            "Achieves 3-4x the VOC removal rate of standard static potted plants through active "
            "convective rhizosphere bio-filtration and transpiration."
        ),
    },
]

# ==============================================================================
# 4. PLANTS DATA (6 NASA Clean Air Plants)
# ==============================================================================

PLANTS_DATA: List[Dict[str, Any]] = [
    {
        "emoji": "🪴",
        "name": "Snake Plant (Sansevieria trifasciata)",
        "description": (
            "An exceptionally hardy architectural succulent renowned for Crassulacean Acid Metabolism (CAM), "
            "meaning it opens its stomata at night to absorb carbon dioxide and release oxygen while you sleep. "
            "It is highly tolerant of neglect and thrives in low-light bedroom corners."
        ),
        "benefits": [
            "Releases pure oxygen and absorbs CO2 throughout the night",
            "Filters toxic airborne formaldehyde, benzene, xylene, and toluene",
            "Extremely drought tolerant and requires watering only every 2-3 weeks",
            "Naturally balances bedroom humidity and soothes airway irritation",
        ],
        "care_level": "Easy",
    },
    {
        "emoji": "🕷️",
        "name": "Spider Plant (Chlorophytum comosum)",
        "description": (
            "A resilient, cascading houseplant with arching variegated foliage that is completely non-toxic to cats and dogs. "
            "NASA clean air trials demonstrated that spider plants can remove up to 95% of airborne formaldehyde, "
            "carbon monoxide, and xylene from sealed test chambers within 24 hours."
        ),
        "benefits": [
            "100% non-toxic and pet-friendly for homes with dogs and cats",
            "Proven rapid elimination of formaldehyde, carbon monoxide, and xylene",
            "Rapidly produces offshoot plantlets for effortless home propagation",
            "Tolerates varied watering schedules and wide temperature ranges",
        ],
        "care_level": "Easy",
    },
    {
        "emoji": "🕊️",
        "name": "Peace Lily (Spathiphyllum wallisii)",
        "description": (
            "A stately tropical plant featuring deep glossy green leaves and graceful white floral spathes. "
            "It is one of the most capable bio-filters identified in NASA studies, actively breaking down chemical solvents "
            "while subtly releasing natural moisture to humidify dry indoor environments."
        ),
        "benefits": [
            "Filters trichloroethylene, benzene, formaldehyde, xylene, and ammonia",
            "High transpiration rate naturally humidifies dry, air-conditioned rooms",
            "Visual watering indicator: foliage droops gently when thirsty and springs back within hours",
            "Thrives in shaded, low-light spaces away from harsh direct sunlight",
        ],
        "care_level": "Moderate",
    },
    {
        "emoji": "🌿",
        "name": "Boston Fern (Nephrolepis exaltata)",
        "description": (
            "A lush, graceful fern with feathery fronds that serves as an extraordinary living humidifier and chemical scavenger. "
            "It excels at removing airborne formaldehyde released from synthetic carpets, adhesives, and pressed-wood cabinets "
            "while restoring moisture balance to dry air."
        ),
        "benefits": [
            "Top-tier natural humidifier capable of transpiring up to 1 liter of water per day",
            "High-efficiency removal of airborne formaldehyde and combustion byproducts",
            "Soft, luxuriant green foliage enhances mental calm and lowers visual fatigue",
            "Thrives in humid environments like bathrooms and misted living areas",
        ],
        "care_level": "Moderate",
    },
    {
        "emoji": "🌴",
        "name": "Areca Palm (Dypsis lutescens)",
        "description": (
            "Also known as the Butterfly Palm, this elegant feathered palm produces large volumes of oxygen and acts "
            "as a powerful indoor air purifier. A cluster of adult Areca palms can maintain healthy ambient humidity "
            "in an entire living room while continuously absorbing volatile toxins."
        ),
        "benefits": [
            "High oxygen production and electrostatic particulate settling capacity",
            "Removes acetone, xylene, toluene, and trace carbon monoxide",
            "Completely safe and non-toxic for curious household pets",
            "Emits abundant moisture into dry, climate-controlled indoor air",
        ],
        "care_level": "Moderate",
    },
    {
        "emoji": "🍃",
        "name": "Rubber Plant (Ficus elastica)",
        "description": (
            "A bold, dramatic plant with broad, leathery, dark-green leaves engineered to trap suspended dust particles "
            "and absorb volatile chemicals. Its expansive leaf surface area captures airborne toxins and channels them "
            "to roots where soil microorganisms break them down permanently."
        ),
        "benefits": [
            "Expansive broad leaves physically trap airborne dust and fine particles",
            "Superior capacity for metabolizing airborne formaldehyde and chemical vapors",
            "Highly resistant to common houseplant pests, under-watering, and disease",
            "Requires only moderate watering and thrives in bright, indirect light",
        ],
        "care_level": "Easy",
    },
]

# ==============================================================================
# 5. ALTERNATIVES DATA (12 Swaps across 6 Categories)
# ==============================================================================

ALTERNATIVES_DATA: List[Dict[str, str]] = [
    # Transport (2 items)
    {
        "category": "transport",
        "emoji": "🚲",
        "title": "Daily Commuter E-Bike or Bicycle",
        "swap_from": "Solo internal combustion engine (ICE) automobile commuting",
        "swap_to": "Pedal-assist commuter e-bike or standard bicycle",
        "description": (
            "Replacing short-to-medium solo gasoline car commutes with a pedal-assist electric bicycle eliminates tailpipe emissions "
            "entirely while bypassing bumper-to-bumper gridlock. Modern e-bikes provide effortless hill climbing and cargo hauling "
            "without excessive sweat, making active transport practical for daily work trips."
        ),
        "co2_savings": "1.9 tonnes CO2e / year",
        "health_impact": "Cuts personal exposure to vehicle-cabin toxic exhaust fumes by 60%; improves cardiovascular fitness.",
        "cost_impact": "Saves $1,800 - $2,500 annually in gasoline, parking, tolls, and vehicle maintenance.",
    },
    {
        "category": "transport",
        "emoji": "🚇",
        "title": "Electrified Rail & Rapid Transit Commuting",
        "swap_from": "Single-occupancy car driving in highway congestion",
        "swap_to": "Metro, commuter train, or electric bus rapid transit",
        "description": (
            "Electrified mass transit moves hundreds of commuters per kilowatt-hour, drastically reducing vehicular congestion "
            "and roadside nitrogen dioxide pollution. Trading driving stress for train travel creates productive transit time for reading, "
            "resting, or working while shrinking your personal transit footprint."
        ),
        "co2_savings": "2.4 tonnes CO2e / year",
        "health_impact": "Lowers daily intake of carcinogenic diesel particulate soot; reduces chronic commuting stress and blood pressure.",
        "cost_impact": "Saves $2,200 annually on fuel, insurance premiums, parking permits, and vehicle depreciation.",
    },

    # Cooking (2 items)
    {
        "category": "cooking",
        "emoji": "⚡",
        "title": "Smart Magnetic Induction Cooktop",
        "swap_from": "Unvented methane gas or LPG stove burners",
        "swap_to": "High-efficiency magnetic induction cooktop",
        "description": (
            "Induction cooktops heat cookware directly using electromagnetic fields, operating at 85-90% thermal efficiency compared "
            "to 40% for conventional gas flames. Switching to induction eliminates indoor combustion byproducts including nitrogen dioxide, "
            "carbon monoxide, and unburned benzene right in your kitchen breathing zone."
        ),
        "co2_savings": "0.45 tonnes CO2e / year",
        "health_impact": "Decreases childhood asthma incidence risk by up to 42% by eliminating open-flame NO2 and benzene emissions.",
        "cost_impact": "Cooks 50% faster than gas; cuts monthly cooking fuel utility costs by 20-35%.",
    },
    {
        "category": "cooking",
        "emoji": "💨",
        "title": "Sealed Convection Air Frying & Steaming",
        "swap_from": "Open-pan shallow or deep oil frying on stovetops",
        "swap_to": "Sealed countertop convection air fryer and multicooker",
        "description": (
            "Open-pan frying atomizes cooking oils into ultrafine oil aerosols (PM2.5) that linger indoors for hours and coat respiratory passages. "
            "Sealed convection air fryers circulate superheated air in a contained chamber, achieving crisp textures with 80% less oil "
            "while trapping aerosolized grease within washable filter cavities."
        ),
        "co2_savings": "0.15 tonnes CO2e / year",
        "health_impact": "Prevents indoor PM2.5 spikes from exceeding 350 µg/m³, reducing chronic airway inflammation and coughing.",
        "cost_impact": "Reduces household cooking oil purchases by 75%, saving $120-$180 per year in grocery bills.",
    },

    # Heating (2 items)
    {
        "category": "heating",
        "emoji": "🌡️",
        "title": "Inverter Mini-Split Air-Source Heat Pump",
        "swap_from": "Unvented kerosene space heater or aging gas furnace",
        "swap_to": "Variable-speed inverter mini-split heat pump",
        "description": (
            "Heat pumps transfer existing ambient heat rather than burning combustible fuel, delivering 3 to 4 units of thermal warmth "
            "for every unit of electricity consumed. Switching away from combustible space heaters removes toxic carbon monoxide, soot, "
            "and nitrogen dioxide risks from your living quarters completely."
        ),
        "co2_savings": "3.2 tonnes CO2e / year",
        "health_impact": "Eliminates carbon monoxide poisoning risks and prevents indoor sulfur dioxide and soot accumulation.",
        "cost_impact": "Cuts winter heating bills by 40-60% compared to electric resistance heating or kerosene heaters.",
    },
    {
        "category": "heating",
        "emoji": "🪵",
        "title": "EPA-Certified Clean Pellet Stove",
        "swap_from": "Traditional open-hearth wood fireplace or older wood burner",
        "swap_to": "Sealed automated wood pellet stove with outside combustion air intake",
        "description": (
            "Traditional open fireplaces pull warm air from rooms while exhausting up to 30 grams of toxic smoke particulate per hour "
            "into the neighborhood. Certified pellet stoves burn recycled compressed sawdust pellets under forced draft with 80%+ efficiency, "
            "cutting particulate emissions by over 90% while ducting all exhaust outside."
        ),
        "co2_savings": "1.8 tonnes CO2e / year",
        "health_impact": "Prevents toxic wood smoke creosote, polycyclic aromatic hydrocarbons (PAHs), and fine ash from entering living quarters.",
        "cost_impact": "Burns dense fuel pellets with 80%+ efficiency, saving $350-$600 annually in heating fuel costs.",
    },

    # Shopping (2 items)
    {
        "category": "shopping",
        "emoji": "👕",
        "title": "Durable Natural Fiber Capsule Wardrobe",
        "swap_from": "Fast-fashion synthetic garments (polyester, nylon, acrylic)",
        "swap_to": "GOTS-certified organic cotton, linen, hemp, and durable wool",
        "description": (
            "Synthetic textiles shed millions of microplastic fibers into household air during wear and laundering, releasing petrochemical "
            "fumes and flame-retardant dust. Investing in high-durability natural fiber clothing ensures non-toxic breathability, skin comfort, "
            "and complete biodegradability at the end of the garment lifecycle."
        ),
        "co2_savings": "0.55 tonnes CO2e / year",
        "health_impact": "Eliminates airborne synthetic microplastic fiber shedding in bedrooms; prevents skin absorption of toxic dyes.",
        "cost_impact": "Higher upfront quality pays back through 3-5x longer lifespan, saving $400+ annually on apparel.",
    },
    {
        "category": "shopping",
        "emoji": "🧴",
        "title": "Concentrated Dissolvable Refills & Solid Bars",
        "swap_from": "Single-use plastic bottled detergents, shampoos, and cleaning sprays",
        "swap_to": "Dehydrated dissolvable cleaning tablets and solid shampoo bars",
        "description": (
            "Conventional bottled household cleaners consist of 90% water shipped in heavy single-use polyethylene bottles. Choosing "
            "compact dissolvable concentrate tablets and solid bars eliminates freight shipping emissions, eliminates plastic bottle waste, "
            "and avoids synthetic chemical fragrances that off-gas indoors."
        ),
        "co2_savings": "0.28 tonnes CO2e / year",
        "health_impact": "Avoids synthetic chemical fragrance off-gassing and phthalate exposure from cheap plastic containers.",
        "cost_impact": "Saves $150-$250 annually by paying only for active cleaning concentrates rather than bottled water and packaging.",
    },

    # Waste (2 items)
    {
        "category": "waste",
        "emoji": "🍂",
        "title": "Aerobic Yard Waste Composting & Mulching",
        "swap_from": "Open-air backyard burning of dry leaves, twigs, and garden waste",
        "swap_to": "Dual-chamber tumbling composter and organic garden mulch",
        "description": (
            "Burning garden clippings and dried leaves releases dense plumes of toxic carbon monoxide, black carbon soot, and hazardous "
            "dioxins into neighborhood air. Composting converts yard waste into moisture-retaining organic humus that enriches garden soil, "
            "locks carbon in the ground, and keeps local air completely smoke-free."
        ),
        "co2_savings": "0.85 tonnes CO2e / year",
        "health_impact": "Protects neighbors and children from severe asthma attacks, stinging eyes, and acute respiratory distress from yard smoke.",
        "cost_impact": "Provides free nutrient-rich garden compost and mulch, saving $100-$180 annually on commercial soil fertilizers.",
    },
    {
        "category": "waste",
        "emoji": "🪱",
        "title": "Bokashi Anaerobic Kitchen Fermentation & Vermicomposting",
        "swap_from": "Dumping food scraps into mixed black-bag landfill trash",
        "swap_to": "Airtight bokashi fermentation bucket or indoor vermiculture worm bin",
        "description": (
            "Organic food scraps dumped into oxygen-deprived landfills decompose into methane gas, a super-pollutant with 28 times the climate "
            "warming potential of CO2. Bokashi fermentation rapidly pickles food scraps with beneficial microbes without foul odors, creating "
            "valuable soil pre-compost and concentrated liquid plant fertilizer."
        ),
        "co2_savings": "0.62 tonnes CO2e / year",
        "health_impact": "Eliminates decomposing waste odors, kitchen fruit flies, and indoor bacterial biofilm proliferation.",
        "cost_impact": "Supplies free liquid bio-fertilizer and compost, eliminating recurring purchases of commercial plant nutrients.",
    },

    # Energy (2 items)
    {
        "category": "energy",
        "emoji": "☀️",
        "title": "Rooftop Solar PV Array & Battery Storage",
        "swap_from": "Fossil fuel grid power and neighborhood diesel backup generators",
        "swap_to": "Rooftop solar photovoltaic panels with lithium-iron-phosphate battery",
        "description": (
            "Distributed rooftop solar captures clean solar energy directly at the point of consumption with zero transmission losses. "
            "Pairing solar with battery storage replaces dirty, noisy diesel generators during power outages and displaces grid power generated "
            "from coal and gas-fired thermal plants."
        ),
        "co2_savings": "4.1 tonnes CO2e / year",
        "health_impact": "Directly eliminates neighborhood diesel exhaust soot and regional coal-fired sulfur and nitrogen emissions.",
        "cost_impact": "Yields free electricity after a 4-6 year payback period, saving $1,200-$1,800 on annual electricity bills.",
    },
    {
        "category": "energy",
        "emoji": "💡",
        "title": "Smart Smart-Plug Outlets & LED Lighting Retrofit",
        "swap_from": "Incandescent/halogen bulbs and idle phantom standby appliance draw",
        "swap_to": "Smart scheduling power strips and high-CRI energy-saving LED lighting",
        "description": (
            "Phantom energy loads from dormant electronics, gaming consoles, and obsolete transformers consume up to 10% of household "
            "electricity. Smart power strips automatically cut parasitic standby power, while modern LED fixtures use 85% less energy "
            "and generate almost zero waste heat."
        ),
        "co2_savings": "0.40 tonnes CO2e / year",
        "health_impact": "Generates virtually zero waste heat, keeping living spaces cooler and mitigating urban indoor heat stress.",
        "cost_impact": "Lowers monthly electric utility bills by 10-15%, saving $140-$220 annually with rapid payback.",
    },
]

# ==============================================================================
# 6. COMMUNITY INITIATIVES (4 Grassroots Initiatives)
# ==============================================================================

COMMUNITY_INITIATIVES: List[Dict[str, str]] = [
    {
        "emoji": "📡",
        "title": "Hyperlocal Citizen Air Monitoring Network",
        "description": (
            "Establish a decentralized neighborhood grid of affordable laser PM2.5 and NO2 sensors mounted on school roofs, "
            "balconies, and community centers. Real-time open-source data streams empower residents to identify hyper-localized "
            "pollution hotspots, detect illegal trash burning, and make informed decisions on school sports and outdoor activities."
        ),
    },
    {
        "emoji": "🌳",
        "title": "Miyawaki Urban Pocket Forests & Green Barriers",
        "description": (
            "Transform underutilized vacant urban plots, schoolyards, and roadside shoulders into dense, multi-layered native botanical "
            "micro-forests using the renowned Miyawaki methodology. These miniature ecosystems grow ten times faster, absorb thirty times "
            "more particulate dust and NO2, and act as living sound and smog buffers between highways and homes."
        ),
    },
    {
        "emoji": "🚲",
        "title": "Open Streets Car-Free Sundays & Ciclovía Corridors",
        "description": (
            "Organize weekly or monthly community car-free days that temporarily repurpose major residential boulevards into protected "
            "avenues for pedestrians, cyclists, rollerbladers, and open-air markets. By temporarily halting motor vehicle traffic, "
            "ambient street-level PM2.5 and nitrogen dioxide drop by over 60%, fostering community wellness and active transit habits."
        ),
    },
    {
        "emoji": "🌾",
        "title": "Agricultural Biomass Pelleting & Stubble Upcycling Cooperative",
        "description": (
            "Partner with regional agricultural collectives to collect seasonal crop residue and rice stubble, converting farm waste "
            "into compressed biofuel pellets and biodegradable bio-composites instead of open-field burning. This prevents catastrophic "
            "seasonal regional smog inversions while providing farmers with new revenue streams and clean organic fertilizer."
        ),
    },
]

# ==============================================================================
# 7. PLEDGES (5 High-Impact Commitments)
# ==============================================================================

PLEDGES: List[Dict[str, str]] = [
    {
        "emoji": "🚶",
        "title": "The 3-Mile Active Mobility Pledge",
        "description": (
            "Commit to walking, cycling, or using an electric micro-mobility vehicle for all personal trips and errands under three miles "
            "instead of starting a combustion car engine. Short vehicle trips operate on cold engines with inefficient catalytic converters, "
            "emitting up to three times more pollutants per mile than long highway drives."
        ),
        "impact": "Prevents approximately 350 kg of CO2e and 1.8 kg of toxic tailpipe particulates per household annually.",
    },
    {
        "emoji": "🏡",
        "title": "Clean Air Sanctuary Pledge",
        "description": (
            "Pledge to keep all home living and sleeping spaces completely free of indoor combustion sources by eliminating incense sticks, "
            "synthetic room sprays, paraffin candles, and indoor smoking. Commit to maintaining an indoor PM2.5 level under 12 µg/m³ "
            "year-round through disciplined HEPA filtration and conscious ventilation."
        ),
        "impact": "Lowers family particulate exposure by 75% and dramatically reduces chronic morning nasal congestion and allergy symptoms.",
    },
    {
        "emoji": "🚫",
        "title": "Zero Waste Burning Pledge",
        "description": (
            "Vow to never burn dry leaves, plastic waste, garden clippings, or municipal garbage under any circumstances, and report open "
            "fires to local clean air authorities. Actively promote composting, leaf mulching, and proper three-stream waste recycling "
            "within your housing society or neighborhood block."
        ),
        "impact": "Eliminates toxic dioxin, black carbon, and carbon monoxide releases that trigger acute community asthma emergencies.",
    },
    {
        "emoji": "✨",
        "title": "Smokeless & Green Festive Celebration Pledge",
        "description": (
            "Celebrate national festivals, weddings, and holidays using vibrant light projections, eco-friendly LED displays, natural flower "
            "decorations, and musical gatherings rather than chemical fireworks and firecrackers. Protect vulnerable seniors, infants, and pets "
            "from deafening sound blasts and catastrophic peak air toxicity."
        ),
        "impact": "Prevents hazardous PM2.5 surges exceeding 800 µg/m³ during festive nights, keeping neighborhood air breathable.",
    },
    {
        "emoji": "⚡",
        "title": "Induction First & Energy Efficiency Pledge",
        "description": (
            "Transition household cooking from open flame gas burners to clean electric magnetic induction, and replace obsolete "
            "incandescent lamps with energy-efficient LED bulbs. Ensure heating and cooling appliances are maintained with clean filters "
            "to optimize thermal efficiency and reduce demand on fossil-fuel power grids."
        ),
        "impact": "Reduces household direct fossil emissions by up to 1.5 tonnes CO2e annually while eliminating indoor toxic NO2 accumulation.",
    },
]

# ==============================================================================
# 8. ROUTINE TEMPLATES (7 Personas x 8-10 Activities each)
# ==============================================================================

ROUTINE_TEMPLATES: Dict[str, List[Dict[str, Any]]] = {
    "family": [
        {
            "time": "06:30 AM",
            "title": "Morning Ambient AQI Check & Window Protocol",
            "description": "Review local air quality forecast on BreatheEasy before deciding whether to open windows or keep home sealed.",
            "emission_level": "low",
            "tags": ["morning", "indoor", "routine", "air-check"],
        },
        {
            "time": "07:15 AM",
            "title": "Electric Induction Family Breakfast",
            "description": "Prepare wholesome oatmeal and scrambled eggs using magnetic induction cooktop with kitchen exhaust running on low.",
            "emission_level": "low",
            "tags": ["cooking", "breakfast", "clean-energy", "family"],
        },
        {
            "time": "08:00 AM",
            "title": "Active School Commute & Drop-off",
            "description": "Walk children to local school or ride cargo e-bike along designated pedestrian greenway rather than driving.",
            "emission_level": "low",
            "tags": ["commute", "active-mobility", "school", "kids"],
        },
        {
            "time": "10:30 AM",
            "title": "Living Room HEPA Flush & Damp Dusting",
            "description": "Wipe common living room surfaces with damp microfiber cloth and run HEPA purifier to capture morning dust.",
            "emission_level": "low",
            "tags": ["cleaning", "hepa", "maintenance", "indoor"],
        },
        {
            "time": "12:30 PM",
            "title": "Steamed Whole-Food Lunch",
            "description": "Steam vegetables, brown rice, and legumes in sealed electric pressure cooker to prevent oil aerosol dispersion.",
            "emission_level": "low",
            "tags": ["cooking", "healthy-eating", "low-emission"],
        },
        {
            "time": "03:30 PM",
            "title": "Indoor Creative Play & Botanical Care",
            "description": "Engage kids in indoor creative crafts while watering and wiping leaves of indoor air-purifying house plants.",
            "emission_level": "low",
            "tags": ["indoor", "kids", "plants", "play"],
        },
        {
            "time": "05:30 PM",
            "title": "Neighborhood Park Play in Low-Smog Window",
            "description": "Head to neighborhood park for outdoor sports during the late afternoon window when traffic exhaust has temporarily eased.",
            "emission_level": "medium",
            "tags": ["outdoor", "exercise", "kids", "family"],
        },
        {
            "time": "07:00 PM",
            "title": "Dinner Preparation with Sealed Exhaust Hood",
            "description": "Cook family dinner on back induction burners with high-efficiency range hood actively venting cooking vapors.",
            "emission_level": "low",
            "tags": ["cooking", "dinner", "ventilation"],
        },
        {
            "time": "08:30 PM",
            "title": "Storytime & Bedroom Seal Check",
            "description": "Read bedtime books with children in sealed bedroom sanctuary with HEPA filtration quietly running on low.",
            "emission_level": "low",
            "tags": ["bedtime", "indoor", "kids", "wellness"],
        },
        {
            "time": "09:45 PM",
            "title": "Night Mode Purification & Rest",
            "description": "Switch bedroom air purifiers to ultra-quiet night mode and ensure window draft-blockers are firmly secured.",
            "emission_level": "low",
            "tags": ["sleep", "rest", "air-quality", "night"],
        },
    ],

    "elderly": [
        {
            "time": "06:00 AM",
            "title": "Indoor Gentle Yoga & Diaphragmatic Breathing",
            "description": "Perform gentle stretching and deep breathing exercises inside a clean, HEPA-purified living room.",
            "emission_level": "low",
            "tags": ["wellness", "indoor", "respiratory", "morning"],
        },
        {
            "time": "07:30 AM",
            "title": "Warm Herbal Tea & Health Check",
            "description": "Drink warm herbal tea and check morning AQI metrics before planning daily movements.",
            "emission_level": "low",
            "tags": ["morning", "hydration", "health", "air-check"],
        },
        {
            "time": "09:30 AM",
            "title": "Mid-Morning Garden Stroll",
            "description": "Enjoy a gentle stroll through community gardens after morning ground temperature inversions have fully lifted.",
            "emission_level": "low",
            "tags": ["outdoor", "walking", "nature", "sunlight"],
        },
        {
            "time": "11:30 AM",
            "title": "Reading in Clean-Air Living Sanctuary",
            "description": "Relax with books or crossword puzzles in comfortable living room with humidity balanced between 40% and 50%.",
            "emission_level": "low",
            "tags": ["indoor", "relaxation", "mental-health"],
        },
        {
            "time": "01:00 PM",
            "title": "Nutritious Steamed Lunch & Hydration",
            "description": "Eat a nutrient-dense lunch of warm steamed soup, lentils, and vegetables prepared on induction cooktop.",
            "emission_level": "low",
            "tags": ["cooking", "lunch", "nutrition", "healthy"],
        },
        {
            "time": "02:30 PM",
            "title": "Afternoon Rest in Climate-Controlled Bedroom",
            "description": "Take an afternoon nap in bedroom protected by sealed windows and continuous whisper-quiet air filtration.",
            "emission_level": "low",
            "tags": ["rest", "sleep", "bedroom", "air-purifier"],
        },
        {
            "time": "04:30 PM",
            "title": "Balcony Container Gardening & Plant Misting",
            "description": "Tend to potted lavender, mint, and spider plants on protected veranda, lightly misting foliage.",
            "emission_level": "low",
            "tags": ["gardening", "plants", "nature", "hobby"],
        },
        {
            "time": "06:30 PM",
            "title": "Light Early Dinner with Family",
            "description": "Share an early dinner cooked without heavy frying or synthetic seasonings to ensure easy digestion.",
            "emission_level": "low",
            "tags": ["dinner", "family", "healthy-eating"],
        },
        {
            "time": "08:00 PM",
            "title": "Family Video Call & Daily Monitor Review",
            "description": "Connect with distant grandchildren over video and check indoor air monitor readings before bed.",
            "emission_level": "low",
            "tags": ["family", "social", "air-monitor"],
        },
        {
            "time": "09:30 PM",
            "title": "Ultrasonic Humidifier Check & Deep Sleep",
            "description": "Ensure bedroom humidifier is filled with clean distilled water to keep airways hydrated throughout the night.",
            "emission_level": "low",
            "tags": ["sleep", "hydration", "bedroom", "wellness"],
        },
    ],

    "commuter": [
        {
            "time": "06:45 AM",
            "title": "Wake-up & Real-Time Route AQI Scan",
            "description": "Check BreatheEasy map to pick the transit route with the lowest particulate exposure and traffic congestion.",
            "emission_level": "low",
            "tags": ["morning", "planning", "commute", "air-check"],
        },
        {
            "time": "07:30 AM",
            "title": "Clean Transit Departure with N95 Mask",
            "description": "Depart for work using electric metro or commuter rail, wearing a comfortable N95 respirator through station hubs.",
            "emission_level": "medium",
            "tags": ["commute", "transit", "mask", "public-transport"],
        },
        {
            "time": "09:00 AM",
            "title": "Office Arrival & Personal Desk HEPA Power-On",
            "description": "Settle into workstation, turn on desktop personal HEPA purifier, and inspect workstation airflow.",
            "emission_level": "low",
            "tags": ["work", "office", "hepa", "desk"],
        },
        {
            "time": "11:30 AM",
            "title": "Indoor Stairwell Walk & Hydration",
            "description": "Take an active walking break up indoor office stairs away from street traffic exhausts; drink fresh water.",
            "emission_level": "low",
            "tags": ["activity", "health", "hydration", "work"],
        },
        {
            "time": "01:00 PM",
            "title": "Clean-Air Cafeteria Dining",
            "description": "Eat lunch in indoor cafeteria or green atrium rather than eating at roadside street stands near heavy traffic.",
            "emission_level": "low",
            "tags": ["lunch", "nutrition", "clean-air"],
        },
        {
            "time": "03:30 PM",
            "title": "CO2 Dilution & Team Collaboration Sprint",
            "description": "Open office meeting room doors to dilute exhaled CO2, maintaining sharp cognitive focus and decision speed.",
            "emission_level": "low",
            "tags": ["office", "productivity", "co2", "ventilation"],
        },
        {
            "time": "05:45 PM",
            "title": "Return Commute via Active Electric Transit",
            "description": "Take metro or electric bike home, avoiding peak highway gridlock and intense diesel exhaust lanes.",
            "emission_level": "medium",
            "tags": ["commute", "transit", "electric", "evening"],
        },
        {
            "time": "07:15 PM",
            "title": "Entry Decontamination & Face Saline Rinse",
            "description": "Remove outdoor shoes at entryway, wash face and hands, and use saline spray to clear road dust from nostrils.",
            "emission_level": "low",
            "tags": ["hygiene", "home", "decontamination", "wellness"],
        },
        {
            "time": "08:30 PM",
            "title": "Low-Emission Induction Dinner & Unwind",
            "description": "Cook quick induction stir-fry with splatter guard and relax in filtered living room.",
            "emission_level": "low",
            "tags": ["dinner", "cooking", "relaxation"],
        },
        {
            "time": "10:30 PM",
            "title": "Night Mode Purification Setup",
            "description": "Power on bedroom purifier in sleep whisper mode and set overnight digital air alert notifications.",
            "emission_level": "low",
            "tags": ["sleep", "air-purifier", "night", "rest"],
        },
    ],

    "outdoor-worker": [
        {
            "time": "05:30 AM",
            "title": "Pre-Shift Prep & Respirator Fit Check",
            "description": "Inspect silicone face seal on reusable elastomeric half-mask or N95 respirator before heading to worksite.",
            "emission_level": "low",
            "tags": ["safety", "ppe", "morning", "preparation"],
        },
        {
            "time": "06:30 AM",
            "title": "Early Commute to Construction / Worksite",
            "description": "Travel to site during early morning before intense solar ultraviolet radiation converts exhaust into ozone.",
            "emission_level": "medium",
            "tags": ["commute", "transit", "worksite"],
        },
        {
            "time": "07:30 AM",
            "title": "Morning Work Shift with Wind Awareness",
            "description": "Position heavy machinery, cutting equipment, and mixing stations downwind from active crew working positions.",
            "emission_level": "high",
            "tags": ["work", "safety", "dust-control", "outdoors"],
        },
        {
            "time": "10:00 AM",
            "title": "Respirator Cleanse & Hydration Break",
            "description": "Take mandatory rest break in enclosed vehicle cabin; wipe face and replace saturated dust pre-filters.",
            "emission_level": "medium",
            "tags": ["break", "hydration", "ppe", "safety"],
        },
        {
            "time": "12:30 PM",
            "title": "Lunch in Air-Filtered Shelter or Vehicle",
            "description": "Dine inside air-conditioned break trailer with active recirculated HEPA filtration to give lungs complete respite.",
            "emission_level": "low",
            "tags": ["lunch", "shelter", "clean-air", "rest"],
        },
        {
            "time": "02:00 PM",
            "title": "Afternoon Work with Dust Suppression Misting",
            "description": "Operate pressurized water misting hoses during concrete cutting and earthmoving to knock down airborne silica.",
            "emission_level": "high",
            "tags": ["work", "suppression", "silica", "dust"],
        },
        {
            "time": "04:30 PM",
            "title": "Worksite Tool De-Dusting & Mask Packdown",
            "description": "Use HEPA-shrouded vacuum attachments rather than compressed air blowers to clean tools and clothes.",
            "emission_level": "medium",
            "tags": ["cleaning", "dust-control", "safety"],
        },
        {
            "time": "05:30 PM",
            "title": "Commute Home with Protective Gear Stored",
            "description": "Travel home after sealing dusty work overalls in a heavy canvas gear bag to protect family living spaces.",
            "emission_level": "medium",
            "tags": ["commute", "safety", "transit"],
        },
        {
            "time": "06:45 PM",
            "title": "Full Shower & Nasal Irrigation",
            "description": "Take thorough warm shower and perform saline sinus rinse to clear all inhaled dust particles and soot.",
            "emission_level": "low",
            "tags": ["hygiene", "recovery", "health"],
        },
        {
            "time": "08:30 PM",
            "title": "Deep Rest in Clean Air Sanctuary",
            "description": "Rest muscles and lungs in sealed bedroom maintained at under 5 µg/m³ PM2.5 by a high-capacity air purifier.",
            "emission_level": "low",
            "tags": ["recovery", "sleep", "bedroom", "air-quality"],
        },
    ],

    "student": [
        {
            "time": "07:00 AM",
            "title": "Wake-up & Campus Air Advisory Review",
            "description": "Check campus air advisory and plan bike route or electric campus shuttle options.",
            "emission_level": "low",
            "tags": ["morning", "study", "campus", "air-check"],
        },
        {
            "time": "07:45 AM",
            "title": "Active Bicycle Commute to Campus",
            "description": "Ride commuter bicycle along dedicated campus bike trail avoiding main bus terminal traffic.",
            "emission_level": "low",
            "tags": ["commute", "bicycle", "active", "student"],
        },
        {
            "time": "08:30 AM",
            "title": "Morning Lecture in Filtered Auditorium",
            "description": "Attend morning lectures in university hall equipped with central MERV 13 HVAC mechanical filtration.",
            "emission_level": "low",
            "tags": ["study", "lecture", "indoor", "education"],
        },
        {
            "time": "11:00 AM",
            "title": "Library Deep Study Session",
            "description": "Study in the quiet library atrium with clean air, excellent natural lighting, and low indoor CO2.",
            "emission_level": "low",
            "tags": ["study", "library", "focus", "indoor"],
        },
        {
            "time": "12:45 PM",
            "title": "Plant-Based Cafeteria Lunch",
            "description": "Enjoy a fresh plant-based meal with friends at the sustainable university student cooperative diner.",
            "emission_level": "low",
            "tags": ["lunch", "nutrition", "sustainable", "social"],
        },
        {
            "time": "02:30 PM",
            "title": "Laboratory Class with Fume Hood Safety",
            "description": "Conduct chemical and biology experiments strictly inside calibrated exhaust fume hoods with sash lowered.",
            "emission_level": "medium",
            "tags": ["lab", "safety", "fume-hood", "science"],
        },
        {
            "time": "04:30 PM",
            "title": "Indoor Intramural Gym Sports",
            "description": "Play basketball or badminton in the air-filtered campus sports complex instead of outdoor asphalt courts.",
            "emission_level": "low",
            "tags": ["sports", "fitness", "indoor", "health"],
        },
        {
            "time": "06:30 PM",
            "title": "Electric Bus Ride Home",
            "description": "Take campus electric transit shuttle back to apartment before evening smog inversion thickens.",
            "emission_level": "medium",
            "tags": ["commute", "transit", "electric-bus"],
        },
        {
            "time": "08:00 PM",
            "title": "Dorm Assignment Sprint with Desk Purifier",
            "description": "Work on assignments at desk with compact HEPA filter running, keeping mind alert and head clear.",
            "emission_level": "low",
            "tags": ["study", "dorm", "productivity", "hepa"],
        },
        {
            "time": "11:00 PM",
            "title": "Bedroom Sanctuary Wind-Down & Sleep",
            "description": "Turn off blue-light devices, set purifier to whisper mode, and enjoy clean-air restorative sleep.",
            "emission_level": "low",
            "tags": ["sleep", "rest", "wellness", "night"],
        },
    ],

    "wfh": [
        {
            "time": "07:30 AM",
            "title": "Morning Sunlight & 10-Minute Balcony Air Check",
            "description": "Check BreatheEasy AQI, step onto balcony for morning sunlight, and determine daily ventilation schedule.",
            "emission_level": "low",
            "tags": ["morning", "sunlight", "routine", "air-check"],
        },
        {
            "time": "08:15 AM",
            "title": "Fresh French-Press Coffee & Desk Plant Inspection",
            "description": "Brew morning coffee using electric kettle and dust the foliage of office ZZ plants and Snake plants.",
            "emission_level": "low",
            "tags": ["coffee", "morning", "plants", "wfh"],
        },
        {
            "time": "09:00 AM",
            "title": "Remote Standup & Ergonomic Office Setup",
            "description": "Join morning video standup in dedicated home office with desktop True HEPA purifier actively filtering breathing zone.",
            "emission_level": "low",
            "tags": ["work", "remote", "standup", "hepa"],
        },
        {
            "time": "11:00 AM",
            "title": "CO2 Flush & Posture Reset",
            "description": "Open interior door and crack window for 5 minutes to flush accumulated carbon dioxide down below 750 ppm.",
            "emission_level": "low",
            "tags": ["ventilation", "co2", "ergonomics", "health"],
        },
        {
            "time": "12:30 PM",
            "title": "Fast Clean Induction Cooking",
            "description": "Cook fresh warm lunch on magnetic induction cooktop with exhaust fan running on medium power.",
            "emission_level": "low",
            "tags": ["cooking", "lunch", "induction", "clean-energy"],
        },
        {
            "time": "02:00 PM",
            "title": "Deep Focus Work Sprint with Low Noise",
            "description": "Tackle complex coding or writing tasks in an acoustically quiet, clean-air room with ambient PM2.5 under 5 µg/m³.",
            "emission_level": "low",
            "tags": ["focus", "productivity", "deep-work"],
        },
        {
            "time": "04:15 PM",
            "title": "Screen Break & Botanical Care",
            "description": "Step away from monitors, do gentle eye exercises, and inspect indoor plant soil moisture levels.",
            "emission_level": "low",
            "tags": ["break", "plants", "eye-health", "wellness"],
        },
        {
            "time": "06:00 PM",
            "title": "Neighborhood Sunset Walk if AQI Permits",
            "description": "Take a 30-minute brisk neighborhood walk if local AQI is under 75; otherwise do an indoor yoga flow.",
            "emission_level": "low",
            "tags": ["walking", "outdoor", "exercise", "sunset"],
        },
        {
            "time": "07:30 PM",
            "title": "Low-Impact Dinner & Kitchen Degrease",
            "description": "Prepare light dinner and wipe kitchen surfaces with natural vinegar and citrus oil spray.",
            "emission_level": "low",
            "tags": ["dinner", "cleaning", "natural", "home"],
        },
        {
            "time": "10:00 PM",
            "title": "Night Ventilation Lockdown & Whisper HEPA Run",
            "description": "Ensure exterior windows are closed against nighttime smog accumulation and set purifier to sleep mode.",
            "emission_level": "low",
            "tags": ["sleep", "bedroom", "hepa", "night"],
        },
    ],

    "athlete": [
        {
            "time": "05:30 AM",
            "title": "Pre-Dawn Ambient Air Quality & Particulate Scan",
            "description": "Check real-time PM2.5 and temperature inversion forecasts to decide between outdoor road run or smart trainer ride.",
            "emission_level": "low",
            "tags": ["morning", "training", "air-check", "fitness"],
        },
        {
            "time": "06:00 AM",
            "title": "Clean Cardio Workout (Indoor Smart Trainer or Clean Trail)",
            "description": "Complete targeted threshold cardio session either on indoor smart bike trainer or outdoor forested trail route.",
            "emission_level": "medium",
            "tags": ["workout", "cardio", "training", "cycling"],
        },
        {
            "time": "07:45 AM",
            "title": "Post-Workout Saline Nasal Cleanse & High-Protein Breakfast",
            "description": "Rinse airways with sterile saline mist and consume high-antioxidant berry and plant-protein recovery smoothie.",
            "emission_level": "low",
            "tags": ["recovery", "nutrition", "respiratory", "smoothie"],
        },
        {
            "time": "09:30 AM",
            "title": "Foam Rolling & Mobility in Purified Room",
            "description": "Spend 30 minutes on myofascial release and joint mobility in a climate-controlled room with pristine air.",
            "emission_level": "low",
            "tags": ["mobility", "recovery", "stretching", "clean-air"],
        },
        {
            "time": "12:30 PM",
            "title": "Nutrient-Dense Induction Whole-Food Lunch",
            "description": "Cook quinoa, steamed wild salmon, and leafy greens on induction stove to restore glycogen without cooking fumes.",
            "emission_level": "low",
            "tags": ["lunch", "nutrition", "athlete", "healthy"],
        },
        {
            "time": "02:30 PM",
            "title": "Active Recovery & Mental Visualization",
            "description": "Recline in oxygen-rich bedroom for 45 minutes of mental rehearsal and diaphragmatic parasympathetic breathing.",
            "emission_level": "low",
            "tags": ["mental-training", "breathing", "recovery"],
        },
        {
            "time": "05:00 PM",
            "title": "Indoor Strength & Conditioning Session",
            "description": "Lift weights in dedicated home gym or filtered fitness center with commercial True HEPA circulation running.",
            "emission_level": "low",
            "tags": ["strength", "gym", "weights", "workout"],
        },
        {
            "time": "07:00 PM",
            "title": "Anti-Inflammatory Dinner with Steamed Greens",
            "description": "Enjoy an antioxidant-rich anti-inflammatory dinner cooked with turmeric, ginger, and steamed cruciferous vegetables.",
            "emission_level": "low",
            "tags": ["dinner", "nutrition", "anti-inflammatory"],
        },
        {
            "time": "08:30 PM",
            "title": "Diaphragmatic Breathwork & Lung Expansion",
            "description": "Practice pranayama and deep lung expansion exercises in filtered room with optimal 45% ambient humidity.",
            "emission_level": "low",
            "tags": ["breathwork", "lungs", "wellness", "meditation"],
        },
        {
            "time": "10:00 PM",
            "title": "Cool, HEPA-Purified Athletic Sleep Sanctuary",
            "description": "Sleep in 18°C bedroom with True HEPA purifier maintaining PM2.5 below 2 µg/m³ for maximal tissue repair.",
            "emission_level": "low",
            "tags": ["sleep", "tissue-repair", "recovery", "night"],
        },
    ],
}

# ==============================================================================
# 9. IMPACT FACTORS (Normalized Personal Emission Coefficients)
# ==============================================================================

IMPACT_FACTORS: Dict[str, Dict[str, float]] = {
    "commute": {
        "car-solo": 6.5,
        "car-pool": 2.5,
        "public": 1.2,
        "cycle": 0.0,
        "ev": 0.5,
        "wfh": 0.0,
    },
    "cooking": {
        "lpg": 1.8,
        "electric": 0.8,
        "biomass": 4.5,
        "kerosene": 3.2,
    },
    "heating": {
        "gas-heater": 3.5,
        "electric-heater": 2.0,
        "heat-pump": 0.8,
        "wood-fire": 5.0,
        "none": 0.0,
    },
    "waste": {
        "mixed": 2.5,
        "segregated": 1.0,
        "composted": 0.5,
        "minimal": 0.2,
    },
    "cleaning": {
        "chemical": 0.8,
        "reduced": 0.4,
        "natural": 0.1,
    },
    "festival": {
        "heavy-crackers": 8.0,
        "green-crackers": 2.0,
        "no-crackers": 0.0,
    },
}

# ==============================================================================
# 10. HELPER UTILITIES (Clean Access Functions)
# ==============================================================================

def get_city_aqi(city: str) -> Optional[Dict[str, Any]]:
    """
    Look up AQI data for a given city name. Normalizes case and spaces/underscores.
    """
    normalized_key = city.strip().lower().replace(" ", "_").replace("-", "_")
    return CITY_AQI_DATA.get(normalized_key)


def list_cities() -> List[str]:
    """
    Return sorted list of available city keys.
    """
    return sorted(list(CITY_AQI_DATA.keys()))


def get_room_tips(room: str) -> List[Dict[str, str]]:
    """
    Retrieve tips for a specific room type ('living', 'bedroom', 'kitchen', 'kids', 'office').
    """
    normalized_room = room.strip().lower()
    return ROOM_TIPS.get(normalized_room, [])


def get_routine_by_persona(persona: str) -> List[Dict[str, Any]]:
    """
    Retrieve routine template for a specific demographic persona.
    """
    normalized_persona = persona.strip().lower().replace("_", "-")
    return ROUTINE_TEMPLATES.get(normalized_persona, [])


def calculate_daily_carbon_score(selections: Dict[str, str]) -> Dict[str, Any]:
    """
    Calculate estimated personal emission impact score based on daily lifestyle selections.
    Takes a dictionary mapping categories ('commute', 'cooking', 'heating', 'waste', 'cleaning', 'festival')
    to user-selected option keys.
    """
    total_score = 0.0
    breakdown = {}

    for category, factor_map in IMPACT_FACTORS.items():
        chosen_option = selections.get(category, "")
        value = factor_map.get(chosen_option, 0.0)
        breakdown[category] = value
        total_score += value

    rating = "Low Impact"
    if total_score > 15.0:
        rating = "Critical High Impact"
    elif total_score > 8.0:
        rating = "Moderate Impact"

    return {
        "total_score": round(total_score, 2),
        "rating": rating,
        "breakdown": breakdown,
    }
