"""Policy pages. DRAFTS for legal review: every [BRACKETED] value must be confirmed before launch.

Each policy: title, nav label, summary (plain-English box at the top), sections [(heading, [paragraph | {"list": [...]}])].
"""
from collections import OrderedDict

UPDATED = "[DATE OF LEGAL REVIEW]"

POLICIES = OrderedDict()

POLICIES["refund-and-cancellation"] = {
    "title": "Refund and cancellation policy",
    "nav": "Refunds and cancellations",
    "summary": "If you cancel, what you get back depends on how many days before departure you tell us in writing and on what airlines, helicopter operators, hotels and permit offices refund to us. We pass on every refund we receive, minus the charges below, within [10] working days of receiving it.",
    "sections": [
        ("How to cancel", [
            "Email us at the address on your booking confirmation. Your cancellation takes effect on the day we receive it. A WhatsApp message is welcome, but please follow it with an email so we both have a written record.",
            "If some members of a group cancel, we recalculate the price for those still travelling, because rooms, vehicles, guides and helicopter charters are priced per party.",
        ]),
        ("Our cancellation scale", [
            "These charges are a percentage of the total package price and apply unless a supplier's own terms are stricter (see below).",
            {"list": [
                "[45] days or more before departure: we keep the deposit of [20]%.",
                "[44–21] days before departure: [40]% of the total price.",
                "[20–8] days before departure: [70]% of the total price.",
                "[7] days or fewer, or no-show: [100]% of the total price.",
            ]},
        ]),
        ("Services with stricter terms", [
            "Some services are non-refundable once issued, and your quote names them before you book: restricted area permits (Upper Mustang, Manaslu, Tsum, Kanchenjunga, Dolpo, Humla), Chinese group visas and Tibet permits for Kailash and Lhasa, peak climbing permits, domestic flight tickets on non-refundable fares and festival-period hotel rooms. Where a supplier refunds nothing, we cannot refund that part.",
        ]),
        ("Weather, flights and helicopters", [
            "Mountain flights and helicopter tours depend on weather. If a scheduled helicopter tour cannot fly because of weather and we cannot reschedule it within your stay, we refund the flight cost in full. If a flight to Lukla, Jomsom or Simikot is cancelled, we rebook the next available flight; extra hotel nights, meals or a charter helicopter that you choose to take are paid by you, and travel insurance usually covers them. See the helicopter and altitude terms for detail.",
        ]),
        ("If we change or cancel", [
            "If we cancel your package for any reason other than events outside our control, we refund everything you have paid us.",
            "If a significant part of the package changes before departure (for example a lower hotel category), we offer a comparable alternative, a price adjustment or a full refund of the affected part.",
        ]),
        ("Events outside anyone's control", [
            "Landslides, floods, road and border closures, strikes (bandh), government restrictions, park closures and similar events can change a route. We reroute you as close to the original plan as we can and pass on any refund or credit suppliers give us. We recommend insurance that covers cancellation and curtailment for these reasons.",
        ]),
        ("Unused services", [
            "If you leave a trek early, skip a sightseeing day or choose not to use a booked service, we cannot refund it, because we have already paid for it. If you leave a trek because of illness or injury, we help you claim the unused part from your insurer.",
        ]),
        ("Refunds", [
            "Refunds go back to the account you paid from, in the currency you paid, within [10] working days of us receiving the money from suppliers. Bank charges and exchange differences are not refundable. [Confirm whether card gateway fees are refunded.]",
        ]),
        ("Changing dates instead", [
            "Moving your dates is often cheaper than cancelling. Changes requested more than [30] days before departure carry no fee from us; suppliers may charge for theirs. We confirm every change in writing.",
        ]),
    ],
}

