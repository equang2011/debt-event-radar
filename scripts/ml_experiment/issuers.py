issuers = [
    # --- HEAVY DEBT FILERS (positives engine) ---
    {"name": "Ford Motor",              "cik": "37996"},    # large revolvers, term loans
    {"name": "AT&T",                    "cik": "732717"},   # massive debt issuance history
    {"name": "HCA Healthcare",          "cik": "860730"},   # very active: term loans, notes, amendments
    {"name": "Delta Air Lines",         "cik": "27904"},    # frequent filer; keep one airline
    # --- ENERGY (borrowing base revolvers — distinctive vocabulary) ---
    {"name": "Devon Energy",            "cik": "1090012"},  # borrowing base, RBL structures
    {"name": "Pioneer Natural Resources","cik": "1038357"}, # credit facility variety
    # --- REIT (mortgage + unsecured debt, different from corporate) ---
    {"name": "Simon Property Group",    "cik": "1063761"},
    # --- RETAIL (debt + good non-debt EX-10s) ---
    {"name": "Macys",                   "cik": "794367"},   # employment, vendor contracts as negatives
    # --- TECH (primarily NEGATIVES: equity plans, employment, licensing) ---
    {"name": "Salesforce",              "cik": "1108524"},  # rich source of non-debt EX-10s
    {"name": "Oracle",                  "cik": "1341439"},  # some debt + good non-debt mix
    # --- MID-CAP (drafting style diversity — big-cap boilerplate is too uniform) ---
    {"name": "Anywhere Real Estate",    "cik": "1398987"},
    # --- FINANCIAL ISSUER (different debt vocabulary than industrials) ---
    {"name": "CIT Group",               "cik": "1171825"},  # verify CIK carefully
]


UNSEEN_TEST_ISSUERS = [
    # --- TELECOM ---
    {"name": "Verizon", "cik": "732712"},

    # --- AIRLINES ---
    {"name": "United Airlines Holdings", "cik": "100517"},
    {"name": "American Airlines Group", "cik": "6201"},

    # --- TRAVEL / CRUISE ---
    {"name": "Carnival", "cik": "815097"},

    # --- RETAIL ---
    {"name": "Walmart", "cik": "104169"},

    # --- TECH / INDUSTRIAL ---
    {"name": "Intel", "cik": "50863"},

    # --- HOSPITALITY ---
    {"name": "Marriott International", "cik": "1048286"},

    # --- ENERGY ---
    {"name": "Occidental Petroleum", "cik": "797468"},
]