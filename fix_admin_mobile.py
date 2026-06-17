import os
import glob

css_to_add = """
        @media (max-width: 768px) {
            .sidebar { transform: translateX(-100%); z-index: 1000; transition: transform 0.3s; }
            .sidebar.show { transform: translateX(0); }
            .main-content { margin-left: 0; padding: 1rem; }
            .mobile-menu-btn { display: inline-block; background: none; border: none; font-size: 1.5rem; color: var(--secondary); margin-right: 15px; }
            .topbar { flex-direction: row; align-items: center; justify-content: flex-start; }
            .topbar > div:last-child { margin-left: auto; }
            .topbar h2, .topbar h4 { font-size: 1.2rem; }
            .sidebar-overlay { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 999; }
            .sidebar-overlay.show { display: block; }
        }
        @media (min-width: 769px) {
            .mobile-menu-btn { display: none; }
            .sidebar-overlay { display: none; }
        }
    </style>
"""

overlay_html = """<body>
    <!-- Sidebar Overlay -->
    <div class="sidebar-overlay" onclick="document.querySelector('.sidebar').classList.remove('show'); this.classList.remove('show');"></div>
"""

menu_btn_html = """        <div class="topbar">
            <div class="d-flex align-items-center">
                <button class="mobile-menu-btn" onclick="document.querySelector('.sidebar').classList.toggle('show'); document.querySelector('.sidebar-overlay').classList.toggle('show');">
                    <i class="fas fa-bars"></i>
                </button>"""

templates = glob.glob('cars/templates/cars/admin/*.html')

for t in templates:
    if 'dashboard.html' in t:
        continue # Already done
    with open(t, 'r') as f:
        content = f.read()
    
    if 'mobile-menu-btn' not in content:
        # Add CSS
        content = content.replace('    </style>', css_to_add)
        # Add overlay
        content = content.replace('<body>', overlay_html)
        # Add menu button - handling different topbar structures
        if '<div class="topbar">\n            <div>' in content:
            content = content.replace('<div class="topbar">\n            <div>', menu_btn_html + '\n                <div>')
        elif '<div class="topbar">\n        <a' in content:
            content = content.replace('<div class="topbar">\n        <a', menu_btn_html + '\n        <a')
            content = content.replace('<!-- Spacer -->\n    </div>', '<!-- Spacer -->\n            </div>\n    </div>')
            
        with open(t, 'w') as f:
            f.write(content)
        print(f"Fixed {t}")