POLICIES["booking-terms"] = {
    "title": "Booking terms and conditions",
    "nav": "Booking terms",
    "summary": "Prices on this site are indicative. Your written quote is the offer; a booking is confirmed when we receive your deposit and send written confirmation. Travel insurance with medical evacuation cover is a condition of booking any trek, heli tour, climb or Kailash yatra.",
    "sections": [
        ("Who we are", [
            "Best Nepal Tour Package is a trading name of [LEGAL NAME], registered at [REGISTERED ADDRESS], Nepal, company registration [NO.], PAN/VAT [NO.], Department of Tourism / Nepal Tourism Board registration [NO.], [TAAN / NATTA MEMBERSHIP IF HELD].",
        ]),
        ("Prices and quotes", [
            "Prices on the website are indicative 'from' prices per person, twin sharing, shown in Indian rupees and US dollars. They are not offers. Your written quote lists the services, hotels, flights, permits, dates and total price including applicable taxes. A quote is valid for [7] days unless it says otherwise and remains subject to availability until booked.",
        ]),
        ("Booking and payment", [
            "To book, accept the quote in writing and pay the deposit of [20]% of the total price. We then confirm each service in writing. The balance is due [30] days before departure; bookings made later are paid in full. Kailash yatras and restricted area treks need passport copies and full payment earlier, as your quote will say.",
        ]),
        ("Your responsibilities", [
            "You must carry valid identity documents (Indian citizens: passport or voter ID card; other nationalities: passport valid six months and a Nepal visa), the permits we tell you about, and insurance covering medical evacuation by helicopter up to the highest altitude on your route. Tell us about health conditions, pregnancy, mobility needs and diets when you book. Our guides may stop you going higher if they judge your health is at risk; their decision is final.",
        ]),
        ("Our responsibilities", [
            "We plan and book your package with care and use suppliers we know. Airlines, helicopter operators, hotels, parks and permit offices provide services under their own terms. If something goes wrong on the ground, tell your guide or our office straight away so we can fix it while you are still there.",
        ]),
        ("Changes, cancellations and refunds", ["See our refund and cancellation policy and our helicopter and altitude terms, which form part of these terms."]),
        ("Complaints", [
            "If something is not right, tell us during the trip. If it is not resolved, write to [COMPLAINTS EMAIL] within [30] days of your return and we will reply within [14] days.",
        ]),
        ("Law", ["These terms are governed by the laws of Nepal. Courts in Kathmandu have jurisdiction. [Confirm with your lawyer, including consumer protection rules for clients in India.]"]),
    ],
}

POLICIES["payments"] = {
    "title": "Payments policy",
    "nav": "Payments",
    "summary": "We take a [20]% deposit to confirm a booking and the balance [30] days before departure. You can pay by [bank transfer in NPR, INR or USD, UPI to our Indian account, or card]. We never ask for card details, OTPs or passwords by email, WhatsApp or phone.",
    "sections": [
        ("When you pay", [
            {"list": [
                "Deposit: [20]% of the total price, to confirm your booking.",
                "Balance: due [30] days before departure.",
                "Late bookings (within [30] days of departure): full payment at booking.",
                "Helicopter charters, Kailash permits and peak permits may need early payment; your quote will say so.",
            ]},
        ]),
        ("How you can pay", [
            "[Confirm accepted methods.] From Nepal: bank transfer or [FONEPAY/ESEWA]. From India: [UPI / NEFT to our Indian collection account] or international transfer in INR. Overseas: SWIFT transfer in USD or cards through [PAYMENT GATEWAY]. Card payments may carry a gateway fee of [X]%, shown before you pay. Cash balance in Kathmandu is accepted in [NPR/USD] on arrival where agreed.",
        ]),
        ("Taxes", ["Quotes include Nepal VAT and service charges where they apply, shown on your invoice. [Confirm the treatment of Indian TCS and GST for clients booking from India with your accountant.]"]),
        ("Keeping payments safe", [
            "Our bank details are only ever sent on a signed PDF invoice from [ACCOUNTS EMAIL]. If you receive bank details from any other address, or a message asking you to pay a different account, call us on [PHONE] before paying.",
        ]),
    ],
}

POLICIES["helicopter-and-altitude"] = {
    "title": "Helicopter, flight and altitude terms",
    "nav": "Heli and altitude terms",
    "summary": "Helicopter tours fly in the morning and only when the pilot judges it safe. At high landings the helicopter carries fewer passengers, so groups may shuttle. Time on the ground above 5,000 m is short, usually 10 to 15 minutes. Anyone with heart or lung conditions, or who is pregnant, should not fly to high altitude without a doctor's clearance.",
    "sections": [
        ("Weather and timing", [
            "Mountain weather is clearest early in the day; clouds often build by late morning. Flights leave at the time the operator sets, usually between 6 and 7 a.m., and the pilot may delay, reroute or cancel for safety. The pilot's decision is final.",
        ]),
        ("Payload and seating", [
            "Helicopters used in Nepal usually carry up to five passengers at lower altitudes. At high landings such as Kala Patthar or Annapurna Base Camp the safe load falls, so the operator may land passengers in two groups or drop some at a lower point while others go up. Weight limits apply; tell us each passenger's weight when booking.",
        ]),
        ("Shared seats and charters", [
            "On a shared-seat tour you fly with other passengers on fixed departures. On a private charter you have the whole helicopter, and the price is per helicopter, not per person.",
        ]),
        ("Weather cancellations", [
            "If weather stops a booked helicopter tour and we cannot reschedule within your stay, we refund the flight in full. If weather forces a shortened route (for example no landing at the highest point), the operator's partial refund, if any, is passed on to you.",
        ]),
        ("Altitude", [
            "Above about 2,500 m some people feel altitude sickness. On treks we build in acclimatisation days; on helicopter tours you go high fast but stay briefly. Tell us about heart, lung or blood pressure conditions, pregnancy or recent surgery. Our guides carry a first-aid kit and pulse oximeter on treks and can arrange evacuation, which your insurance should cover.",
        ]),
        ("Evacuation", [
            "If you need a rescue helicopter on a trek, we call it immediately. The operator bills your insurer or you directly; costs can be several thousand US dollars. Insurance with helicopter evacuation cover to your highest altitude is a condition of booking.",
        ]),
    ],
}

