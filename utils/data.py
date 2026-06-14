def get_village_data(village_name: str) -> dict:
    villages = {
        "Rampur Village": {
            "metrics": {
                "population": 4500, "pop_growth": 120,
                "dev_score": 62, "budget": "50.00 Lakh",
                "priority_areas": 3,
            },
            "agents": {
                "Water":          {"icon": "💧", "score": 45, "issues": ["Water scarcity", "No piped supply", "Contamination risk"], "recommendations": ["Install borewells", "Water purification plant", "Rainwater harvesting", "Jal Jeevan Mission application"]},
                "Agriculture":    {"icon": "🌾", "score": 62, "issues": ["Low yield", "No cold storage", "Market access"], "recommendations": ["Soil health cards", "Drip irrigation", "FPO formation", "PM-KISAN enrollment"]},
                "Healthcare":     {"icon": "❤️", "score": 38, "issues": ["No PHC nearby", "High infant mortality", "No ambulance"], "recommendations": ["Mobile health unit", "ASHA worker training", "Ayushman Bharat enrollment", "Telemedicine setup"]},
                "Education":      {"icon": "🎓", "score": 58, "issues": ["High dropout rate", "No digital lab", "Teacher shortage"], "recommendations": ["Digital classroom", "Mid-day meal improvement", "Scholarship schemes", "Teacher recruitment"]},
                "Employment":     {"icon": "💼", "score": 41, "issues": ["High unemployment", "No skill center", "Youth migration"], "recommendations": ["PMKVY skill center", "SHG formation", "MGNREGS projects", "Startup incubation"]},
                "Infrastructure": {"icon": "🏗️", "score": 67, "issues": ["Road conditions", "No street lights", "Drainage issues"], "recommendations": ["PMGSY road upgrade", "Solar street lights", "Drainage construction", "Community hall"]},
                "Environment":    {"icon": "🌳", "score": 67, "issues": ["Deforestation", "Waste management", "Air quality"], "recommendations": ["Plantation drive", "Solid waste mgmt", "Solar energy", "Biogas plants"]},
            },
            "budget_allocation": {
                "Water Resources": 20.00,
                "Healthcare": 12.00,
                "Education": 8.00,
                "Agriculture": 6.00,
                "Employment": 2.50,
                "Infrastructure": 1.50,
            },
            "phases": [
                {"name": "Phase 1", "duration": "0 - 12 Months", "budget": "18.50 Lakh", "items": ["Water Conservation", "Primary Healthcare Center", "School Infrastructure", "Skill Development Program"]},
                {"name": "Phase 2", "duration": "12 - 24 Months", "budget": "16.00 Lakh", "items": ["Irrigation Enhancement", "Digital Education Center", "Rural Road Improvement", "Women Self Help Groups"]},
                {"name": "Phase 3", "duration": "24 - 36 Months", "budget": "15.50 Lakh", "items": ["Agricultural Processing Unit", "Community Health Programs", "Renewable Energy Projects", "Tourism & Handicrafts"]},
            ],
            "priorities": [
                {"name": "Water Scarcity", "impact": "High Impact"},
                {"name": "Healthcare Access", "impact": "High Impact"},
                {"name": "Unemployment", "impact": "Medium Impact"},
                {"name": "Education Quality", "impact": "Medium Impact"},
                {"name": "Road Connectivity", "impact": "High Impact"},
            ],
        },
        "Sundarpur Village": {
            "metrics": {"population": 3200, "pop_growth": 85, "dev_score": 71, "budget": "35.00 Lakh", "priority_areas": 2},
            "agents": {
                "Water":          {"icon": "💧", "score": 72, "issues": ["Seasonal shortage"], "recommendations": ["Rainwater harvesting", "Check dam construction"]},
                "Agriculture":    {"icon": "🌾", "score": 78, "issues": ["Market linkage"], "recommendations": ["E-NAM registration", "FPO support"]},
                "Healthcare":     {"icon": "❤️", "score": 65, "issues": ["Specialist shortage"], "recommendations": ["Telemedicine", "Ayushman enrollment"]},
                "Education":      {"icon": "🎓", "score": 70, "issues": ["Higher education access"], "recommendations": ["Scholarship programs", "Digital labs"]},
                "Employment":     {"icon": "💼", "score": 60, "issues": ["Skill gaps"], "recommendations": ["PMKVY center", "Agri-business training"]},
                "Infrastructure": {"icon": "🏗️", "score": 75, "issues": ["Last mile connectivity"], "recommendations": ["Bridge construction", "Optical fiber"]},
                "Environment":    {"icon": "🌳", "score": 80, "issues": ["Waste management"], "recommendations": ["Composting", "Solar power"]},
            },
            "budget_allocation": {"Water Resources": 10.00, "Healthcare": 8.00, "Education": 7.00, "Agriculture": 5.00, "Employment": 3.00, "Infrastructure": 2.00},
            "phases": [
                {"name": "Phase 1", "duration": "0 - 12 Months", "budget": "12.00 Lakh", "items": ["Check dam", "Health camp", "Digital school", "Market linkage"]},
                {"name": "Phase 2", "duration": "12 - 24 Months", "budget": "12.00 Lakh", "items": ["FPO formation", "Telemedicine", "Bridge repair", "SHG training"]},
                {"name": "Phase 3", "duration": "24 - 36 Months", "budget": "11.00 Lakh", "items": ["Solar plant", "Cold storage", "Tourism", "Skill center"]},
            ],
            "priorities": [
                {"name": "Market Linkage", "impact": "High Impact"},
                {"name": "Skill Development", "impact": "Medium Impact"},
                {"name": "Last Mile Roads", "impact": "High Impact"},
            ],
        },
        "Krishnapur Village": {
            "metrics": {"population": 6800, "pop_growth": 200, "dev_score": 48, "budget": "75.00 Lakh", "priority_areas": 5},
            "agents": {
                "Water":          {"icon": "💧", "score": 32, "issues": ["Acute shortage", "Contamination", "No infrastructure"], "recommendations": ["Emergency borewells", "Jal Jeevan Mission", "Water ATMs"]},
                "Agriculture":    {"icon": "🌾", "score": 45, "issues": ["Drought prone", "No irrigation", "Pest damage"], "recommendations": ["Drip irrigation", "Crop insurance", "Soil testing"]},
                "Healthcare":     {"icon": "❤️", "score": 28, "issues": ["No facility", "High MMR", "Malnutrition"], "recommendations": ["PHC setup", "NHM programs", "Nutrition camps"]},
                "Education":      {"icon": "🎓", "score": 42, "issues": ["Low literacy", "No school building", "Child labor"], "recommendations": ["School construction", "Mid-day meal", "Awareness camps"]},
                "Employment":     {"icon": "💼", "score": 35, "issues": ["90% unemployed", "No skills", "Bonded labor"], "recommendations": ["MGNREGS", "Skill mission", "SHG formation"]},
                "Infrastructure": {"icon": "🏗️", "score": 55, "issues": ["No proper roads", "No electricity"], "recommendations": ["PMGSY", "DDUGJY electrification"]},
                "Environment":    {"icon": "🌳", "score": 60, "issues": ["Deforestation"], "recommendations": ["Van Mahotsav", "MNREGS plantation"]},
            },
            "budget_allocation": {"Water Resources": 25.00, "Healthcare": 18.00, "Education": 12.00, "Agriculture": 10.00, "Employment": 6.00, "Infrastructure": 4.00},
            "phases": [
                {"name": "Phase 1", "duration": "0 - 12 Months", "budget": "30.00 Lakh", "items": ["Emergency water supply", "Mobile health unit", "School repair", "MGNREGS jobs"]},
                {"name": "Phase 2", "duration": "12 - 24 Months", "budget": "25.00 Lakh", "items": ["PHC construction", "Irrigation canal", "New school building", "Skill training center"]},
                {"name": "Phase 3", "duration": "24 - 36 Months", "budget": "20.00 Lakh", "items": ["Solar power plant", "Cold storage", "Market yard", "Women empowerment"]},
            ],
            "priorities": [
                {"name": "Water Emergency", "impact": "High Impact"},
                {"name": "Healthcare Setup", "impact": "High Impact"},
                {"name": "Employment Crisis", "impact": "High Impact"},
                {"name": "Education Gap", "impact": "High Impact"},
                {"name": "Road Access", "impact": "Medium Impact"},
            ],
        },
    }
    return villages.get(village_name, villages["Rampur Village"])


SCHEMES = [
    {"name": "Jal Jeevan Mission", "amount": "12.00 Lakh"},
    {"name": "PMKSY – Irrigation", "amount": "8.50 Lakh"},
    {"name": "Ayushman Bharat", "amount": "5.00 Lakh"},
    {"name": "PM Gram Sadak Yojana", "amount": "7.20 Lakh"},
    {"name": "PMKVY Skill Dev.", "amount": "3.80 Lakh"},
    {"name": "PM Awas Yojana", "amount": "6.40 Lakh"},
    {"name": "MGNREGS", "amount": "9.00 Lakh"},
    {"name": "Digital India BharatNet", "amount": "4.50 Lakh"},
    {"name": "PM-KISAN", "amount": "2.00 Lakh/yr"},
    {"name": "Swachh Bharat Mission", "amount": "3.20 Lakh"},
]
