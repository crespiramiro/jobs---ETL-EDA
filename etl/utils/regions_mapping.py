import re

region_map = {
    "Latam": ["latam", "latin america", "argentina", "mexico", "colombia", "brazil", "costa rica", "uruguay", "peru", "chile"],
    "North America": ["usa", "united states", "canada", "northern america"],
    "Europe": ["europe", "uk", "germany", "france", "ireland", "spain", "italy", "portugal", "netherlands", "romania", "sweden", "poland", "croatia", "bulgaria", "austria", "czech republic", "finland", "greece", "hungary", "switzerland", "denmark", "belgium", "estonia", "ukraine"],
    "Asia": ["india", "china", "philippines", "vietnam", "bangladesh", "indonesia", "japan", "israel", "georgia", "taiwan"],
    "Oceania": ["australia", "new zealand", "papua new guinea"],
    "Africa": ["south africa", "kenya", "nigeria", "uganda", "ghana", "algeria", "egypt"],
}


def map_region(raw_region: str) -> str:
    if not isinstance(raw_region, str):
        return "Other"

    raw = raw_region.lower().strip()
    
    # Si menciona "remote", "global" o hay más de una región separada por coma → Remote
    if "remote" in raw or "global" in raw or "," in raw:
        return "Remote"

    for region, keywords in region_map.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", raw):
                return region

    return "Other"
