"""Line icons (24×24, stroke = currentColor), drawn for this site.

One per region, one per package type, one per experience kind and style, plus UI icons.
Render with {% icon "everest" %} or {% icon "heli" "icon--lg" %}.
"""

ICONS = {
    # ---- regions
    "pagoda":  # Kathmandu: three-roof Newar pagoda temple on a plinth
        '<path d="M12 2.5v2"/><path d="M8.5 8L12 4.5 15.5 8z"/><path d="M9.5 8v1.5h5V8"/>'
        '<path d="M6.5 12.5L9 9.5h6l2.5 3z"/><path d="M8.5 12.5v2h7v-2"/><path d="M4.5 17.5l3-3h9l3 3z"/>'
        '<path d="M7 17.5V21h10v-3.5"/><path d="M11 21v-2h2v2"/><path d="M3 21h18"/>',
    "paraglider":  # Pokhara: canopy, lines and pilot over the lake
        '<path d="M3 7.5c3-3.8 15-3.8 18 0"/><path d="M3 7.5c3-1.6 15-1.6 18 0"/>'
        '<path d="M4 7.8l7.2 7.6M20 7.8l-7.2 7.6M9 6.6l2.4 8.6M15 6.6l-2.4 8.6"/><circle cx="12" cy="16.6" r="1.3"/>'
        '<path d="M2 21c2-.8 4-.8 6 0s4 .8 6 0 4-.8 6 0"/>',
    "rhododendron":  # Annapurna: five-petal rhododendron with leaves
        '<circle cx="12" cy="5.4" r="2.2"/><circle cx="15.5" cy="8" r="2.2"/><circle cx="14.2" cy="12" r="2.2"/>'
        '<circle cx="9.8" cy="12" r="2.2"/><circle cx="8.5" cy="8" r="2.2"/><circle cx="12" cy="9" r=".7"/>'
        '<path d="M12 14.2V21"/><path d="M12 18.2c-2.5-.2-4.5-1.5-5.5-3.5 2.5 0 4.5 1.2 5.5 3.5zM12 17.2c2.3-.3 4-1.6 5-3.5-2.3.1-4.2 1.3-5 3.5z"/>',
    "chorten":  # Mustang: chorten with stepped base, dome and spire
        '<path d="M4 21h16"/><path d="M6 21v-2.5h12V21"/><path d="M7.5 18.5V16h9v2.5"/><path d="M8.5 16a3.5 3.5 0 0 1 7 0"/>'
        '<path d="M10.3 12.5h3.4"/><path d="M11 12.5l1-6 1 6"/><path d="M11.3 10.5h1.4M11.6 8.5h.8"/><path d="M12 6.5V4.5"/>'
        '<path d="M12 4.5c.8-.6 1.6-.6 2.3 0"/>',
    "summit":  # Everest: pyramid peak, snow line and summit flag
        '<path d="M2 20l7.5-12L12 11l2.5-4L22 20z"/><path d="M7.3 11.6l1.7 1.2 1.5-1.2 1.4 1.2M13.3 9.2l1.2 1 1.4-1"/>'
        '<path d="M14.5 7V3l3 1.1-3 1.1"/>',
    "lake":  # Langtang: peaks over a holy lake
        '<path d="M3 13l5-7 3 4 2.5-3L21 13"/><path d="M3 13h18"/><path d="M6 16h12M8 18.5h8M10 21h4"/>',
    "flags":  # Manaslu: prayer flags strung over a ridge
        '<path d="M3 21V5M21 21V5"/><path d="M3 5c6 3 12 3 18 0"/>'
        '<path d="M6 6.4v3l1.7-1 1.7 1V7.3M10.9 7.4v3l1.5-.9 1.5.9V7.4M15.9 7.2v3l1.6-.9 1.6.8V6.5"/><path d="M6 21l6-7 6 7"/>',
    "rhino":  # Chitwan: one-horned rhinoceros
        '<path d="M3 16.5c0-3.6 2.6-6.5 6.6-6.5h4.9c1.6 0 2.7.6 3.4 1.6l1.6-2.7.6 3.3c.6.7.9 1.6.9 2.8v1h-2.4"/>'
        '<path d="M5.2 16.5v3.2h2.4v-2.5M14.6 17.3v2.4H17v-3"/><path d="M17.6 13.4h.01"/><path d="M9.6 10V8.6M11.4 10V9"/>'
        '<path d="M3 16.5l-.8.9"/>',
    "lotus":  # Lumbini: lotus in bloom
        '<path d="M12 18c-2.5-2-3.5-4.5-3.5-7.5 1.5.7 2.8 1.9 3.5 3.5.7-1.6 2-2.8 3.5-3.5 0 3-1 5.5-3.5 7.5z"/>'
        '<path d="M12 14c-1.2-2.4-1.2-5 0-8 1.2 3 1.2 5.6 0 8z"/>'
        '<path d="M8.6 12.5C6.5 12 4.5 12.5 3 14c1.5 2.5 5 4 9 4M15.4 12.5c2.1-.5 4.1 0 5.6 1.5-1.5 2.5-5 4-9 4"/><path d="M5 21h14"/>',
    "tea":  # East Nepal: tea leaves and bud
        '<path d="M12 21c-.5-5.5 1.5-10 7-13.5.5 6.5-2 11-7 13.5z"/><path d="M12 21c-4-1.5-7-5-7-10.5 4 1.5 6.5 4.5 7 10.5z"/>'
        '<path d="M12 21c.3-3 1.5-6 4-8.5M12 21c-1-2.5-2.5-5-5-7"/><path d="M12.5 7c-.8-1.6-.6-3 .5-4 1 1.2.9 2.6-.5 4z"/>',
    "boat":  # Far West: boat on Rara with junipers
        '<path d="M3.5 15h13l-2.3 3H6z"/><path d="M8 15l3.5-3.5"/><path d="M2 21c2-.8 4-.8 6 0s4 .8 6 0 4-.8 6 0"/>'
        '<path d="M17.5 12l2-6.5 2 6.5zM19.5 12v2.5"/><path d="M13.5 10l1.5-4.2 1.5 4.2zM15 10v1.5"/>',
    "kailash":  # Kailash: the domed peak with its snow bands and south-face gully
        '<path d="M3 19c2-1 3-5 5-8 1.3-2 2.6-4.5 4-4.5s2.7 2.5 4 4.5c2 3 3 7 5 8"/>'
        '<path d="M9.2 10h5.6M8.2 12.5h7.6M12 6.5V15"/><path d="M2 21c4-1.6 16-1.6 20 0"/>',
    # ---- package types
    "heli":  # helicopter
        '<path d="M4 4.5h16M12 4.5V7"/><path d="M8.5 7H15a5 5 0 0 1 5 5v1.5h-8.5a3 3 0 0 1-3-3z"/><path d="M15 7v3.5h5"/>'
        '<path d="M8.5 10H3M3 8v4"/><path d="M9 18h11.5M11.5 13.5V18M17 13.5V18"/>',
    "boot":  # trekking boot
        '<path d="M6 3h5v6l6.5 3.5c1.5.8 2.5 2 2.5 3.5v1H4V5a2 2 0 0 1 2-2z"/><path d="M4 17v2.5h16V17"/>'
        '<path d="M11 9H8M11 12H8.5M14.5 11.2l-1.3 1.8"/>',
    "bell":  # temple bell
        '<path d="M12 3v2.5"/><path d="M7 16c0-6 1.5-10 5-10s5 4 5 10"/><path d="M5 16h14v2H5z"/><path d="M12 18v2"/>'
        '<circle cx="12" cy="21" r=".8"/>',
    "axe":  # ice axe
        '<path d="M5 21L16 7"/><path d="M9.5 6.5c3-2.2 7.2-2.8 11.5-1.3-3.2.4-5.7 1.4-7.4 3.4"/><path d="M15.8 7.2l-3.6-3.6"/>',
    # ---- styles
    "family": '<circle cx="7" cy="5" r="2"/><circle cx="16.5" cy="5" r="2"/><circle cx="12" cy="11.5" r="1.5"/>'
              '<path d="M4 21v-8a3 3 0 0 1 6 0M13.5 13a3 3 0 0 1 6 0v8"/><path d="M10.5 21v-4a1.5 1.5 0 0 1 3 0v4"/><path d="M4 21h16"/>',
    "heart": '<path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.4 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10z"/>',
    "crown": '<path d="M3 8l4 4 5-7 5 7 4-4-2 10H5z"/><path d="M5 21h14"/>',
    "coin": '<circle cx="12" cy="12" r="9"/><path d="M8.5 8h7M8.5 11h7M9.5 8c3.3 0 3.3 6-.6 6l5 4"/>',
    "yoga": '<circle cx="12" cy="4.8" r="2"/><path d="M12 7.8v6"/><path d="M6 10.8l6 2 6-2"/>'
            '<path d="M5 19c2-2 4.5-3 7-3s5 1 7 3"/><path d="M8 19.8h8"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "road": '<path d="M8 3L4 21M16 3l4 18"/><path d="M12 4v3M12 10v3M12 16v4"/>',
    "camera": '<path d="M3 8h4l2-3h6l2 3h4v12H3z"/><circle cx="12" cy="13.5" r="3.5"/>',
    "lamp":  # diyo, for festivals
        '<path d="M4 14c0 3 3.5 5 8 5s8-2 8-5z"/><path d="M20 14c1 0 2-.5 2-1.5"/>'
        '<path d="M12 11c-1.2-1.4-1.2-3 0-5 1.2 2 1.2 3.6 0 5z"/><path d="M12 11v3"/>',
    # ---- experience kinds
    "culture": '<path d="M12 2.5v2"/><path d="M7.5 8L12 4.5 16.5 8z"/><path d="M5 13l3-5h8l3 5z"/>'
               '<path d="M7 13v8M17 13v8M10 21v-4h4v4"/><path d="M3 21h18"/>',
    "spiritual":  # prayer wheel
        '<rect x="7.5" y="6" width="9" height="10" rx="1.5"/><path d="M7.5 9h9M7.5 13h9"/><path d="M12 3v3M12 16v5"/>'
        '<path d="M16.5 7.5l2.5-1.5"/><circle cx="19.6" cy="5.6" r=".9"/>',
    "nature": '<path d="M2 20l7-11 4 6 3-4 6 9z"/><circle cx="17.5" cy="5.5" r="2"/>',
    "wildlife": '<path d="M3 16.5c0-3.6 2.6-6.5 6.6-6.5h4.9c1.6 0 2.7.6 3.4 1.6l1.6-2.7.6 3.3c.6.7.9 1.6.9 2.8v1h-2.4"/>'
                '<path d="M5.2 16.5v3.2h2.4v-2.5M14.6 17.3v2.4H17v-3"/><path d="M17.6 13.4h.01"/>',
    "adventure": '<path d="M3 7.5c3-3.8 15-3.8 18 0"/><path d="M3 7.5c3-1.6 15-1.6 18 0"/>'
                 '<path d="M4 7.8l7.2 7.6M20 7.8l-7.2 7.6"/><circle cx="12" cy="16.6" r="1.3"/><path d="M8 21l4-3 4 3"/>',
    "aerial": '<path d="M4 4.5h16M12 4.5V7"/><path d="M8.5 7H15a5 5 0 0 1 5 5v1.5h-8.5a3 3 0 0 1-3-3z"/>'
              '<path d="M8.5 10H3M3 8v4"/><path d="M9 18h11.5M11.5 13.5V18M17 13.5V18"/>',
    "hiking": '<circle cx="13" cy="4" r="1.8"/><path d="M12.6 7l-2.1 6 3 3 1 5M10.5 13l-2.5 8"/><path d="M12 8.5l3 3 2.5-1"/>'
              '<path d="M18 9l-1 12"/>',
    "food":  # momo
        '<path d="M4 15c0-4 3.6-7 8-7s8 3 8 7c-2 1.5-5 2-8 2s-6-.5-8-2z"/><path d="M8 9.5l1 3M12 8v3.5M16 9.5l-1 3"/>'
        '<path d="M12 6.3c.6-.8.6-1.7 0-2.5"/><path d="M3 19.5h18"/>',
    "water": '<path d="M3.5 15h13l-2.3 3H6z"/><path d="M8 15l3.5-3.5"/><path d="M2 21c2-.8 4-.8 6 0s4 .8 6 0 4-.8 6 0"/>'
             '<circle cx="18" cy="6" r="2.5"/>',
    "wellness": '<path d="M12 20c-3-2.5-4.5-5.5-4.5-9 1.8.8 3.3 2.3 4.5 4.5 1.2-2.2 2.7-3.7 4.5-4.5 0 3.5-1.5 6.5-4.5 9z"/>'
                '<path d="M12 15.5c-2-3-2-6 0-9 2 3 2 6 0 9z"/><path d="M4 20h16"/>',
    # ---- UI
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chevron": '<path d="M9 6l6 6-6 6"/>',
    "chevron-down": '<path d="M6 9l6 6 6-6"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "altitude": '<path d="M3 20l6-9 3 4 3-5 6 10z"/><path d="M18 3v5.5M15.6 5.4L18 3l2.4 2.4"/>',
    "users": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 5a3 3 0 0 1 0 6M18 14c2 .7 3 2.8 3 6"/>',
    "bed": '<path d="M3 18V6M3 14h18v4M21 14v-2a3 3 0 0 0-3-3h-7v5"/><circle cx="7" cy="11" r="2"/>',
    "plane": '<path d="M2.5 13.5l6.5-1 4-7.5h2.2l-2 7.2 5.3-.7 1.7-2.3h1.6l-.8 3.8.8 3.8h-1.6l-1.7-2.3-5.3-.7 2 7.2H13l-4-7.5-6.5-1z"/>',
    "car": '<path d="M4 16v-4.5L6.5 6h11l2.5 5.5V16z"/><path d="M4 11.5h16"/><circle cx="7.5" cy="16.5" r="1.8"/><circle cx="16.5" cy="16.5" r="1.8"/>',
    "meal": '<path d="M7 3v7a2 2 0 0 0 2 2v9M5 3v5M9 3v5"/><path d="M17 21V3c-2 1.5-3 4.2-3 7.2h3"/>',
    "whatsapp": '<path d="M3.5 20.5l1.3-4A8.5 8.5 0 1 1 8 19.5z"/><path d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.5-2-1-1 .8a4 4 0 0 1-2.3-2.3l.8-1-1-2z"/>',
    "phone": '<path d="M21 16.4v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 1.1 3.7 2 2 0 0 1 3.1 1.5h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L7 9.3a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.9 2.1z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h10"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "pin": '<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    "ticket": '<path d="M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v2a2.5 2.5 0 0 0 0 5v2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-2a2.5 2.5 0 0 0 0-5z"/>'
              '<path d="M14.5 5v2M14.5 10.5v2M14.5 16v2"/>',
    "filter": '<path d="M4 5h16l-6 7.5V19l-4 1.5v-8z"/>',
    "grade": '<path d="M5 20v-4M10 20v-8M15 20v-12M20 20V4"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 10h8M8 13h5"/>',
    "book": '<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/>',
    "route": '<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18h6a3 3 0 0 0 0-6h-4a3 3 0 0 1 0-6h6"/>',
    "map": '<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 16l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/>',
    "stamp": '<path d="M9 3h6v5l3 3v3H6v-3l3-3z"/><path d="M4 18h16v3H4z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "snow": '<path d="M12 2v20M3.3 7l17.4 10M3.3 17L20.7 7"/><path d="M9.5 3.5L12 5l2.5-1.5M9.5 20.5L12 19l2.5 1.5"/>',
    "rain": '<path d="M7 15a4.5 4.5 0 0 1-.5-9 6 6 0 0 1 11.3 1.6A3.8 3.8 0 0 1 17 15z"/><path d="M8 18l-1 3M12 18l-1 3M16 18l-1 3"/>',
    "permit": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h4"/><circle cx="16" cy="16" r="1.6"/>',
    "download": '<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>',
    "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
}


def svg(name, cls=""):
    body = ICONS.get(name) or ICONS["sparkle"]
    return (f'<svg class="icon {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')