POLICIES["privacy"] = {
    "title": "Privacy policy",
    "nav": "Privacy",
    "summary": "We collect the details you give us to quote, book and run your trip, and use them for nothing else. We share only what a hotel, airline, helicopter operator, permit office or guide needs to provide a booked service. We do not sell your data.",
    "sections": [
        ("What we collect", [
            "When you enquire: your name, phone, email and the trip you describe. When you book: passport or ID details, dates of birth and weights where airlines, helicopter operators or permit offices require them, health and diet notes you choose to share, and payment records. When you subscribe: your email address.",
        ]),
        ("How we use it", ["To reply to your enquiry, quote, book and run your trip, look after you while you travel, keep accounting records and, if you subscribed, send our monthly email. We do not build advertising profiles."]),
        ("Who we share it with", ["Only the suppliers providing a service you booked, permit offices, our accountants and payment providers. Kailash and Tibet bookings require sharing passport details with our partner agency in Tibet and Chinese authorities for permits."]),
        ("How long we keep it", ["Enquiries that do not lead to a booking: [24] months. Booking records: as long as Nepal tax law requires, currently [6] years. Newsletter: until you unsubscribe."]),
        ("Your rights", ["You can ask to see, correct or delete your personal data, or unsubscribe, by writing to [PRIVACY EMAIL]. We reply within [30] days. [Confirm obligations under Nepal's Individual Privacy Act, 2075 and, for Indian clients, India's Digital Personal Data Protection Act.]"]),
        ("This website", ["The site sets a security cookie for its forms and no advertising cookies. It loads fonts from Google Fonts, scripts from cdnjs and unpkg, and photographs from Wikimedia; those services see your IP address when your browser requests their files. Our maps are drawn on our own server, with no map service."]),
    ],
}

POLICIES["cookies"] = {
    "title": "Cookie policy",
    "nav": "Cookies",
    "summary": "This website uses one essential cookie to protect its forms. It uses no advertising or tracking cookies unless we add analytics, in which case this page will list them.",
    "sections": [
        ("Essential", ["csrftoken: set by our website software to protect forms from cross-site attacks. Expires after one year. Contains no personal data."]),
        ("Stored in your browser", ["Your currency choice (INR or USD), recently viewed packages and a dismissed planning prompt are remembered in your browser's storage. Nothing is sent to us."]),
        ("Analytics", ["[If you enable Google Analytics 4, list its cookies here (_ga, _ga_*) and add a consent banner before setting them.]"]),
    ],
}

POLICIES["disclaimer"] = {
    "title": "Disclaimer",
    "nav": "Disclaimer",
    "summary": "We keep this site accurate, but permits, fees, flight schedules, helicopter landing rules, Kailash rules, road conditions, festival dates and prices change, sometimes at short notice. Check current status before you travel; your written quote is what counts.",
    "sections": [
        ("Information on this site", ["Our guides, packages and place pages describe conditions as we understand them when written. They are for planning, not a guarantee. Altitudes are approximate, distances and drive times typical. Prices are indicative."]),
        ("Health and altitude", ["Notes on altitude and health are general information, not medical advice. See a doctor before any trek, heli tour, climb or Kailash yatra."]),
        ("Photographs", ["Photographs come from Wikimedia Commons under free licences and are credited to their authors. They show places as they were when photographed. See our photo credits page."]),
        ("Maps", ["Our maps are drawn from Natural Earth outlines (public domain) with international borders as shown on Nepal's official map. They show where places are and are not for navigation."]),
        ("Links", ["Links to hotels and other sites are for convenience. We are not responsible for their content."]),
    ],
}

POLICIES["accessibility"] = {
    "title": "Accessibility statement",
    "nav": "Accessibility",
    "summary": "We want this site to work for everyone, including people who use screen readers, keyboards or zoom. We aim for WCAG 2.2 level AA. If something does not work for you, tell us and we will fix it or send you the information another way.",
    "sections": [
        ("What we have done", [
            {"list": [
                "Text contrast of at least 4.5:1, with each region's colours tested.",
                "Every page works with a keyboard, with visible focus outlines.",
                "Photos have text alternatives; maps and elevation charts come with numbered lists and tables.",
                "Animations stop if your device asks for reduced motion.",
                "Pages and forms work without JavaScript; the trip tools need it.",
            ]},
        ]),
        ("Travelling with access needs", ["Many temples, durbar squares and trails have steps and uneven ground. Tell us about mobility, sight, hearing or other needs and we will check hotels, vehicles and sites before you book. Helicopter tours can suit travellers who cannot trek, subject to the operator's boarding rules."]),
        ("Contact", ["Write to [ACCESSIBILITY EMAIL] or call [PHONE]."]),
    ],
}
