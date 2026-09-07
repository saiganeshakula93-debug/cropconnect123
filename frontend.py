# ==============================================================================
# CropConnect - Direct Farm-to-Buyer Marketplace & Smart Logistics Platform
# Thoughtfully Handcrafted UI with Modern Lucide React Iconography
# Currency: Indian Rupee (₹) | Real-time APMC Mandi Linkage | Consolidated 2-Opt Logistics
# ==============================================================================

FRONTEND_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CropConnect | Direct Farm-to-Buyer Marketplace &amp; Smart Agri Logistics</title>
  
  <!-- Google Fonts: Plus Jakarta Sans & Outfit -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- Bootstrap 5.3.2 CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  
  <!-- Lucide Icons (Standard Modern React Icon System) -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    :root {
      --primary: #15803d;
      --primary-dark: #14532d;
      --primary-light: #22c55e;
      --primary-surface: #f0fdf4;
      --primary-border: #bbf7d0;
      
      --accent-amber: #d97706;
      --accent-amber-light: #fef3c7;
      --accent-earth: #92400e;
      
      --bg-warm: #f8fafc;
      --bg-card: #ffffff;
      --text-main: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --border-subtle: #e2e8f0;
      --border-strong: #cbd5e1;
      
      --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.04);
      --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.06), 0 1px 2px -1px rgb(0 0 0 / 0.04);
      --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.08), 0 2px 4px -2px rgb(0 0 0 / 0.06);
      --shadow-hover: 0 14px 28px -4px rgba(21, 128, 61, 0.12), 0 6px 12px -2px rgba(21, 128, 61, 0.06);
      
      --radius-xs: 6px;
      --radius-sm: 10px;
      --radius-md: 16px;
      --radius-lg: 22px;
      --radius-full: 9999px;
    }

    *, *::before, *::after {
      box-sizing: border-box;
    }

    body {
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      background-color: var(--bg-warm);
      color: var(--text-main);
      -webkit-font-smoothing: antialiased;
      line-height: 1.5;
    }

    h1, h2, h3, h4, h5, h6, .brand-font {
      font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
      letter-spacing: -0.025em;
      color: var(--text-main);
    }

    /* Lucide React Icon Sizing & Sizing Utilities */
    .lucide, [data-lucide] {
      width: 1.15rem;
      height: 1.15rem;
      stroke-width: 1.9px;
      stroke: currentColor;
      display: inline-block;
      vertical-align: -0.16em;
      transition: stroke 0.15s ease;
    }
    .icon-xs { width: 0.92rem !important; height: 0.92rem !important; stroke-width: 2.1px !important; }
    .icon-sm { width: 1.05rem !important; height: 1.05rem !important; stroke-width: 2px !important; }
    .icon-md { width: 1.3rem !important; height: 1.3rem !important; stroke-width: 1.85px !important; }
    .icon-lg { width: 1.65rem !important; height: 1.65rem !important; stroke-width: 1.8px !important; }
    .icon-xl { width: 2.25rem !important; height: 2.25rem !important; stroke-width: 1.75px !important; }

    /* Top Navbar */
    .navbar-custom {
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0.75rem 0;
      transition: box-shadow 0.2s ease;
    }
    .brand-logo {
      font-weight: 800;
      font-size: 1.35rem;
      color: var(--primary-dark) !important;
      display: inline-flex;
      align-items: center;
      gap: 0.55rem;
      text-decoration: none;
    }
    .brand-logo .logo-icon {
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, #15803d 0%, #16a34a 100%);
      color: #ffffff;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 10px rgba(21, 128, 61, 0.25);
    }

    /* Live Mandi Benchmark Ticker */
    .mandi-ticker-bar {
      background: #0f2e1b;
      color: #e2f2e6;
      font-size: 0.78rem;
      padding: 0.45rem 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      overflow: hidden;
      white-space: nowrap;
    }
    .ticker-pill-label {
      background: #22c55e;
      color: #052e16;
      font-weight: 700;
      font-size: 0.7rem;
      letter-spacing: 0.03em;
      padding: 0.2rem 0.55rem;
      border-radius: var(--radius-full);
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      margin-right: 0.8rem;
    }
    .ticker-pulse-dot {
      width: 6px;
      height: 6px;
      background: #052e16;
      border-radius: 50%;
      animation: pulseGreen 1.8s infinite;
    }
    @keyframes pulseGreen {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.3; transform: scale(1.4); }
    }
    .ticker-scroll-content {
      display: inline-block;
      white-space: nowrap;
      animation: tickerScroll 38s linear infinite;
    }
    .ticker-scroll-content:hover {
      animation-play-state: paused;
    }
    @keyframes tickerScroll {
      0% { transform: translateX(0); }
      100% { transform: translateX(-50%); }
    }
    .ticker-item {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      margin-right: 1.8rem;
      color: #cbd5e1;
    }
    .ticker-item strong {
      color: #ffffff;
    }
    .ticker-up { color: #4ade80; font-weight: 600; }
    .ticker-down { color: #f87171; font-weight: 600; }

    /* Hero Section */
    .hero-container {
      background: linear-gradient(145deg, #14532d 0%, #166534 50%, #0f3d1f 100%);
      color: #ffffff;
      padding: 3.25rem 0 2.75rem;
      position: relative;
      overflow: hidden;
    }
    .hero-container::before {
      content: "";
      position: absolute;
      top: -40%;
      right: -8%;
      width: 550px;
      height: 550px;
      background: radial-gradient(circle, rgba(34, 197, 94, 0.18) 0%, rgba(255,255,255,0) 70%);
      border-radius: 50%;
      pointer-events: none;
    }
    .hero-container::after {
      content: "";
      position: absolute;
      bottom: -30%;
      left: -5%;
      width: 400px;
      height: 400px;
      background: radial-gradient(circle, rgba(217, 119, 6, 0.15) 0%, rgba(255,255,255,0) 70%);
      border-radius: 50%;
      pointer-events: none;
    }
    .badge-glass {
      background: rgba(255, 255, 255, 0.12);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.22);
      color: #ffffff;
      padding: 0.35rem 0.9rem;
      border-radius: var(--radius-full);
      font-size: 0.82rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
    }
    .sms-callout-pill {
      background: rgba(0, 0, 0, 0.32);
      border: 1px dashed rgba(255, 255, 255, 0.35);
      border-radius: var(--radius-full);
      padding: 0.35rem 1rem;
      font-size: 0.82rem;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      color: #e2e8f0;
    }

    /* Tabs Bar */
    .nav-tabs-wrapper {
      background: #ffffff;
      border-bottom: 1px solid var(--border-subtle);
      box-shadow: var(--shadow-xs);
    }
    .nav-tabs-custom .nav-link {
      color: var(--text-muted);
      font-weight: 600;
      font-size: 0.92rem;
      border: none;
      border-bottom: 3px solid transparent;
      padding: 0.85rem 1.25rem;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
    }
    .nav-tabs-custom .nav-link:hover {
      color: var(--primary);
      border-bottom-color: rgba(21, 128, 61, 0.3);
    }
    .nav-tabs-custom .nav-link.active {
      color: var(--primary-dark);
      border-bottom-color: var(--primary);
      background: transparent;
      font-weight: 700;
    }

    /* Category Filter Chips */
    .chip-filter {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.42rem 0.95rem;
      border-radius: var(--radius-full);
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      font-size: 0.83rem;
      font-weight: 600;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.18s ease;
      user-select: none;
    }
    .chip-filter:hover {
      border-color: var(--primary-light);
      color: var(--primary);
      background: var(--primary-surface);
      transform: translateY(-1px);
    }
    .chip-filter.active {
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
      box-shadow: 0 2px 8px rgba(21, 128, 61, 0.25);
    }
    .chip-filter.active .lucide {
      stroke: #ffffff;
    }

    /* Crop Card System */
    .crop-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
      display: flex;
      flex-direction: column;
      height: 100%;
      position: relative;
    }
    .crop-card:hover {
      transform: translateY(-4px);
      box-shadow: var(--shadow-hover);
      border-color: rgba(21, 128, 61, 0.35);
    }

    /* Visual Crop Badges with tailored color themes */
    .crop-avatar {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: transform 0.2s ease;
    }
    .crop-card:hover .crop-avatar {
      transform: scale(1.05);
    }
    .crop-avatar-rose   { background: #fff1f2; color: #e11d48; border: 1px solid #ffe4e6; }
    .crop-avatar-purple { background: #faf5ff; color: #9333ea; border: 1px solid #f3e8ff; }
    .crop-avatar-amber  { background: #fffbeb; color: #b45309; border: 1px solid #fef3c7; }
    .crop-avatar-red    { background: #fef2f2; color: #dc2626; border: 1px solid #fee2e2; }
    .crop-avatar-green  { background: #f0fdf4; color: #16a34a; border: 1px solid #dcfce7; }
    .crop-avatar-yellow { background: #fefce8; color: #ca8a04; border: 1px solid #fef9c3; }
    .crop-avatar-gold   { background: #fffbeb; color: #d97706; border: 1px solid #fef3c7; }
    .crop-avatar-emerald{ background: #ecfdf5; color: #059669; border: 1px solid #d1fae5; }
    .crop-avatar-default{ background: #f0fdf4; color: #15803d; border: 1px solid #dcfce7; }

    .price-display {
      font-family: 'Outfit', sans-serif;
      font-size: 1.6rem;
      font-weight: 800;
      color: var(--text-main);
      line-height: 1;
    }
    .price-unit {
      font-size: 0.82rem;
      color: var(--text-muted);
      font-weight: 600;
    }
    .savings-badge {
      background: var(--accent-amber-light);
      color: var(--accent-earth);
      font-weight: 700;
      font-size: 0.76rem;
      padding: 0.28rem 0.6rem;
      border-radius: var(--radius-xs);
      border: 1px solid rgba(217, 119, 6, 0.25);
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
    }

    /* Role Badges */
    .role-badge-farmer {
      background: #ecfdf5;
      color: #065f46;
      border: 1px solid #a7f3d0;
      font-weight: 600;
      font-size: 0.72rem;
      padding: 0.2rem 0.55rem;
      border-radius: var(--radius-full);
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
    }
    .role-badge-fpo {
      background: #f5f3ff;
      color: #5b21b6;
      border: 1px solid #ddd6fe;
      font-weight: 600;
      font-size: 0.72rem;
      padding: 0.2rem 0.55rem;
      border-radius: var(--radius-full);
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
    }

    /* Buttons */
    .btn-brand {
      background: var(--primary);
      color: #ffffff;
      font-weight: 600;
      border: none;
      border-radius: var(--radius-sm);
      padding: 0.55rem 1.15rem;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.45rem;
    }
    .btn-brand:hover {
      background: var(--primary-dark);
      color: #ffffff;
      box-shadow: 0 4px 12px rgba(21, 128, 61, 0.25);
      transform: translateY(-1px);
    }
    .btn-brand-outline {
      background: transparent;
      color: var(--primary);
      border: 1.5px solid var(--primary);
      font-weight: 600;
      border-radius: var(--radius-sm);
      padding: 0.5rem 1rem;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.45rem;
    }
    .btn-brand-outline:hover {
      background: var(--primary-surface);
      color: var(--primary-dark);
      border-color: var(--primary-dark);
    }

    /* Chat Styling */
    .chat-bubble {
      max-width: 82%;
      word-break: break-word;
      border-radius: 14px;
      padding: 0.65rem 0.95rem;
      font-size: 0.88rem;
    }
    .chat-bubble-self {
      background: var(--primary);
      color: #ffffff;
      border-bottom-right-radius: 4px;
    }
    .chat-bubble-other {
      background: #ffffff;
      color: var(--text-main);
      border: 1px solid var(--border-subtle);
      border-bottom-left-radius: 4px;
    }

    /* Metric Card */
    .metric-card {
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 1.15rem;
      box-shadow: var(--shadow-xs);
      text-align: center;
      transition: transform 0.18s ease;
    }
    .metric-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-sm);
    }

    /* Modals */
    .modal-content-custom {
      border-radius: var(--radius-lg);
      border: none;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
      overflow: hidden;
    }
    .modal-header-custom {
      background: linear-gradient(135deg, var(--primary) 0%, #16a34a 100%);
      color: #ffffff;
      padding: 1.15rem 1.5rem;
      border-bottom: none;
    }

    /* Toast Notification Container */
    .toast-container-custom {
      position: fixed;
      top: 1.25rem;
      right: 1.25rem;
      z-index: 1090;
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      max-width: 380px;
      pointer-events: none;
    }
    .custom-toast {
      background: #ffffff;
      border: 1px solid var(--border-subtle);
      border-left: 4px solid var(--primary);
      border-radius: var(--radius-sm);
      padding: 0.85rem 1.1rem;
      box-shadow: var(--shadow-md);
      pointer-events: auto;
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      animation: slideInToast 0.25s ease-out forwards;
      transition: opacity 0.25s ease, transform 0.25s ease;
    }
    .custom-toast-error {
      border-left-color: #ef4444;
    }
    .custom-toast-info {
      border-left-color: #3b82f6;
    }
    @keyframes slideInToast {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }

    /* Footer */
    .footer-custom {
      background: #ffffff;
      border-top: 1px solid var(--border-subtle);
      padding: 2.75rem 0 1.75rem;
      margin-top: 4.5rem;
      color: var(--text-muted);
      font-size: 0.85rem;
    }
  </style>
</head>
<body>

  <!-- Live APMC Mandi Benchmark Ticker -->
  <div class="mandi-ticker-bar">
    <div class="container d-flex align-items-center">
      <div class="ticker-pill-label flex-shrink-0">
        <span class="ticker-pulse-dot"></span>
        <span>LIVE MANDI BENCHMARKS</span>
      </div>
      <div class="overflow-hidden flex-grow-1">
        <div class="ticker-scroll-content">
          <span class="ticker-item"><strong>Azadpur APMC Tomato:</strong> ₹18.00/kg <span class="ticker-up"><i data-lucide="trending-up" class="icon-xs"></i> +₹1.50</span></span>
          <span class="ticker-item"><strong>Bowenpally Onion Red:</strong> ₹16.00/kg <span class="ticker-down"><i data-lucide="trending-down" class="icon-xs"></i> -₹0.80</span></span>
          <span class="ticker-item"><strong>Kolar APMC Potato:</strong> ₹14.00/kg <span class="ticker-up"><i data-lucide="trending-up" class="icon-xs"></i> +₹0.50</span></span>
          <span class="ticker-item"><strong>Guntur APMC Chilli Teja:</strong> ₹42.00/kg <span class="ticker-up"><i data-lucide="trending-up" class="icon-xs"></i> +₹2.20</span></span>
          <span class="ticker-item"><strong>Vashi Banana:</strong> ₹24.00/dozen <span class="text-white-50">— Stable</span></span>
          <span class="ticker-item"><strong>Warangal Turmeric:</strong> ₹92.00/kg <span class="ticker-up"><i data-lucide="trending-up" class="icon-xs"></i> +₹3.00</span></span>
          <span class="ticker-item"><strong>Shamshabad Hub Logistics:</strong> 2-Opt Pooled Freight ₹2.50/kg</span>
          <!-- Repeat for smooth infinite scroll -->
          <span class="ticker-item"><strong>Azadpur APMC Tomato:</strong> ₹18.00/kg <span class="ticker-up"><i data-lucide="trending-up" class="icon-xs"></i> +₹1.50</span></span>
          <span class="ticker-item"><strong>Bowenpally Onion Red:</strong> ₹16.00/kg <span class="ticker-down"><i data-lucide="trending-down" class="icon-xs"></i> -₹0.80</span></span>
          <span class="ticker-item"><strong>Kolar APMC Potato:</strong> ₹14.00/kg <span class="ticker-up"><i data-lucide="trending-up" class="icon-xs"></i> +₹0.50</span></span>
          <span class="ticker-item"><strong>Guntur APMC Chilli Teja:</strong> ₹42.00/kg <span class="ticker-up"><i data-lucide="trending-up" class="icon-xs"></i> +₹2.20</span></span>
        </div>
      </div>
    </div>
  </div>

  <!-- Top Navigation Bar -->
  <nav class="navbar navbar-expand-lg navbar-custom sticky-top">
    <div class="container">
      <a class="navbar-brand brand-logo" href="#" onclick="switchTab('marketplace'); return false;">
        <div class="logo-icon"><i data-lucide="sprout"></i></div>
        <span>CropConnect</span>
      </a>

      <!-- Right Nav Items -->
      <div class="d-flex align-items-center gap-2">
        <!-- Language Switcher -->
        <div class="dropdown">
          <button class="btn btn-sm btn-outline-secondary dropdown-toggle d-flex align-items-center gap-1.5 rounded-pill px-3" type="button" data-bs-toggle="dropdown">
            <i data-lucide="globe" class="icon-sm text-success"></i>
            <span id="langLabel" class="fw-semibold">English</span>
          </button>
          <ul class="dropdown-menu dropdown-menu-end shadow-sm border rounded-3">
            <li><a class="dropdown-item py-2" href="#" onclick="setLang('en');return false;"><span class="badge bg-primary-subtle text-primary border me-2">EN</span>English</a></li>
            <li><a class="dropdown-item py-2" href="#" onclick="setLang('hi');return false;"><span class="badge bg-warning-subtle text-warning-emphasis border me-2">हि</span>हिन्दी (Hindi)</a></li>
            <li><a class="dropdown-item py-2" href="#" onclick="setLang('te');return false;"><span class="badge bg-danger-subtle text-danger border me-2">తె</span>తెలుగు (Telugu)</a></li>
            <li><a class="dropdown-item py-2" href="#" onclick="setLang('ta');return false;"><span class="badge bg-success-subtle text-success border me-2">த</span>தமிழ் (Tamil)</a></li>
          </ul>
        </div>

        <!-- Auth Actions (Guest) -->
        <div id="navAuthBtns" class="d-flex gap-2">
          <button class="btn btn-sm btn-brand-outline rounded-pill px-3" data-bs-toggle="modal" data-bs-target="#authModal" onclick="setAuthTab('login')">
            <i data-lucide="log-in" class="icon-xs"></i>
            <span data-i18n="login">Log In</span>
          </button>
          <button class="btn btn-sm btn-brand rounded-pill px-3" data-bs-toggle="modal" data-bs-target="#authModal" onclick="setAuthTab('register')">
            <i data-lucide="user-plus" class="icon-xs"></i>
            <span data-i18n="register">Register</span>
          </button>
        </div>

        <!-- Logged In User State -->
        <div id="navUserArea" class="d-none align-items-center gap-2">
          <span class="badge rounded-pill" id="navUserBadge"></span>
          <span class="fw-bold text-dark small" id="navUserName"></span>
          <button class="btn btn-sm btn-outline-danger rounded-circle p-1 d-flex align-items-center justify-content-center" style="width:32px;height:32px;" onclick="logout()" title="Logout">
            <i data-lucide="log-out" class="icon-xs"></i>
          </button>
        </div>
      </div>
    </div>
  </nav>

  <!-- Hero Header -->
  <section class="hero-container">
    <div class="container text-center position-relative">
      <div class="badge-glass mb-3">
        <i data-lucide="shield-check" class="icon-xs text-emerald-300"></i>
        <span data-i18n="tagline_badge">Direct Farm-to-Buyer Marketplace &amp; Smart AI Logistics</span>
      </div>
      <h1 class="display-6 fw-bold mb-2 text-white" data-i18n="hero_title">Fair Harvest Prices for Farmers. Fresh Produce for Buyers.</h1>
      <p class="lead mb-3 text-white-50 small mx-auto" style="max-width: 720px;" data-i18n="hero_subtitle">
        Farmers earn up to +45% over APMC mandi rates, direct buyers save 25% vs supermarket markups, with zero middleman commissions and optimized pooled delivery routes.
      </p>

      <!-- SMS Helpline Callout -->
      <div class="sms-callout-pill">
        <i data-lucide="smartphone" class="icon-xs text-warning"></i>
        <span><span data-i18n="sms_hint">No smartphone needed: Farmers list via SMS:</span> <code class="text-warning fw-bold bg-dark bg-opacity-50 px-2 py-0.5 rounded">SELL TOMATO 50KG 28</code></span>
      </div>
    </div>
  </section>

  <!-- Main Tabs Navigation -->
  <div class="nav-tabs-wrapper sticky-top" style="top: 57px; z-index: 1020;">
    <div class="container">
      <ul class="nav nav-tabs nav-tabs-custom border-bottom-0" id="mainAppTabs">
        <li class="nav-item">
          <button class="nav-link active" onclick="switchTab('marketplace')" id="tab-marketplace">
            <i data-lucide="store" class="icon-sm"></i>
            <span data-i18n="nav_marketplace">Direct Marketplace</span>
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" onclick="switchTab('orders')" id="tab-orders">
            <i data-lucide="package-check" class="icon-sm"></i>
            <span data-i18n="nav_orders">Orders &amp; Requests</span>
            <span class="badge bg-danger rounded-pill ms-1 d-none" id="tabOrdersBadge">0</span>
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" onclick="switchTab('ai')" id="tab-ai">
            <i data-lucide="trending-up" class="icon-sm"></i>
            <span data-i18n="nav_ai">AI Demand Forecast</span>
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" onclick="switchTab('logistics')" id="tab-logistics">
            <i data-lucide="truck" class="icon-sm"></i>
            <span data-i18n="nav_logistics">Smart Logistics &amp; Route</span>
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" onclick="switchTab('analytics')" id="tab-analytics">
            <i data-lucide="pie-chart" class="icon-sm"></i>
            <span data-i18n="nav_value">Fair Pricing &amp; Value Chain</span>
          </button>
        </li>
      </ul>
    </div>
  </div>

  <main class="container my-4">

    <!-- ========================================================================= -->
    <!-- TAB 1: DIGITAL MARKETPLACE -->
    <!-- ========================================================================= -->
    <div id="view-marketplace" class="tab-pane-view">

      <!-- Search & Filters Container -->
      <div class="card bg-white border-0 shadow-sm rounded-4 p-3 mb-4">
        <div class="row g-2 align-items-center mb-3">
          <div class="col-md-5">
            <div class="input-group">
              <span class="input-group-text bg-light border-end-0 text-muted"><i data-lucide="search" class="icon-sm"></i></span>
              <input type="text" id="searchInput" class="form-control border-start-0 bg-light" oninput="fetchListings()" placeholder="Search crops (e.g. Tomato, Onion, Chilli)..." data-i18n-attr="placeholder" data-i18n="search_placeholder">
            </div>
          </div>
          <div class="col-md-3">
            <div class="input-group">
              <span class="input-group-text bg-light border-end-0 text-muted"><i data-lucide="map-pin" class="icon-sm"></i></span>
              <input type="text" id="zipInput" class="form-control border-start-0 bg-light" oninput="fetchListings()" placeholder="Pincode (e.g. 500001)..." data-i18n-attr="placeholder" data-i18n="zip_placeholder">
            </div>
          </div>
          <div class="col-md-2">
            <select id="sellerTypeFilter" class="form-select bg-light" onchange="fetchListings()">
              <option value="" data-i18n="filter_all_sellers">All Sellers (Farmers &amp; FPOs)</option>
              <option value="FARMER" data-i18n="filter_farmers_only">Individual Farmers</option>
              <option value="FPO" data-i18n="filter_fpos_only">FPO Collectives</option>
            </select>
          </div>
          <div class="col-md-2 d-flex gap-2">
            <button class="btn btn-brand w-100 fw-semibold" onclick="fetchListings()">
              <i data-lucide="sliders-horizontal" class="icon-xs"></i>
              <span data-i18n="filter_btn">Filter</span>
            </button>
            <button class="btn btn-outline-success d-none" id="farmerAddListingBtn" onclick="openCreateListingModal()" title="Add Crop Listing">
              <i data-lucide="plus" class="icon-sm"></i>
            </button>
          </div>
        </div>

        <!-- Category Filter Chips with Lucide React Icons -->
        <div class="d-flex align-items-center gap-2 flex-wrap pt-2 border-top">
          <span class="small fw-semibold text-muted me-1">Category:</span>
          <button type="button" class="chip-filter active" onclick="filterByChip('', this)"><i data-lucide="layers" class="icon-sm"></i> <span>All Produce</span></button>
          <button type="button" class="chip-filter" onclick="filterByChip('TOMATO', this)"><i data-lucide="apple" class="icon-sm text-danger"></i> <span>Tomatoes</span></button>
          <button type="button" class="chip-filter" onclick="filterByChip('ONION', this)"><i data-lucide="circle-dot" class="icon-sm text-purple"></i> <span>Onions</span></button>
          <button type="button" class="chip-filter" onclick="filterByChip('POTATO', this)"><i data-lucide="package" class="icon-sm text-warning"></i> <span>Potatoes</span></button>
          <button type="button" class="chip-filter" onclick="filterByChip('CHILLI', this)"><i data-lucide="flame" class="icon-sm text-danger"></i> <span>Chillies</span></button>
          <button type="button" class="chip-filter" onclick="filterByChip('BANANA', this)"><i data-lucide="citrus" class="icon-sm text-warning"></i> <span>Fruits</span></button>
          <button type="button" class="chip-filter" onclick="filterByChip('CABBAGE', this)"><i data-lucide="leaf" class="icon-sm text-success"></i> <span>Greens</span></button>
        </div>
      </div>

      <!-- Seller Quick Inventory Bar (When Farmer/FPO is Logged In) -->
      <div id="sellerDashboardBox" class="card border-0 bg-success bg-opacity-10 rounded-4 p-3 mb-4 d-none">
        <div class="d-flex flex-wrap justify-content-between align-items-center gap-2">
          <div>
            <h6 class="fw-bold text-success mb-0 d-flex align-items-center gap-1.5">
              <i data-lucide="layout-dashboard" class="icon-sm"></i>
              <span data-i18n="seller_portal">Seller Hub</span>
            </h6>
            <small class="text-muted" data-i18n="seller_portal_desc">Manage your live farm harvest listings, buyer inquiries, and automated dispatch.</small>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-sm btn-brand fw-semibold rounded-pill px-3" onclick="openCreateListingModal()">
              <i data-lucide="plus-circle" class="icon-xs"></i>
              <span data-i18n="add_listing">+ Add Harvest Listing</span>
            </button>
            <button class="btn btn-sm btn-outline-success fw-semibold rounded-pill px-3" onclick="switchTab('logistics')">
              <i data-lucide="truck" class="icon-xs"></i>
              <span data-i18n="route_dispatch">Logistics Dispatch</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Crop Listings Grid -->
      <div class="row g-4" id="listingsContainer"></div>

      <div id="noListings" class="text-center text-muted d-none my-5 py-5">
        <div class="p-3 bg-light rounded-circle d-inline-flex mb-3">
          <i data-lucide="shopping-bag" class="icon-xl text-muted"></i>
        </div>
        <h5 class="fw-bold text-dark mb-1">No Active Listings Found</h5>
        <p class="mb-0 text-muted" data-i18n="no_listings">No active crop listings match your current filters. Try searching for "Tomato" or PIN "500001".</p>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 2: ORDERS & REQUESTS -->
    <!-- ========================================================================= -->
    <div id="view-orders" class="tab-pane-view d-none">
      <div class="card bg-white border-0 shadow-sm rounded-4 p-4">
        <div class="d-flex flex-wrap justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-1 d-flex align-items-center gap-2">
              <i data-lucide="package-check" class="icon-md text-success"></i>
              <span id="ordersTitleText" data-i18n="orders_title">Orders &amp; Batch Requests</span>
            </h4>
            <p class="text-muted small mb-0" data-i18n="orders_desc">Real-time status tracking from farm-gate harvest to verified delivery.</p>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-outline-success btn-sm rounded-pill px-3 d-flex align-items-center gap-1.5" onclick="fetchOrdersData()">
              <i data-lucide="rotate-cw" class="icon-xs"></i>
              <span data-i18n="refresh">Refresh</span>
            </button>
            <button class="btn btn-brand btn-sm d-none rounded-pill px-3 d-flex align-items-center gap-1.5" id="orderAutoDispatchBtn" onclick="autoLoadOrdersToLogistics()">
              <i data-lucide="truck" class="icon-xs"></i>
              <span data-i18n="plan_route_from_orders">Plan Delivery Route</span>
            </button>
          </div>
        </div>

        <div id="ordersTableContainer">
          <div class="text-center py-5 text-muted">
            <span class="spinner-border spinner-border-sm me-2 text-success"></span><span data-i18n="loading">Loading orders...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 3: AI DEMAND FORECASTING -->
    <!-- ========================================================================= -->
    <div id="view-ai" class="tab-pane-view d-none">
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="card bg-white border-0 shadow-sm rounded-4 p-4 h-100">
            <h5 class="fw-bold text-success mb-3 d-flex align-items-center gap-2">
              <i data-lucide="sparkles" class="icon-md"></i>
              <span data-i18n="ai_forecast_config">Forecast Query</span>
            </h5>
            <div class="mb-3">
              <label class="form-label small fw-semibold text-secondary" data-i18n="crop_name">Select / Enter Crop</label>
              <select id="forecastCropSelect" class="form-select mb-2" onchange="syncForecastCropInput(this.value)">
                <option value="TOMATO">TOMATO (Tomato)</option>
                <option value="RED ONION">RED ONION (Red Onion)</option>
                <option value="POTATO">POTATO (Potato)</option>
                <option value="CHILLI">CHILLI (Green / Red Chilli)</option>
                <option value="BANANA">BANANA (Banana)</option>
                <option value="MANGO">MANGO (Mango)</option>
                <option value="CARROT">CARROT (Carrot)</option>
                <option value="RICE">RICE (Paddy / Rice)</option>
                <option value="WHEAT">WHEAT (Wheat)</option>
              </select>
              <input type="text" id="forecastCropInput" class="form-control" placeholder="Or type custom crop..." value="TOMATO">
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold text-secondary" data-i18n="forecast_horizon">Forecast Horizon</label>
              <select id="forecastDaysSelect" class="form-select">
                <option value="7">Next 7 Days</option>
                <option value="14">Next 14 Days</option>
                <option value="30">Next 30 Days</option>
              </select>
            </div>
            <button class="btn btn-brand w-100 py-2 fw-semibold rounded-pill" onclick="runAIDemandForecast()">
              <i data-lucide="cpu" class="icon-sm"></i>
              <span data-i18n="run_forecast_btn">Generate AI Forecast</span>
            </button>
            
            <hr class="my-4">
            <div class="small text-muted">
              <h6 class="fw-bold text-dark small mb-2 d-flex align-items-center gap-1.5">
                <i data-lucide="info" class="icon-xs text-primary"></i>How the AI Engine Works:
              </h6>
              <ul class="ps-3 mb-0" style="font-size:0.82rem; line-height: 1.6;">
                <li>Recency-weighted regression on real marketplace order transactions.</li>
                <li>Crop perishability &amp; seasonal elasticity weighting.</li>
                <li>Equilibrium pricing balancing farmer profit vs buyer savings in ₹.</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="col-lg-8">
          <div class="card bg-white border-0 shadow-sm rounded-4 p-4 h-100" id="forecastResultsCard">
            <div class="text-center py-5 text-muted">
              <div class="p-3 bg-light rounded-circle d-inline-flex mb-2">
                <i data-lucide="bar-chart-3" class="icon-xl text-muted"></i>
              </div>
              <p data-i18n="ai_forecast_prompt">Select a crop and click 'Generate AI Forecast' to view demand projections &amp; price advice.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 4: SMART LOGISTICS & 2-OPT ROUTE OPTIMIZATION -->
    <!-- ========================================================================= -->
    <div id="view-logistics" class="tab-pane-view d-none">
      <div class="card bg-white border-0 shadow-sm rounded-4 p-4 mb-4">
        <div class="d-flex flex-wrap justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-1 d-flex align-items-center gap-2">
              <i data-lucide="truck" class="icon-md text-success"></i>
              <span data-i18n="logistics_title">Smart Logistics &amp; Route Optimizer</span>
            </h4>
            <p class="text-muted small mb-0" data-i18n="logistics_desc">Consolidated multi-drop routing cuts road miles, fuel costs in ₹, and transit spoilage.</p>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-outline-success btn-sm rounded-pill px-3 d-flex align-items-center gap-1.5" onclick="autoLoadOrdersToLogistics()">
              <i data-lucide="sparkles" class="icon-xs"></i>
              <span data-i18n="auto_import_orders">Auto-Import Accepted Orders</span>
            </button>
          </div>
        </div>

        <div class="row g-4">
          <div class="col-lg-5">
            <div class="p-3 bg-light rounded-4 border">
              <h6 class="fw-bold text-dark mb-3 d-flex align-items-center gap-1.5">
                <i data-lucide="map-pin" class="icon-sm text-danger"></i>Hub Origin &amp; Vehicle Capacity
              </h6>
              <div class="row g-2 mb-3">
                <div class="col-12">
                  <label class="form-label small fw-semibold text-secondary">Origin Hub Name</label>
                  <input id="originName" class="form-control form-control-sm" value="Shamshabad Agri Hub / Central Warehouse">
                </div>
                <div class="col-6">
                  <label class="form-label small fw-semibold text-secondary">Origin Lat</label>
                  <input id="originLat" type="number" step="any" class="form-control form-control-sm" value="17.2500">
                </div>
                <div class="col-6">
                  <label class="form-label small fw-semibold text-secondary">Origin Lon</label>
                  <input id="originLon" type="number" step="any" class="form-control form-control-sm" value="78.4200">
                </div>
                <div class="col-12">
                  <label class="form-label small fw-semibold text-secondary">Vehicle Capacity (KG)</label>
                  <input id="vehicleCapacity" type="number" class="form-control form-control-sm" value="800">
                </div>
              </div>

              <h6 class="fw-bold text-dark mb-2 d-flex align-items-center gap-1.5">
                <i data-lucide="milestone" class="icon-sm text-success"></i>Delivery Waypoint Stops
              </h6>
              <p class="text-muted" style="font-size:0.78rem;">Format per line: <code>Buyer Name, Lat, Lon, KG, [Address]</code></p>
              <textarea id="routeStops" class="form-control font-monospace mb-3" rows="6" placeholder="Wholesale Mart Begumpet, 17.4435, 78.4738, 150, Secunderabad&#10;Green Valley Apt Banjara Hills, 17.4156, 78.4350, 25, Road 12&#10;Kukatpally Supermarket, 17.4933, 78.3995, 200, Main Road&#10;Madhapur Organic Store, 17.4483, 78.3915, 80, Hitec City"></textarea>

              <button class="btn btn-brand w-100 fw-semibold rounded-pill" onclick="runRouteOptimizer()">
                <i data-lucide="route" class="icon-sm"></i>
                <span data-i18n="optimize_route_btn">Optimize Delivery Route</span>
              </button>
            </div>
          </div>

          <div class="col-lg-7">
            <div id="routeResultsBox" class="p-3 bg-light rounded-4 border h-100">
              <div class="text-center py-5 text-muted">
                <div class="p-3 bg-white rounded-circle d-inline-flex mb-2 shadow-sm">
                  <i data-lucide="map" class="icon-xl text-muted"></i>
                </div>
                <p class="mb-0" data-i18n="route_prompt">Add waypoint stops and click 'Optimize Delivery Route' to generate the most efficient drop sequence.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Dispatched Trips History -->
        <div class="mt-5">
          <h5 class="fw-bold text-dark mb-3 d-flex align-items-center gap-2">
            <i data-lucide="clock" class="icon-md text-primary"></i>
            <span data-i18n="active_trips_title">Active Logistics Trips</span>
          </h5>
          <div id="tripsListContainer">
            <p class="text-muted small">Loading active trips...</p>
          </div>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 5: FAIR PRICING & VALUE CHAIN TRANSPARENCY -->
    <!-- ========================================================================= -->
    <div id="view-analytics" class="tab-pane-view d-none">
      <div class="card bg-white border-0 shadow-sm rounded-4 p-4 mb-4">
        <div class="d-flex flex-wrap justify-content-between align-items-center mb-3">
          <div>
            <h4 class="fw-bold text-dark mb-1 d-flex align-items-center gap-2">
              <i data-lucide="pie-chart" class="icon-md text-success"></i>
              <span data-i18n="fair_price_title">Fair Pricing &amp; Middleman Elimination Breakdown</span>
            </h4>
            <p class="text-muted small mb-0" data-i18n="fair_price_desc">Compare traditional multi-hop mandi losses vs CropConnect direct farm linkage.</p>
          </div>
          <div class="d-flex gap-2 align-items-center">
            <label class="small fw-semibold text-secondary mb-0">Crop:</label>
            <select id="valueCropSelect" class="form-select form-select-sm" onchange="fetchValueDistribution(this.value)">
              <option value="TOMATO">TOMATO (Tomato)</option>
              <option value="RED ONION">RED ONION (Red Onion)</option>
              <option value="POTATO">POTATO (Potato)</option>
              <option value="CHILLI">CHILLI (Chilli)</option>
              <option value="BANANA">BANANA (Banana)</option>
              <option value="MANGO">MANGO (Mango)</option>
            </select>
          </div>
        </div>

        <div id="valueDistributionContent">
          <div class="text-center py-5 text-muted">
            <span class="spinner-border spinner-border-sm me-2 text-success"></span>Loading value distribution model...
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- ========================================================================= -->
  <!-- MODALS -->
  <!-- ========================================================================= -->

  <!-- Auth Modal -->
  <div class="modal fade" id="authModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content modal-content-custom">
        <div class="modal-header border-bottom-0 pb-0">
          <ul class="nav nav-tabs border-bottom-0" id="authTabs">
            <li class="nav-item">
              <button class="nav-link active fw-bold" id="login-tab" data-bs-toggle="tab" data-bs-target="#login-pane" data-i18n="login">Log In</button>
            </li>
            <li class="nav-item">
              <button class="nav-link fw-bold" id="register-tab" data-bs-toggle="tab" data-bs-target="#register-pane" data-i18n="register">Register</button>
            </li>
          </ul>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body p-4">
          <div class="tab-content">
            <!-- LOGIN FORM -->
            <div class="tab-pane fade show active" id="login-pane">
              <form onsubmit="handleLogin(event)">
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="role_label">Account Role</label>
                  <select class="form-select" id="loginRole">
                    <option value="FARMER">Farmer — Individual Cultivator</option>
                    <option value="FPO">FPO — Farmer Producer Organization / Collective</option>
                    <option value="BULK_BUYER">Bulk Buyer — Wholesaler, Supermarket, HoReCa</option>
                    <option value="CONSUMER">Consumer — Direct Household / Retail Buyer</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="phone_placeholder">Phone Number</label>
                  <input type="tel" class="form-control" id="loginPhone" required placeholder="+919876543210 or 9876543210">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="password_placeholder">Password</label>
                  <input type="password" class="form-control" id="loginPassword" required placeholder="Password">
                </div>
                <button type="submit" class="btn btn-brand w-100 py-2 fw-semibold rounded-pill" data-i18n="sign_in">Sign In</button>
                
                <!-- Quick 1-Click Demo Accounts -->
                <div class="p-3 bg-light border small mt-3 mb-0 rounded-3">
                  <div class="fw-bold text-dark mb-1 d-flex align-items-center gap-1">
                    <i data-lucide="zap" class="icon-xs text-warning"></i>
                    <span>Quick-Fill Demo Accounts:</span>
                  </div>
                  <div class="d-flex flex-wrap gap-1 mt-2">
                    <button type="button" class="btn btn-xs btn-outline-success rounded-pill px-2 py-1" onclick="quickFillAuth('+919876543210', 'password123', 'FARMER')">
                      Farmer (Ramesh)
                    </button>
                    <button type="button" class="btn btn-xs btn-outline-primary rounded-pill px-2 py-1" onclick="quickFillAuth('+919876543220', 'password123', 'FPO')">
                      FPO Collective
                    </button>
                    <button type="button" class="btn btn-xs btn-outline-warning rounded-pill px-2 py-1" onclick="quickFillAuth('+919876543211', 'password123', 'BULK_BUYER')">
                      Bulk Buyer
                    </button>
                    <button type="button" class="btn btn-xs btn-outline-info rounded-pill px-2 py-1" onclick="quickFillAuth('+919876543230', 'password123', 'CONSUMER')">
                      Consumer (Priya)
                    </button>
                  </div>
                </div>
              </form>
            </div>
            
            <!-- REGISTER FORM -->
            <div class="tab-pane fade" id="register-pane">
              <form onsubmit="handleRegister(event)">
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="role_label">Account Role</label>
                  <select class="form-select" id="regRole">
                    <option value="FARMER">Farmer — Individual Cultivator</option>
                    <option value="FPO">FPO — Farmer Producer Organization / Collective</option>
                    <option value="BULK_BUYER">Bulk Buyer — Wholesaler, Supermarket, HoReCa</option>
                    <option value="CONSUMER">Consumer — Direct Household / Retail Buyer</option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="name_placeholder">Full / Collective Name</label>
                  <input type="text" class="form-control" id="regName" required placeholder="e.g. Ramesh Kumar or Telangana Kisan FPO">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="phone_placeholder">Phone Number</label>
                  <input type="tel" class="form-control" id="regPhone" required placeholder="e.g. +919876543210">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="zip_code">Pin Code</label>
                  <input type="text" class="form-control" id="regZip" required placeholder="e.g. 500001">
                </div>
                <div class="mb-3">
                  <label class="form-label small fw-semibold text-secondary" data-i18n="password_placeholder">Password</label>
                  <input type="password" class="form-control" id="regPassword" required placeholder="Create password">
                </div>
                <button type="submit" class="btn btn-brand w-100 py-2 fw-semibold rounded-pill" data-i18n="create_account">Create Account</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Add / Edit Listing Modal -->
  <div class="modal fade" id="listingModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content modal-content-custom">
        <div class="modal-header modal-header-custom">
          <h5 class="modal-title fw-bold d-flex align-items-center gap-2" id="listingModalTitle">
            <i data-lucide="plus-circle" class="icon-sm"></i>
            <span data-i18n="new_listing_title">Add Harvest Listing</span>
          </h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <form onsubmit="handleSaveListing(event)">
          <div class="modal-body p-4">
            <input type="hidden" id="listingId">
            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="crop_name">Crop Name</label>
              <input type="text" class="form-control" id="listingCrop" required placeholder="e.g. TOMATO, RED ONION, POTATO">
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-semibold" data-i18n="quantity_kg">Available Quantity (KG)</label>
                <input type="number" step="any" min="1" class="form-control" id="listingQty" required placeholder="e.g. 250">
              </div>
              <div class="col-6">
                <label class="form-label small fw-semibold">Price per KG (₹)</label>
                <input type="number" step="any" min="1" class="form-control" id="listingPrice" required placeholder="e.g. 28">
              </div>
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-semibold">Min Order Qty (KG)</label>
                <input type="number" step="any" min="1" class="form-control" id="listingMinQty" value="5" placeholder="5">
              </div>
              <div class="col-6">
                <label class="form-label small fw-semibold">Bulk Rate (₹/KG for 50+ KG)</label>
                <input type="number" step="any" min="1" class="form-control" id="listingBulkPrice" placeholder="Optional discount">
              </div>
            </div>
            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-semibold" data-i18n="zip_code">Pin Code</label>
                <input type="text" class="form-control" id="listingZip" required placeholder="e.g. 500001">
              </div>
              <div class="col-6">
                <label class="form-label small fw-semibold">Shelf Life (Days)</label>
                <input type="number" class="form-control" id="listingShelfLife" value="7" placeholder="7">
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label small fw-semibold">Quality Grade / Description</label>
              <input type="text" class="form-control" id="listingGrade" value="Grade A - Freshly Harvested" placeholder="e.g. Organic Certified Grade A">
            </div>
          </div>
          <div class="modal-footer bg-light rounded-bottom-4">
            <button type="button" class="btn btn-secondary rounded-pill px-3" data-bs-dismiss="modal" data-i18n="cancel">Cancel</button>
            <button type="submit" class="btn btn-brand rounded-pill px-4 fw-semibold" data-i18n="save">Save Listing</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Place Order Modal -->
  <div class="modal fade" id="orderModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content modal-content-custom">
        <div class="modal-header modal-header-custom">
          <h5 class="modal-title fw-bold d-flex align-items-center gap-2" id="orderModalTitle">
            <i data-lucide="shopping-bag" class="icon-sm"></i>
            <span data-i18n="request_order_title">Order Fresh Crop Batch</span>
          </h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <form onsubmit="handleSubmitOrder(event)">
          <div class="modal-body p-4">
            <input type="hidden" id="orderListingId">
            <input type="hidden" id="orderPricePerKg">
            <input type="hidden" id="orderBulkPricePerKg">

            <div class="alert alert-light border rounded-3 mb-3 p-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="fw-bold text-success fs-5" id="orderCropName">TOMATO</span>
                <span class="badge bg-success-subtle text-success fs-6" id="orderPriceBadge">₹28/kg</span>
              </div>
              <small class="text-muted d-block">
                <span data-i18n="seller">Seller</span>: <strong id="orderFarmerName">Ramesh Kumar</strong> (<span id="orderFarmerPhone"></span>)
              </small>
              <small class="text-muted d-block">
                <span data-i18n="available_stock">Available Stock</span>: <strong id="orderAvailableQty" class="text-dark">450</strong> KG
              </small>
              <small class="text-muted d-block">
                <span data-i18n="min_order">Min Order</span>: <strong id="orderMinQty" class="text-dark">5</strong> KG
              </small>
            </div>

            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="request_qty">Quantity to Order (KG)</label>
              <input type="number" step="any" min="1" class="form-control form-control-lg fw-bold text-success" id="orderQuantityInput" required oninput="updateOrderTotal()">
            </div>

            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="delivery_address">Delivery Address / Destination</label>
              <textarea class="form-control" id="orderDeliveryAddress" rows="2" required placeholder="Door / shop address with landmark"></textarea>
            </div>

            <div class="row g-2 mb-3">
              <div class="col-6">
                <label class="form-label small fw-semibold">Destination Lat</label>
                <input type="number" step="any" class="form-control form-control-sm" id="orderDeliveryLat" value="17.4156">
              </div>
              <div class="col-6">
                <label class="form-label small fw-semibold">Destination Lon</label>
                <input type="number" step="any" class="form-control form-control-sm" id="orderDeliveryLon" value="78.4350">
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label small fw-semibold" data-i18n="order_notes">Delivery Notes (Optional)</label>
              <input type="text" class="form-control form-control-sm" id="orderNotesInput" placeholder="e.g. Deliver before 10 AM, wholesale gate entry">
            </div>

            <!-- Transparent Price Breakdown in ₹ -->
            <div class="p-3 bg-light rounded-3 border">
              <div class="d-flex justify-content-between mb-1">
                <span class="text-muted small">Estimated Total:</span>
                <span class="fs-4 fw-bold text-success" id="orderTotalPriceEst">₹0</span>
              </div>
              <div class="d-flex justify-content-between align-items-center">
                <span class="badge bg-warning-subtle text-warning-emphasis border" id="orderSavingsBadge">You save ~₹0 vs Retail!</span>
                <small class="text-muted"><i data-lucide="shield-check" class="icon-xs text-success me-1"></i>₹0 Middleman Cut</small>
              </div>
            </div>
          </div>
          <div class="modal-footer bg-light rounded-bottom-4">
            <button type="button" class="btn btn-secondary rounded-pill px-3" data-bs-dismiss="modal" data-i18n="cancel">Cancel</button>
            <button type="submit" class="btn btn-brand rounded-pill px-4 fw-semibold" data-i18n="submit_order_btn">Confirm &amp; Place Order</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Direct Chat Modal -->
  <div class="modal fade" id="chatModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content modal-content-custom">
        <div class="modal-header modal-header-custom">
          <div>
            <h6 class="modal-title fw-bold mb-0 d-flex align-items-center gap-1.5" id="chatCropTitle">
              <i data-lucide="message-square" class="icon-sm"></i>
              <span>Direct Chat</span>
            </h6>
            <small class="text-white-50" id="chatPartnerTitle"></small>
          </div>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body p-3">
          <div id="farmerBuyerBar" class="p-2 bg-light rounded-3 mb-2 d-none">
            <small class="fw-semibold text-secondary d-block mb-1" data-i18n="select_buyer">Active Conversations:</small>
            <div class="d-flex gap-1 flex-wrap" id="buyerChipsContainer"></div>
          </div>

          <div class="chat-box p-3 bg-light rounded-3 mb-3" id="chatMessagesList" style="height: 320px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px;">
            <p class="text-muted small text-center my-auto">Loading messages...</p>
          </div>

          <form onsubmit="handleSendMessage(event)" class="d-flex gap-2">
            <input type="text" class="form-control rounded-pill px-3" id="chatInputText" placeholder="Type a message..." data-i18n-attr="placeholder" data-i18n="type_message" required>
            <button type="submit" class="btn btn-brand rounded-circle p-0 d-flex align-items-center justify-content-center" style="width:42px;height:42px;flex-shrink:0;" id="chatSendBtn">
              <i data-lucide="send" class="icon-sm"></i>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Floating Toast Notifications Container -->
  <div class="toast-container-custom" id="toastContainer"></div>

  <!-- Handcrafted Footer -->
  <footer class="footer-custom">
    <div class="container">
      <div class="row g-4 align-items-center">
        <div class="col-md-6">
          <div class="d-flex align-items-center gap-2 mb-2">
            <div class="logo-icon" style="width:28px;height:28px;"><i data-lucide="sprout" class="icon-sm text-success"></i></div>
            <strong class="text-dark fs-6">CropConnect</strong>
          </div>
          <p class="text-muted small mb-0">Empowering Indian farmers and direct buyers through transparent pricing in ₹, direct chat, and consolidated 2-Opt logistics.</p>
        </div>
        <div class="col-md-6 text-md-end">
          <div class="small text-muted mb-1">
            <i data-lucide="phone" class="icon-xs text-success me-1"></i> Kisan Call Centre / Farmer Helpline: <strong>1800-180-1551</strong>
          </div>
          <div class="small text-muted">
            <i data-lucide="shield-check" class="icon-xs text-primary me-1"></i> APMC Mandi Benchmark Integration &middot; Zero Hidden Markups
          </div>
        </div>
      </div>
    </div>
  </footer>

  <!-- Bootstrap 5 JS -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

  <script>
    // ==========================================
    // MULTILINGUAL I18N DICTIONARY (ALL IN ₹)
    // ==========================================
    const I18N = {
      en: {
        app_name: "CropConnect",
        hero_title: "Fair Harvest Prices for Farmers. Fresh Produce for Buyers.",
        hero_subtitle: "Farmers earn up to +45% over APMC mandi rates, direct buyers save 25% vs supermarket markups, with zero middleman commissions.",
        tagline_badge: "Direct Farm-to-Buyer Marketplace & Smart AI Logistics",
        sms_hint: "No smartphone needed: Farmers list via SMS:",
        login: "Log In", register: "Register", logout: "Log Out",
        nav_marketplace: "Direct Marketplace", nav_orders: "Orders & Requests",
        nav_ai: "AI Demand Forecast", nav_logistics: "Smart Logistics & Route",
        nav_value: "Fair Pricing & Value Chain",
        search_placeholder: "Search crops (e.g. Tomato, Onion, Chilli)...",
        zip_placeholder: "Pincode (e.g. 500001)...",
        filter_all_sellers: "All Sellers (Farmers & FPOs)",
        filter_farmers_only: "Individual Farmers",
        filter_fpos_only: "FPO Collectives",
        filter_btn: "Filter", add_listing: "+ Add Harvest Listing",
        seller_portal: "Seller Hub",
        seller_portal_desc: "Manage your live farm harvest listings, buyer inquiries, and automated dispatch.",
        route_dispatch: "Logistics Dispatch",
        no_listings: "No active crop listings found matching your search.",
        kg_left: "KG Left", min_order: "Min Order",
        market_benchmark: "Retail Supermarket:",
        farmer_gain: "Farmer earns +45% more",
        consumer_save: "Save 25% vs Retail",
        chat_seller: "Chat with Seller", order_now: "Order Batch / Retail",
        orders_title: "Orders & Batch Requests",
        orders_desc: "Real-time status tracking from farm-gate harvest to verified delivery.",
        refresh: "Refresh", plan_route_from_orders: "Plan Delivery Route",
        crop_name: "Crop Name", seller: "Seller", quantity_kg: "Quantity (KG)",
        total_price: "Total Price", status: "Status", actions: "Actions",
        status_pending: "Pending", status_accepted: "Accepted",
        status_rejected: "Declined", status_dispatched: "Dispatched",
        status_delivered: "Delivered", status_cancelled: "Cancelled",
        accept: "Accept", decline: "Decline", chat: "Chat", cancel_order: "Cancel",
        new_listing_title: "Add Harvest Listing", edit_listing_title: "Edit Harvest Listing",
        save: "Save Listing", cancel: "Cancel",
        request_order_title: "Order Fresh Crop Batch",
        request_qty: "Quantity to Order (KG)", delivery_address: "Delivery Address / Destination",
        order_notes: "Delivery Notes (Optional)", submit_order_btn: "Confirm & Place Order",
        available_stock: "Available Stock",
        ai_forecast_config: "Forecast Query", forecast_horizon: "Forecast Horizon",
        run_forecast_btn: "Generate AI Forecast", ai_forecast_prompt: "Select a crop and click 'Generate AI Forecast' to view demand projections & price advice.",
        logistics_title: "Smart Logistics & Route Optimizer",
        logistics_desc: "Consolidated multi-drop routing cuts road miles, fuel costs in ₹, and transit spoilage.",
        auto_import_orders: "Auto-Import Accepted Orders",
        optimize_route_btn: "Optimize Delivery Route",
        route_prompt: "Add waypoint stops and click 'Optimize Delivery Route' to generate the most efficient drop sequence.",
        active_trips_title: "Active Logistics Trips",
        fair_price_title: "Fair Pricing & Middleman Elimination Breakdown",
        fair_price_desc: "Compare traditional multi-hop mandi losses vs CropConnect direct farm linkage.",
        type_message: "Type a message...", send: "Send",
        select_buyer: "Active Conversations:", loading: "Loading...",
        you: "You"
      },
      hi: {
        app_name: "क्रॉपकनेक्ट",
        hero_title: "किसानों को उचित मूल्य, उपभोक्ताओं को ताज़ी फसल।",
        hero_subtitle: "किसानों को मंडी से +45% अधिक लाभ, उपभोक्ताओं को खुदरा से 25% बचत, शून्य बिचौलिया और AI रूट डिलीवरी।",
        tagline_badge: "सीधा डिजिटल बाज़ार + स्मार्ट AI लॉजिस्टिक्स",
        sms_hint: "किसान SMS भेजें:",
        login: "लॉग इन", register: "पंजीकरण", logout: "लॉग आउट",
        nav_marketplace: "सीधा बाज़ार", nav_orders: "ऑर्डर व अनुरोध",
        nav_ai: "AI मांग पूर्वानुमान", nav_logistics: "स्मार्ट लॉजिस्टिक्स व रूट",
        nav_value: "उचित मूल्य व बचत विश्लेषण",
        search_placeholder: "फसल खोजें (जैसे टमाटर, प्याज)...",
        zip_placeholder: "पिन कोड (जैसे 500001)...",
        filter_all_sellers: "सभी विक्रेता (किसान व FPO)",
        filter_farmers_only: "केवल व्यक्तिगत किसान",
        filter_fpos_only: "केवल FPO समूह",
        filter_btn: "फ़िल्टर", add_listing: "+ फसल जोड़ें",
        seller_portal: "विक्रेता केंद्र (Seller Hub)",
        seller_portal_desc: "अपनी फसल सूची, ऑर्डर और 1-क्लिक लॉजिस्टिक्स डिलीवरी प्रबंधित करें।",
        route_dispatch: "लॉजिस्टिक्स डिस्पैच",
        no_listings: "कोई सक्रिय फसल सूची नहीं मिली।",
        kg_left: "किलो शेष", min_order: "न्यूनतम ऑर्डर",
        market_benchmark: "खुदरा बाज़ार दर:",
        farmer_gain: "किसान को +45% अधिक लाभ",
        consumer_save: "खुदरा से 25% बचत",
        chat_seller: "विक्रेता से चैट करें", order_now: "ऑर्डर करें",
        orders_title: "ऑर्डर और बैच अनुरोध",
        orders_desc: "खेत से उपभोक्ता तक सीधी डिलीवरी ट्रैकिंग।",
        refresh: "ताज़ा करें", plan_route_from_orders: "डिलीवरी रूट बनाएं",
        crop_name: "फसल का नाम", seller: "विक्रेता", quantity_kg: "मात्रा (किलो)",
        total_price: "कुल मूल्य", status: "स्थिति", actions: "कार्रवाई",
        status_pending: "लंबित", status_accepted: "स्वीकृत",
        status_rejected: "अस्वीकृत", status_dispatched: "रवाना (Dispatched)",
        status_delivered: "वितरित (Delivered)", status_cancelled: "रद्द",
        accept: "स्वीकार करें", decline: "अस्वीकार", chat: "चैट", cancel_order: "रद्द करें",
        new_listing_title: "नई फसल सूची जोड़ें", edit_listing_title: "फसल सूची संपादित करें",
        save: "सहेजें", cancel: "रद्द करें",
        request_order_title: "ताज़ी फसल का ऑर्डर दें",
        request_qty: "खरीदने की मात्रा (किलो)", delivery_address: "डिलीवरी का पता",
        order_notes: "डिलीवरी निर्देश / टिप्पणी", submit_order_btn: "ऑर्डर की पुष्टि करें",
        available_stock: "उपलब्ध स्टॉक",
        ai_forecast_config: "पूर्वानुमान खोज", forecast_horizon: "पूर्वानुमान अवधि",
        run_forecast_btn: "AI पूर्वानुमान चलाएं", ai_forecast_prompt: "मांग और मूल्य सलाह देखने के लिए फसल चुनें।",
        logistics_title: "स्मार्ट लॉजिस्टिक्स व रूट ऑप्टिमाइज़र",
        logistics_desc: "2-Opt रूटिंग दूरी, ईंधन लागत और फसल के खराब होने को कम करती है।",
        auto_import_orders: "स्वीकृत ऑर्डर स्वतः जोड़ें",
        optimize_route_btn: "रूट ऑप्टिमाइज़ करें",
        route_prompt: "रूट तैयार करने के लिए स्टॉप जोड़ें।",
        active_trips_title: "सक्रिय लॉजिस्टिक्स ट्रिप",
        fair_price_title: "उचित मूल्य व बिचौलिया उन्मूलन",
        fair_price_desc: "देखें कि सीधे बाज़ार से किसानों और उपभोक्ताओं को कितना लाभ होता है।",
        type_message: "संदेश लिखें...", send: "भेजें",
        select_buyer: "खरीदार पूछताछ:", loading: "लोड हो रहा है...",
        you: "आप"
      },
      te: {
        app_name: "క్రాప్‌కనెక్ట్",
        hero_title: "రైతులకు గిట్టుబాటు ధర. కొనుగోలుదారులకు తాజా పంట.",
        hero_subtitle: "రైతులకు +45% అధిక ఆదాయం, కొనుగోలుదారులకు 25% ఆదా, దళారులు లేని నేరుగా సరఫరా & AI రవాణా.",
        tagline_badge: "ప్రత్యక్ష డిజిటల్ మార్కెట్ + స్మార్ట్ AI లాజిస్టిక్స్",
        sms_hint: "రైతులు SMS పంపండి:",
        login: "లాగిన్", register: "నమోదు", logout: "లాగౌట్",
        nav_marketplace: "ప్రత్యక్ష మార్కెట్", nav_orders: "ఆర్డర్లు & అభ్యర్థనలు",
        nav_ai: "AI డిమాండ్ అంచనా", nav_logistics: "స్మార్ట్ లాజిస్టిక్స్ & రూట్",
        nav_value: "ధర & విలువ విశ్లేషణ",
        search_placeholder: "పంటను శోధించండి (ఉదా: టమోటా)...",
        zip_placeholder: "పిన్ కోడ్ (ఉదా: 500001)...",
        filter_all_sellers: "అందరూ అమ్మకందారులు (రైతులు & FPOలు)",
        filter_farmers_only: "రైతులు మాత్రమే",
        filter_fpos_only: "FPO సంఘాలు మాత్రమే",
        filter_btn: "ఫిల్టర్", add_listing: "+ పంటను జోడించండి",
        seller_portal: "విక్రేత కేంద్రం (Seller Hub)",
        seller_portal_desc: "మీ పంట నిల్వలు, ఆర్డర్లు మరియు డెలివరీ రూట్‌ను నిర్వహించండి.",
        route_dispatch: "రవాణా పంపు",
        no_listings: "పంట జాబితాలు ఏవీ దొరకలేదు.",
        kg_left: "కేజీ మిగిలి ఉంది", min_order: "కనిష్ట ఆర్డర్",
        market_benchmark: "మార్కెట్ ధర:",
        farmer_gain: "రైతుకు +45% అధిక ఆదాయం",
        consumer_save: "రిటైల్ కంటే 25% ఆదా",
        chat_seller: "రైతుతో చాట్ చేయండి", order_now: "ఆర్డర్ చేయండి",
        orders_title: "ఆర్డర్లు & అభ్యర్థనలు",
        orders_desc: "పొలం నుండి నేరుగా డెలివరీ స్థితిని ట్రాక్ చేయండి.",
        refresh: "రిఫ్రెష్", plan_route_from_orders: "డెలివరీ రూట్ ప్లాన్ చేయండి",
        crop_name: "పంట పేరు", seller: "విక్రేత", quantity_kg: "పరిమాణం (కేజీ)",
        total_price: "మొత్తం ధర", status: "స్థితి", actions: "చర్యలు",
        status_pending: "పెండింగ్", status_accepted: "అంగీకరించబడింది",
        status_rejected: "తిరస్కరించబడింది", status_dispatched: "రవాణాలో ఉంది",
        status_delivered: "చేరింది (Delivered)", status_cancelled: "రద్దు చేయబడింది",
        accept: "అంగీకరించు", decline: "తిరస్కరించు", chat: "చాట్", cancel_order: "రద్దు చేయి",
        new_listing_title: "కొత్త పంటను చేర్చండి", edit_listing_title: "పంట జాబితా సవరణ",
        save: "భద్రపరచు", cancel: "రద్దు చేయి",
        request_order_title: "తాజా పంటను ఆర్డర్ చేయండి",
        request_qty: "కొనుగోలు పరిమాణం (కేజీ)", delivery_address: "డెలివరీ చిరునామా",
        order_notes: "డెలివరీ సూచనలు", submit_order_btn: "ఆర్డర్ నిర్ధారించండి",
        available_stock: "అందుబాటులో ఉన్న నిల్వ",
        ai_forecast_config: "డిమాండ్ అంచనా", forecast_horizon: "అంచనా కాలం",
        run_forecast_btn: "AI అంచనా వేయండి", ai_forecast_prompt: "పంటను ఎంచుకుని అంచనా వేయండి.",
        logistics_title: "స్మార్ట్ లాజిస్టిక్స్ & రూట్ ఆప్టిమైజర్",
        logistics_desc: "2-Opt రూటింగ్ ద్వారా రవాణా దూరం మరియు ఖర్చు ఆదా అవుతాయి.",
        auto_import_orders: "ఆర్డర్లను నేరుగా తీసుకోండి",
        optimize_route_btn: "రూట్ ఆప్టిమైజ్ చేయండి",
        route_prompt: "రూట్ కోసం డెలివరీ స్థలాలను చేర్చండి.",
        active_trips_title: "ప్రస్తుత రవాణా ట్రిప్పులు",
        fair_price_title: "సరసమైన ధర & దళారుల తొలగింపు",
        fair_price_desc: "రైతులు మరియు వినియోగదారులకు పొందే లాభాన్ని చూడండి.",
        type_message: "సందేశం రాయండి...", send: "పంపు",
        select_buyer: "కొనుగోలుదారుల సందేశాలు:", loading: "లోడ్ అవుతోంది...",
        you: "మీరు"
      },
      ta: {
        app_name: "கிராப்கனெக்ட்",
        hero_title: "விவசாயிகளுக்கு நியாயமான விலை. நுகர்வோருக்கு புதிய விளைபொருட்கள்.",
        hero_subtitle: "விவசாயிகளுக்கு +45% அதிக வருமானம், நுகர்வோருக்கு 25% சேமிப்பு, இடைத்தரகர் இல்லா வர்த்தகம் & AI போக்குவரத்து.",
        tagline_badge: "நேரடி டிஜிட்டல் சந்தை + ஸ்மார்ட் AI தளவாடங்கள்",
        sms_hint: "விவசாயிகள் SMS அனுப்புக:",
        login: "உள்நுழைக", register: "பதிவு செய்க", logout: "வெளியேறுக",
        nav_marketplace: "நேரடி சந்தை", nav_orders: "ஆர்டர்கள் & கோரிக்கைகள்",
        nav_ai: "AI தேவை கணிப்பு", nav_logistics: "ஸ்மார்ட் தளவாடங்கள் & பாதை",
        nav_value: "நியாயமான விலை பகுப்பாய்வு",
        search_placeholder: "பயிர்களைத் தேடுக (எ.கா. தக்காளி, வெங்காயம்)...",
        zip_placeholder: "பின்கோடு (எ.கா. 500001)...",
        filter_all_sellers: "அனைத்து விற்பனையாளர்கள்",
        filter_farmers_only: "விவசாயிகள் மட்டும்",
        filter_fpos_only: "FPO அமைப்புகள் மட்டும்",
        filter_btn: "வடிகட்டுக", add_listing: "+ பயிரை சேர்க்கவும்",
        seller_portal: "விற்பனையாளர் மையம் (Seller Hub)",
        seller_portal_desc: "உங்கள் விளைபொருள் இருப்பு, ஆர்டர்கள் மற்றும் போக்குவரத்து வழியை நிர்வகிக்கவும்.",
        route_dispatch: "தளவாடங்கள் அனுப்புக",
        no_listings: "விளைபொருள் எதுவும் கிடைக்கவில்லை.",
        kg_left: "கிலோ மீதம்", min_order: "குறைந்தபட்ச ஆர்டர்",
        market_benchmark: "சந்தை விலை:",
        farmer_gain: "விவசாயிக்கு +45% கூடுதல் வருவாய்",
        consumer_save: "சில்லறை விலையை விட 25% சேமிப்பு",
        chat_seller: "விவசாயியுடன் அரட்டையடிக்கவும்", order_now: "ஆர்டர் செய்க",
        orders_title: "ஆர்டர்கள் மற்றும் கோரிக்கைகள்",
        orders_desc: "பண்ணையிலிருந்து நுகர்வோர் வரை நேரடி கண்காணிப்பு.",
        refresh: "புதுப்பி", plan_route_from_orders: "டெலிவரி பாதையை திட்டமிடுக",
        crop_name: "பயிரின் பெயர்", seller: "விற்பனையாளர்", quantity_kg: "அளவு (கிலோ)",
        total_price: "மொத்த விலை", status: "நிலை", actions: "செயல்கள்",
        status_pending: "நிலுவையில்", status_accepted: "ஏற்றுக்கொள்ளப்பட்டது",
        status_rejected: "நிராகரிக்கப்பட்டது", status_dispatched: "அனுப்பப்பட்டது",
        status_delivered: "சேர்க்கப்பட்டது", status_cancelled: "ரத்து செய்யப்பட்டது",
        accept: "ஏற்கவும்", decline: "நிராகரிக்கவும்", chat: "அரட்டை", cancel_order: "ரத்து செய்",
        new_listing_title: "புதிய பயிர் பட்டியல்", edit_listing_title: "பயிர் பட்டியல் திருத்து",
        save: "சேமிக்கவும்", cancel: "ரத்து",
        request_order_title: "புதிய பயிரை ஆர்டர் செய்யவும்",
        request_qty: "ஆர்டர் அளவு (கிலோ)", delivery_address: "டெலிவரி முகவரி",
        order_notes: "டெலிவரி குறிப்புகள்", submit_order_btn: "ஆர்டரை உறுதிப்படுத்துக",
        available_stock: "கிடைக்கும் இருப்பு",
        ai_forecast_config: "தேவை கணிப்பு", forecast_horizon: "கணிப்பு காலம்",
        run_forecast_btn: "AI கணிப்பை இயக்குக", ai_forecast_prompt: "பயிரைத் தேர்வுசெய்து கணிப்பைக் காண்க.",
        logistics_title: "ஸ்மார்ட் தளவாடங்கள் & வழி உகப்பாக்கம்",
        logistics_desc: "2-Opt வழித்தட உகப்பாக்கம் மூலம் எரிபொருள் செலவு மிச்சமாகிறது.",
        auto_import_orders: "ஏற்றுக்கொண்ட ஆர்டர்களை சேர்க்க",
        optimize_route_btn: "பாதையை உகப்பாக்குக",
        route_prompt: "பாதையை உருவாக்க டெலிவரி நிறுத்தங்களை சேர்க்கவும்.",
        active_trips_title: "செயலில் உள்ள பயணங்கள்",
        fair_price_title: "நியாயமான விலை & இடைத்தரகர் ஒழிப்பு",
        fair_price_desc: "விவசாயிகள் மற்றும் வாங்குபவர்கள் பெறும் உண்மையான பயனைப் பாருங்கள்.",
        type_message: "செய்தி தட்டச்சு செய்க...", send: "அனுப்புக",
        select_buyer: "வாங்குபவர் உரையாடல்கள்:", loading: "ஏற்றுகிறது...",
        you: "நீங்கள்"
      }
    };

    let currentLang = localStorage.getItem("cc_lang") || "en";
    let currentUser = JSON.parse(localStorage.getItem("cc_user") || "null");
    let currentActiveTab = "marketplace";

    // Chat state
    let activeChatListing = null;
    let activeChatPartnerPhone = null;
    let activeChatPartnerName = null;
    let chatPollTimer = null;
    let syncPollTimer = null;

    // Cache
    window._lastListings = [];
    window._lastOrders = [];

    // Helper: Lucide Icon Refresher
    function refreshIcons() {
      if (window.lucide && typeof window.lucide.createIcons === "function") {
        window.lucide.createIcons();
      }
    }

    // Helper: Toast Notifications
    function showToast(title, message, type = "success") {
      const container = document.getElementById("toastContainer");
      if (!container) return;

      const toast = document.createElement("div");
      toast.className = `custom-toast ${type === 'error' ? 'custom-toast-error' : (type === 'info' ? 'custom-toast-info' : '')}`;
      
      let iconName = "check-circle-2";
      let iconColor = "text-success";
      if (type === "error") { iconName = "alert-circle"; iconColor = "text-danger"; }
      if (type === "info") { iconName = "info"; iconColor = "text-primary"; }

      toast.innerHTML = `
        <i data-lucide="${iconName}" class="icon-sm ${iconColor} flex-shrink-0 mt-0.5"></i>
        <div class="flex-grow-1">
          <strong class="d-block text-dark small mb-0.5">${esc(title)}</strong>
          <span class="text-muted small">${esc(message)}</span>
        </div>
        <button type="button" class="btn-close btn-close-sm" style="font-size: 0.65rem;" onclick="this.closest('.custom-toast').remove()"></button>
      `;

      container.appendChild(toast);
      refreshIcons();

      setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(100%)";
        setTimeout(() => toast.remove(), 250);
      }, 3500);
    }

    // Quick-Fill Demo Auth Helper
    function quickFillAuth(phone, password, role) {
      document.getElementById("loginPhone").value = phone;
      document.getElementById("loginPassword").value = password;
      document.getElementById("loginRole").value = role;
      showToast("Demo Credentials Loaded", `Ready to sign in as ${role}`, "info");
    }

    // Helper: Styled Crop Visual Badges (Lucide React Icons with tailored backgrounds)
    function getCropVisual(name) {
      const n = (name || "").toUpperCase();
      if (n.includes("TOMATO")) {
        return { icon: "apple", colorClass: "crop-avatar-rose", label: "Tomato" };
      }
      if (n.includes("ONION")) {
        return { icon: "circle-dot", colorClass: "crop-avatar-purple", label: "Onion" };
      }
      if (n.includes("POTATO")) {
        return { icon: "package", colorClass: "crop-avatar-amber", label: "Potato" };
      }
      if (n.includes("CHILLI") || n.includes("CHILI")) {
        return { icon: "flame", colorClass: "crop-avatar-red", label: "Chilli" };
      }
      if (n.includes("BANANA") || n.includes("MANGO")) {
        return { icon: "citrus", colorClass: "crop-avatar-yellow", label: "Fruit" };
      }
      if (n.includes("CABBAGE") || n.includes("GREENS") || n.includes("SPINACH")) {
        return { icon: "leaf", colorClass: "crop-avatar-green", label: "Greens" };
      }
      if (n.includes("CARROT")) {
        return { icon: "carrot", colorClass: "crop-avatar-amber", label: "Root" };
      }
      if (n.includes("CAPSICUM") || n.includes("PEPPER")) {
        return { icon: "shield", colorClass: "crop-avatar-emerald", label: "Capsicum" };
      }
      if (n.includes("RICE") || n.includes("PADDY") || n.includes("WHEAT")) {
        return { icon: "wheat", colorClass: "crop-avatar-gold", label: "Grain" };
      }
      return { icon: "sprout", colorClass: "crop-avatar-default", label: "Farm Produce" };
    }

    function setLang(lang) {
      currentLang = lang;
      localStorage.setItem("cc_lang", lang);
      document.documentElement.lang = lang;
      applyTranslations();
    }

    function t(key) {
      return (I18N[currentLang] && I18N[currentLang][key]) || (I18N.en && I18N.en[key]) || key;
    }

    function esc(s) {
      return String(s == null ? "" : s).replace(/[&<>"']/g, c =>
        ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    }

    function applyTranslations() {
      const labels = { en: "English", hi: "हिन्दी", te: "తెలుగు", ta: "தமிழ்" };
      document.getElementById("langLabel").textContent = labels[currentLang] || "English";

      document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        const attr = el.getAttribute("data-i18n-attr");
        const value = t(key);
        if (attr) el.setAttribute(attr, value);
        else el.textContent = value;
      });

      renderBuyerListings(window._lastListings || []);
      if (window._lastOrders && window._lastOrders.length) {
        renderOrdersTable(window._lastOrders);
      }
      refreshIcons();
    }

    function switchTab(tabId) {
      currentActiveTab = tabId;
      document.querySelectorAll(".tab-pane-view").forEach(el => el.classList.add("d-none"));
      document.querySelectorAll("#mainAppTabs .nav-link").forEach(el => el.classList.remove("active"));

      const viewEl = document.getElementById(`view-${tabId}`);
      const tabEl = document.getElementById(`tab-${tabId}`);
      if (viewEl) viewEl.classList.remove("d-none");
      if (tabEl) tabEl.classList.add("active");

      if (tabId === "marketplace") fetchListings();
      if (tabId === "orders") fetchOrdersData();
      if (tabId === "ai") runAIDemandForecast();
      if (tabId === "logistics") fetchTripsData();
      if (tabId === "analytics") fetchValueDistribution(document.getElementById("valueCropSelect").value);

      refreshIcons();
    }

    function filterByChip(crop, chipEl) {
      document.querySelectorAll(".chip-filter").forEach(c => c.classList.remove("active"));
      if (chipEl) chipEl.classList.add("active");
      document.getElementById("searchInput").value = crop;
      fetchListings();
    }

    function updateNavUserState() {
      const authBtns = document.getElementById("navAuthBtns");
      const userArea = document.getElementById("navUserArea");
      const sellerBox = document.getElementById("sellerDashboardBox");
      const addBtn = document.getElementById("farmerAddListingBtn");
      const autoDispatchBtn = document.getElementById("orderAutoDispatchBtn");

      if (!currentUser) {
        authBtns.classList.remove("d-none");
        authBtns.classList.add("d-flex");
        userArea.classList.add("d-none");
        userArea.classList.remove("d-flex");
        sellerBox.classList.add("d-none");
        addBtn.classList.add("d-none");
        autoDispatchBtn.classList.add("d-none");
        refreshIcons();
        return;
      }

      authBtns.classList.add("d-none");
      authBtns.classList.remove("d-flex");
      userArea.classList.remove("d-none");
      userArea.classList.add("d-flex");

      document.getElementById("navUserName").textContent = currentUser.name;
      const badgeEl = document.getElementById("navUserBadge");
      
      const role = (currentUser.role || "").toUpperCase();
      if (role === "FARMER") {
        badgeEl.innerHTML = `<i data-lucide="sprout" class="icon-xs me-1"></i> Farmer`;
        badgeEl.className = "badge bg-success-subtle text-success border border-success-subtle px-2.5 py-1.5 rounded-pill d-inline-flex align-items-center";
        sellerBox.classList.remove("d-none");
        addBtn.classList.remove("d-none");
        autoDispatchBtn.classList.remove("d-none");
      } else if (role === "FPO") {
        badgeEl.innerHTML = `<i data-lucide="users" class="icon-xs me-1"></i> FPO Collective`;
        badgeEl.className = "badge bg-primary-subtle text-primary border border-primary-subtle px-2.5 py-1.5 rounded-pill d-inline-flex align-items-center";
        sellerBox.classList.remove("d-none");
        addBtn.classList.remove("d-none");
        autoDispatchBtn.classList.remove("d-none");
      } else if (role === "BULK_BUYER") {
        badgeEl.innerHTML = `<i data-lucide="building-2" class="icon-xs me-1"></i> Bulk Buyer`;
        badgeEl.className = "badge bg-warning-subtle text-warning-emphasis border border-warning-subtle px-2.5 py-1.5 rounded-pill d-inline-flex align-items-center";
        sellerBox.classList.add("d-none");
        addBtn.classList.add("d-none");
        autoDispatchBtn.classList.add("d-none");
      } else {
        badgeEl.innerHTML = `<i data-lucide="shopping-cart" class="icon-xs me-1"></i> Consumer`;
        badgeEl.className = "badge bg-info-subtle text-info-emphasis border border-info-subtle px-2.5 py-1.5 rounded-pill d-inline-flex align-items-center";
        sellerBox.classList.add("d-none");
        addBtn.classList.add("d-none");
        autoDispatchBtn.classList.add("d-none");
      }
      refreshIcons();
    }

    function logout() {
      currentUser = null;
      localStorage.removeItem("cc_user");
      stopChatPolling();
      stopSyncPolling();
      updateNavUserState();
      fetchListings();
      showToast("Signed Out", "You have been logged out successfully.", "info");
    }

    function setAuthTab(tab) {
      new bootstrap.Tab(document.querySelector(`#${tab}-tab`)).show();
    }

    // ============ Background Sync Polling ============
    function startSyncPolling() {
      stopSyncPolling();
      syncPollTimer = setInterval(() => {
        if (!currentUser) return;
        if (currentActiveTab === "marketplace") fetchListings(true);
        if (currentActiveTab === "orders") fetchOrdersData(true);
      }, 4000);
    }

    function stopSyncPolling() {
      if (syncPollTimer) {
        clearInterval(syncPollTimer);
        syncPollTimer = null;
      }
    }

    // =========================================================================
    // TAB 1: Marketplace API & Rendering (ALL IN ₹)
    // =========================================================================
    async function fetchListings(isSilent = false) {
      const searchEl = document.getElementById("searchInput");
      const zipEl = document.getElementById("zipInput");
      const sellerTypeEl = document.getElementById("sellerTypeFilter");

      const crop = searchEl ? searchEl.value.trim() : "";
      const zip = zipEl ? zipEl.value.trim() : "";
      const sellerType = sellerTypeEl ? sellerTypeEl.value.trim() : "";

      try {
        const res = await fetch(`/api/listings?crop=${encodeURIComponent(crop)}&zip_code=${encodeURIComponent(zip)}&seller_type=${encodeURIComponent(sellerType)}`);
        if (!res.ok) return;
        const data = await res.json();
        window._lastListings = data;
        renderBuyerListings(data);
      } catch (err) {
        if (!isSilent) console.error("fetchListings error:", err);
      }
    }

    function renderBuyerListings(data) {
      const container = document.getElementById("listingsContainer");
      const noEl = document.getElementById("noListings");
      if (!container) return;
      container.innerHTML = "";

      if (!data || data.length === 0) {
        if (noEl) noEl.classList.remove("d-none");
        refreshIcons();
        return;
      }
      if (noEl) noEl.classList.add("d-none");

      data.forEach(item => {
        const isFPO = (item.seller_type === "FPO");
        const sellerBadgeClass = isFPO ? "role-badge-fpo" : "role-badge-farmer";
        const sellerRoleIcon = isFPO ? "users" : "sprout";
        const sellerTypeTitle = isFPO ? "FPO Collective" : "Verified Farmer";
        const sourceLabel = item.source === "SMS" 
          ? `<span class="badge bg-warning-subtle text-warning-emphasis border border-warning-subtle rounded-pill px-2 py-0.5 d-inline-flex align-items-center gap-1"><i data-lucide="smartphone" class="icon-xs"></i> SMS Listed</span>`
          : `<span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-2 py-0.5 d-inline-flex align-items-center gap-1"><i data-lucide="check-check" class="icon-xs"></i> Web Verified</span>`;
        
        const visual = getCropVisual(item.crop_name);

        const retailBenchmark = item.retail_market_price_per_kg || Math.round(item.price_per_kg * 1.45);
        const savingsAmount = Math.max(0, retailBenchmark - item.price_per_kg);
        const savingsPercent = Math.round((savingsAmount / retailBenchmark) * 100);

        container.innerHTML += `
          <div class="col-md-6 col-lg-4">
            <div class="crop-card p-3">
              <div class="d-flex justify-content-between align-items-start mb-2.5">
                <div class="d-flex align-items-center gap-2.5">
                  <div class="crop-avatar ${visual.colorClass}">
                    <i data-lucide="${visual.icon}" class="icon-lg"></i>
                  </div>
                  <div>
                    <span class="${sellerBadgeClass}">
                      <i data-lucide="${sellerRoleIcon}" class="icon-xs"></i>
                      <span>${sellerTypeTitle}</span>
                    </span>
                    <h5 class="fw-bold text-dark mb-0 mt-1">${esc(item.crop_name)}</h5>
                  </div>
                </div>
                <div class="text-end">
                  <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-2.5 py-1 fw-semibold">
                    ${item.quantity_kg} ${t("kg_left")}
                  </span>
                  <div class="mt-1">${sourceLabel}</div>
                </div>
              </div>

              <!-- Price & Transparent Savings in ₹ -->
              <div class="p-2.5 bg-light rounded-3 mb-3 border">
                <div class="d-flex justify-content-between align-items-baseline">
                  <div>
                    <span class="price-display">₹${item.price_per_kg}</span>
                    <span class="price-unit">/kg</span>
                  </div>
                  <div class="text-end">
                    <span class="savings-badge">
                      <i data-lucide="trending-up" class="icon-xs"></i>
                      <span>Save ~${savingsPercent}%</span>
                    </span>
                  </div>
                </div>
                <div class="d-flex justify-content-between text-muted" style="font-size:0.76rem; margin-top:5px;">
                  <span>${t("market_benchmark")} <del>₹${retailBenchmark}</del></span>
                  <span class="text-success fw-bold">Direct Save ₹${savingsAmount.toFixed(1)}/kg</span>
                </div>
              </div>

              <!-- Farmer / Location Details -->
              <div class="mb-3 small">
                <div class="text-secondary mb-1.5 d-flex align-items-center gap-1.5">
                  <i data-lucide="user" class="icon-xs text-success"></i>
                  <span>${t("seller")}: <strong class="text-dark">${esc(item.farmer_name)}</strong></span>
                </div>
                <div class="text-secondary mb-1.5 d-flex align-items-center gap-1.5">
                  <i data-lucide="map-pin" class="icon-xs text-danger"></i>
                  <span class="text-truncate">${esc(item.location_name || item.zip_code)} (Pin: ${esc(item.zip_code)})</span>
                </div>
                <div class="text-secondary d-flex align-items-center justify-content-between pt-1 border-top" style="font-size:0.78rem;">
                  <span class="d-flex align-items-center gap-1"><i data-lucide="shield-check" class="icon-xs text-success"></i> ${esc(item.quality_grade || "Grade A Fresh")}</span>
                  <span class="d-flex align-items-center gap-1"><i data-lucide="package" class="icon-xs text-muted"></i> Min: <strong>${item.min_order_kg || 1} KG</strong></span>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="mt-auto d-grid gap-2">
                <div class="d-flex gap-2">
                  <button class="btn btn-sm btn-brand-outline w-50" onclick="openChatForListing(${item.id}, '${esc(item.crop_name)}', '${esc(item.farmer_phone)}', '${esc(item.farmer_name)}')">
                    <i data-lucide="message-square" class="icon-xs"></i>
                    <span>${t("chat_seller")}</span>
                  </button>
                  <button class="btn btn-sm btn-brand w-50" onclick='openOrderModal(${JSON.stringify(item)})'>
                    <i data-lucide="shopping-bag" class="icon-xs"></i>
                    <span>${t("order_now")}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>`;
      });
      refreshIcons();
    }

    // =========================================================================
    // Order Request Modal Handlers (ALL IN ₹)
    // =========================================================================
    function openOrderModal(item) {
      if (!currentUser) {
        showToast("Authentication Required", "Please log in or register first to place an order.", "info");
        setAuthTab("login");
        new bootstrap.Modal(document.getElementById("authModal")).show();
        return;
      }

      document.getElementById("orderListingId").value = item.id;
      document.getElementById("orderPricePerKg").value = item.price_per_kg;
      document.getElementById("orderBulkPricePerKg").value = item.bulk_price_per_kg || item.price_per_kg;
      document.getElementById("orderCropName").textContent = item.crop_name;
      document.getElementById("orderPriceBadge").textContent = `₹${item.price_per_kg}/kg`;
      document.getElementById("orderFarmerName").textContent = item.farmer_name;
      document.getElementById("orderFarmerPhone").textContent = item.farmer_phone;
      document.getElementById("orderAvailableQty").textContent = item.quantity_kg;
      document.getElementById("orderMinQty").textContent = item.min_order_kg || 1;

      const qtyInput = document.getElementById("orderQuantityInput");
      qtyInput.min = item.min_order_kg || 1;
      qtyInput.max = item.quantity_kg;
      qtyInput.value = item.min_order_kg || 5;

      document.getElementById("orderDeliveryAddress").value = currentUser.name ? `${currentUser.name} Address, Pin: ${currentUser.zip_code}` : "Direct Customer Delivery Address";
      document.getElementById("orderNotesInput").value = "";

      updateOrderTotal();
      new bootstrap.Modal(document.getElementById("orderModal")).show();
      refreshIcons();
    }

    function updateOrderTotal() {
      const qty = parseFloat(document.getElementById("orderQuantityInput").value) || 0;
      const basePrice = parseFloat(document.getElementById("orderPricePerKg").value) || 0;
      const bulkPrice = parseFloat(document.getElementById("orderBulkPricePerKg").value) || basePrice;

      const effectivePrice = (qty >= 50 && bulkPrice) ? bulkPrice : basePrice;
      const total = Math.round(qty * effectivePrice);
      document.getElementById("orderTotalPriceEst").textContent = `₹${total}`;

      const retailBench = effectivePrice * 1.45;
      const totalSaved = Math.round(qty * (retailBench - effectivePrice));
      document.getElementById("orderSavingsBadge").textContent = `You save ~₹${totalSaved} vs Retail!`;
    }

    async function handleSubmitOrder(e) {
      e.preventDefault();
      if (!currentUser) return;

      const listing_id = parseInt(document.getElementById("orderListingId").value, 10);
      const quantity_kg = parseFloat(document.getElementById("orderQuantityInput").value);
      const delivery_address = document.getElementById("orderDeliveryAddress").value;
      const delivery_lat = parseFloat(document.getElementById("orderDeliveryLat").value) || 17.4156;
      const delivery_lon = parseFloat(document.getElementById("orderDeliveryLon").value) || 78.4350;
      const notes = document.getElementById("orderNotesInput").value;

      try {
        const res = await fetch("/api/order", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            listing_id,
            buyer_phone: currentUser.phone,
            quantity_kg,
            delivery_address,
            delivery_lat,
            delivery_lon,
            notes
          })
        });

        const data = await res.json();
        if (res.ok) {
          bootstrap.Modal.getInstance(document.getElementById("orderModal")).hide();
          showToast("Order Placed Successfully", data.message || "Your harvest order has been received by the producer.", "success");
          fetchListings();
          switchTab("orders");
        } else {
          showToast("Order Error", data.detail || "Could not place order", "error");
        }
      } catch (err) {
        console.error("Order submit error:", err);
        showToast("Error", "Network error while placing order", "error");
      }
    }

    // =========================================================================
    // TAB 2: Orders API & Table Rendering (ALL IN ₹)
    // =========================================================================
    async function fetchOrdersData(isSilent = false) {
      if (!currentUser) {
        document.getElementById("ordersTableContainer").innerHTML = `
          <div class="text-center py-5 text-muted">
            <div class="p-3 bg-light rounded-circle d-inline-flex mb-2">
              <i data-lucide="shield" class="icon-xl text-warning"></i>
            </div>
            <h5 class="fw-bold text-dark mb-1">Authentication Required</h5>
            <p class="text-muted small mb-3">Please log in to view and manage your orders and batch requests.</p>
            <button class="btn btn-brand btn-sm fw-semibold rounded-pill px-4" data-bs-toggle="modal" data-bs-target="#authModal" onclick="setAuthTab('login')">
              <i data-lucide="log-in" class="icon-xs me-1"></i> Log In Now
            </button>
          </div>`;
        refreshIcons();
        return;
      }

      const isSellerRole = (currentUser.role === "FARMER" || currentUser.role === "FPO");
      const url = isSellerRole 
        ? `/api/farmer/orders?farmer_phone=${encodeURIComponent(currentUser.phone)}`
        : `/api/buyer/orders?buyer_phone=${encodeURIComponent(currentUser.phone)}`;

      try {
        const res = await fetch(url);
        if (!res.ok) return;
        const orders = await res.json();
        window._lastOrders = orders;
        renderOrdersTable(orders);
      } catch (err) {
        if (!isSilent) console.error("fetchOrdersData error:", err);
      }
    }

    function renderOrdersTable(orders) {
      const container = document.getElementById("ordersTableContainer");
      const badge = document.getElementById("tabOrdersBadge");
      const isSellerRole = currentUser && (currentUser.role === "FARMER" || currentUser.role === "FPO");

      const pendingCount = (orders || []).filter(o => o.status === "PENDING").length;
      if (pendingCount > 0) {
        badge.textContent = pendingCount;
        badge.classList.remove("d-none");
      } else {
        badge.classList.add("d-none");
      }

      if (!orders || orders.length === 0) {
        container.innerHTML = `
          <div class="text-center py-5 text-muted">
            <div class="p-3 bg-light rounded-circle d-inline-flex mb-2">
              <i data-lucide="inbox" class="icon-xl text-muted"></i>
            </div>
            <p class="mb-0">No orders recorded yet.</p>
          </div>`;
        refreshIcons();
        return;
      }

      container.innerHTML = `
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th scope="col"># Order</th>
                <th scope="col">${t("crop_name")}</th>
                <th scope="col">${isSellerRole ? "Buyer / Destination" : "Farmer / FPO"}</th>
                <th scope="col">${t("quantity_kg")}</th>
                <th scope="col">${t("total_price")}</th>
                <th scope="col">${t("status")}</th>
                <th scope="col" class="text-end">${t("actions")}</th>
              </tr>
            </thead>
            <tbody>
              ${orders.map(o => {
                let statusBadge = "";
                if (o.status === "PENDING") statusBadge = `<span class="badge bg-warning-subtle text-warning-emphasis border border-warning-subtle rounded-pill px-2.5 py-1 d-inline-flex align-items-center gap-1"><i data-lucide="clock" class="icon-xs"></i> Pending</span>`;
                else if (o.status === "ACCEPTED") statusBadge = `<span class="badge bg-primary-subtle text-primary border border-primary-subtle rounded-pill px-2.5 py-1 d-inline-flex align-items-center gap-1"><i data-lucide="check-circle-2" class="icon-xs"></i> Accepted</span>`;
                else if (o.status === "DISPATCHED") statusBadge = `<span class="badge bg-info-subtle text-info-emphasis border border-info-subtle rounded-pill px-2.5 py-1 d-inline-flex align-items-center gap-1"><i data-lucide="truck" class="icon-xs"></i> Dispatched</span>`;
                else if (o.status === "DELIVERED") statusBadge = `<span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-2.5 py-1 d-inline-flex align-items-center gap-1"><i data-lucide="shield-check" class="icon-xs"></i> Delivered</span>`;
                else if (o.status === "REJECTED") statusBadge = `<span class="badge bg-danger-subtle text-danger border border-danger-subtle rounded-pill px-2.5 py-1 d-inline-flex align-items-center gap-1"><i data-lucide="x-circle" class="icon-xs"></i> Declined</span>`;
                else statusBadge = `<span class="badge bg-secondary-subtle text-secondary border rounded-pill px-2.5 py-1">Cancelled</span>`;

                const buyerOrSellerInfo = isSellerRole ? `
                  <div>
                    <strong>${esc(o.buyer_name)}</strong>
                    <small class="badge bg-light text-dark border ms-1">${esc(o.buyer_role || "Consumer")}</small>
                    <div class="text-muted" style="font-size:0.75rem;">${esc(o.delivery_address || o.delivery_zip)}</div>
                  </div>` : `
                  <div>
                    <strong>${esc(o.farmer_name)}</strong>
                    <div class="text-muted" style="font-size:0.75rem;">${esc(o.farmer_phone)}</div>
                  </div>`;

                let actions = "";
                if (isSellerRole) {
                  if (o.status === "PENDING") {
                    actions = `
                      <div class="btn-group btn-group-sm">
                        <button class="btn btn-success fw-semibold d-inline-flex align-items-center gap-1" onclick="handleAcceptOrder(${o.id})">
                          <i data-lucide="check" class="icon-xs"></i> Accept
                        </button>
                        <button class="btn btn-outline-danger" onclick="handleRejectOrder(${o.id})" title="Decline">
                          <i data-lucide="x" class="icon-xs"></i>
                        </button>
                        <button class="btn btn-outline-primary" onclick="openChatForListing(${o.listing_id}, '${esc(o.crop_name)}', '${esc(o.buyer_phone)}', '${esc(o.buyer_name)}')" title="Chat">
                          <i data-lucide="message-square" class="icon-xs"></i>
                        </button>
                      </div>`;
                  } else if (o.status === "ACCEPTED") {
                    actions = `
                      <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary d-inline-flex align-items-center gap-1" onclick="loadSingleOrderToRoute(${JSON.stringify(o).replace(/"/g, '&quot;')})">
                          <i data-lucide="truck" class="icon-xs"></i> Route
                        </button>
                        <button class="btn btn-outline-success" onclick="openChatForListing(${o.listing_id}, '${esc(o.crop_name)}', '${esc(o.buyer_phone)}', '${esc(o.buyer_name)}')" title="Chat">
                          <i data-lucide="message-square" class="icon-xs"></i>
                        </button>
                      </div>`;
                  } else {
                    actions = `
                      <button class="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-1" onclick="openChatForListing(${o.listing_id}, '${esc(o.crop_name)}', '${esc(o.buyer_phone)}', '${esc(o.buyer_name)}')">
                        <i data-lucide="message-square" class="icon-xs"></i> Chat
                      </button>`;
                  }
                } else {
                  if (o.status === "PENDING") {
                    actions = `
                      <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-danger" onclick="handleCancelOrder(${o.id})">
                          Cancel
                        </button>
                        <button class="btn btn-outline-success d-inline-flex align-items-center gap-1" onclick="openChatForListing(${o.listing_id}, '${esc(o.crop_name)}', '${esc(o.farmer_phone)}', '${esc(o.farmer_name)}')">
                          <i data-lucide="message-square" class="icon-xs"></i> Chat
                        </button>
                      </div>`;
                  } else {
                    actions = `
                      <button class="btn btn-sm btn-outline-success d-inline-flex align-items-center gap-1" onclick="openChatForListing(${o.listing_id}, '${esc(o.crop_name)}', '${esc(o.farmer_phone)}', '${esc(o.farmer_name)}')">
                        <i data-lucide="message-square" class="icon-xs"></i> Chat
                      </button>`;
                  }
                }

                return `
                  <tr>
                    <td><strong class="text-secondary">#${o.id}</strong></td>
                    <td><strong class="text-success">${esc(o.crop_name)}</strong></td>
                    <td>${buyerOrSellerInfo}</td>
                    <td><strong>${o.quantity_kg} KG</strong></td>
                    <td><strong>₹${o.total_price}</strong> <small class="text-muted">(@ ₹${o.price_per_kg}/kg)</small></td>
                    <td>${statusBadge}</td>
                    <td class="text-end">${actions}</td>
                  </tr>`;
              }).join("")}
            </tbody>
          </table>
        </div>`;
      refreshIcons();
    }

    async function handleAcceptOrder(orderId) {
      if (!confirm("Accept this batch request? Inventory will be allocated and scheduled for logistics dispatch.")) return;
      try {
        const res = await fetch(`/api/orders/${orderId}/accept?farmer_phone=${encodeURIComponent(currentUser.phone)}`, { method: "POST" });
        const data = await res.json();
        if (res.ok) {
          showToast("Order Accepted", data.message || "Batch request accepted and ready for dispatch.", "success");
          fetchOrdersData();
          fetchListings();
        } else {
          showToast("Error", data.detail || "Error accepting order", "error");
        }
      } catch (err) {
        console.error("Accept error:", err);
      }
    }

    async function handleRejectOrder(orderId) {
      if (!confirm("Decline this batch request?")) return;
      try {
        const res = await fetch(`/api/orders/${orderId}/reject?farmer_phone=${encodeURIComponent(currentUser.phone)}`, { method: "POST" });
        const data = await res.json();
        if (res.ok) {
          showToast("Order Declined", data.message || "Batch request declined.", "info");
          fetchOrdersData();
        } else {
          showToast("Error", data.detail || "Error declining order", "error");
        }
      } catch (err) {
        console.error("Reject error:", err);
      }
    }

    async function handleCancelOrder(orderId) {
      if (!confirm("Cancel this order request?")) return;
      try {
        const res = await fetch(`/api/orders/${orderId}/cancel?buyer_phone=${encodeURIComponent(currentUser.phone)}`, { method: "POST" });
        const data = await res.json();
        if (res.ok) {
          showToast("Order Cancelled", data.message || "Order request cancelled.", "info");
          fetchOrdersData();
          fetchListings();
        } else {
          showToast("Error", data.detail || "Error cancelling order", "error");
        }
      } catch (err) {
        console.error("Cancel error:", err);
      }
    }

    // =========================================================================
    // TAB 3: AI Demand Forecasting (ALL IN ₹)
    // =========================================================================
    function syncForecastCropInput(val) {
      document.getElementById("forecastCropInput").value = val;
    }

    async function runAIDemandForecast() {
      const crop = (document.getElementById("forecastCropInput").value || "TOMATO").trim();
      const days = document.getElementById("forecastDaysSelect").value || "7";
      const card = document.getElementById("forecastResultsCard");

      card.innerHTML = `<div class="text-center py-5 text-muted"><span class="spinner-border spinner-border-sm me-2 text-success"></span>Analyzing multi-factor demand trends...</div>`;

      try {
        const res = await fetch(`/api/ai/demand-forecast?crop=${encodeURIComponent(crop)}&days=${encodeURIComponent(days)}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Forecast calculation error");

        const isRising = data.trend === "rising";
        const isFalling = data.trend === "falling";
        const trendBadge = isRising ? "bg-success-subtle text-success border border-success-subtle" : (isFalling ? "bg-danger-subtle text-danger border border-danger-subtle" : "bg-primary-subtle text-primary border border-primary-subtle");
        const trendIcon = isRising ? "trending-up" : (isFalling ? "trending-down" : "minus");

        const maxVal = Math.max(...data.daily_projection.map(d => d.demand_kg), 10);
        const barsHtml = data.daily_projection.map((d, i) => {
          const heightPct = Math.round((d.demand_kg / maxVal) * 100);
          return `
            <div class="d-flex flex-column align-items-center flex-fill" style="min-width:44px;">
              <span class="small fw-bold text-success mb-1" style="font-size:0.72rem;">${d.demand_kg}kg</span>
              <div class="w-100 bg-success bg-opacity-75 rounded-top" style="height:${heightPct}px; min-height:10px;"></div>
              <span class="text-muted text-truncate mt-1.5" style="font-size:0.68rem;">${d.day.split(" ")[0]}</span>
            </div>`;
        }).join("");

        card.innerHTML = `
          <div class="d-flex justify-content-between align-items-start mb-3">
            <div>
              <span class="badge ${trendBadge} rounded-pill px-3 py-1 mb-1 d-inline-flex align-items-center gap-1">
                <i data-lucide="${trendIcon}" class="icon-xs"></i>
                <span>Trend: ${esc(data.trend.toUpperCase())}</span>
              </span>
              <h4 class="fw-bold text-success mb-0">${esc(data.crop)} AI Demand Forecast (${data.forecast_days} Days)</h4>
            </div>
            <div class="text-end">
              <span class="badge bg-light text-dark border px-2.5 py-1.5 rounded-pill small">
                Confidence: <strong>${data.confidence_percent}%</strong>
              </span>
            </div>
          </div>

          <div class="row g-3 mb-4">
            <div class="col-md-3 col-6">
              <div class="metric-card">
                <small class="text-muted d-block">Projected Demand</small>
                <h5 class="fw-bold text-dark mb-0">${data.forecast_total_kg} KG</h5>
                <small class="text-muted">~${data.forecast_daily_kg} kg/day</small>
              </div>
            </div>
            <div class="col-md-3 col-6">
              <div class="metric-card">
                <small class="text-muted d-block">Current Supply</small>
                <h5 class="fw-bold text-dark mb-0">${data.current_supply_kg} KG</h5>
                <small class="text-muted">Active in Portal</small>
              </div>
            </div>
            <div class="col-md-3 col-6">
              <div class="metric-card">
                <small class="text-muted d-block">Supply Gap</small>
                <h5 class="fw-bold ${data.supply_gap_kg > 0 ? 'text-danger' : 'text-success'} mb-0">
                  ${data.supply_gap_kg > 0 ? '+' + data.supply_gap_kg : data.supply_gap_kg} KG
                </h5>
                <small class="text-muted">${data.supply_gap_kg > 0 ? 'Deficit' : 'Surplus'}</small>
              </div>
            </div>
            <div class="col-md-3 col-6">
              <div class="metric-card">
                <small class="text-muted d-block">Target Stocking</small>
                <h5 class="fw-bold text-primary mb-0">${data.recommended_stock_kg} KG</h5>
                <small class="text-muted">+15% safety buffer</small>
              </div>
            </div>
          </div>

          <div class="p-3 bg-light rounded-4 mb-4 border">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h6 class="fw-bold text-dark small mb-0 d-flex align-items-center gap-1.5">
                <i data-lucide="bar-chart-3" class="icon-xs text-success"></i>Daily Projected Consumption (KG)
              </h6>
              <span class="badge bg-white text-muted border small">Shelf Life: ${data.shelf_life_days} Days</span>
            </div>
            <div class="d-flex align-items-end gap-2 pt-3 pb-1" style="height:140px; overflow-x:auto;">
              ${barsHtml}
            </div>
          </div>

          <!-- Price Recommendation in ₹ -->
          <div class="row g-3 mb-3">
            <div class="col-md-6">
              <div class="p-3 bg-success bg-opacity-10 border border-success border-opacity-25 rounded-4">
                <h6 class="fw-bold text-success mb-1 d-flex align-items-center gap-1.5">
                  <i data-lucide="coins" class="icon-sm"></i>Recommended Farmer Price
                </h6>
                <div class="fs-4 fw-bold text-success">₹${data.fair_farmer_price_inr} / KG</div>
                <small class="text-muted">Mandi Baseline: <del>₹${data.mandi_benchmark_inr}</del> (Farmer earns <strong>+45% more</strong>)</small>
              </div>
            </div>
            <div class="col-md-6">
              <div class="p-3 bg-primary bg-opacity-10 border border-primary border-opacity-25 rounded-4">
                <h6 class="fw-bold text-primary mb-1 d-flex align-items-center gap-1.5">
                  <i data-lucide="shopping-bag" class="icon-sm"></i>Target Direct Consumer Price
                </h6>
                <div class="fs-4 fw-bold text-primary">₹${data.fair_consumer_price_inr} / KG</div>
                <small class="text-muted">Retail Supermarket: <del>₹${data.retail_benchmark_inr}</del> (Consumer saves <strong>25%</strong>)</small>
              </div>
            </div>
          </div>

          <div class="alert alert-success d-flex align-items-center mb-0 rounded-4">
            <i data-lucide="lightbulb" class="icon-md text-success me-3 flex-shrink-0"></i>
            <div>
              <strong class="d-block mb-0.5">AI Recommendation:</strong>
              <span class="small">${esc(data.recommendation)}</span>
            </div>
          </div>`;
        refreshIcons();
      } catch (err) {
        card.innerHTML = `<div class="alert alert-danger mb-0">${esc(err.message)}</div>`;
      }
    }

    // =========================================================================
    // TAB 4: Smart Logistics & 2-Opt Optimizer (ALL IN ₹)
    // =========================================================================
    let lastOptimizedData = null;

    function autoLoadOrdersToLogistics() {
      switchTab("logistics");
      const acceptedOrders = (window._lastOrders || []).filter(o => o.status === "ACCEPTED");
      if (acceptedOrders.length === 0) {
        showToast("No Orders Available", "Accept pending orders first to load them into the delivery route.", "info");
        return;
      }

      const stopsLines = acceptedOrders.map(o => {
        const name = o.buyer_name || `Buyer #${o.id}`;
        const lat = o.delivery_lat || 17.4156;
        const lon = o.delivery_lon || 78.4350;
        const kg = o.quantity_kg || 10;
        const addr = (o.delivery_address || `Order #${o.id}`).replace(/,/g, ' ');
        return `${name}, ${lat}, ${lon}, ${kg}, ${addr}`;
      });

      document.getElementById("routeStops").value = stopsLines.join("\n");
      runRouteOptimizer();
    }

    function loadSingleOrderToRoute(order) {
      switchTab("logistics");
      const name = order.buyer_name || `Buyer #${order.id}`;
      const lat = order.delivery_lat || 17.4156;
      const lon = order.delivery_lon || 78.4350;
      const kg = order.quantity_kg || 10;
      const addr = (order.delivery_address || `Order #${order.id}`).replace(/,/g, ' ');
      document.getElementById("routeStops").value = `${name}, ${lat}, ${lon}, ${kg}, ${addr}`;
      runRouteOptimizer();
    }

    function parseRouteStopsText() {
      const lines = document.getElementById("routeStops").value.split(/\r?\n/).map(x => x.trim()).filter(Boolean);
      const stops = [];
      for (const line of lines) {
        const parts = line.split(",").map(x => x.trim());
        if (parts.length < 4) throw new Error(`Invalid stop line: "${line}". Format: Name, Lat, Lon, KG, [Address]`);
        const lat = Number(parts[1]);
        const lon = Number(parts[2]);
        const kg = Number(parts[3]);
        const addr = parts.slice(4).join(", ") || "Delivery Destination";
        if (!Number.isFinite(lat) || !Number.isFinite(lon) || !Number.isFinite(kg) || kg < 0) {
          throw new Error(`Invalid numeric coordinates or weight in: "${line}"`);
        }
        stops.push({ name: parts[0], lat, lon, quantity_kg: kg, address: addr });
      }
      return stops;
    }

    async function runRouteOptimizer() {
      const resultBox = document.getElementById("routeResultsBox");
      try {
        const stops = parseRouteStopsText();
        const originName = document.getElementById("originName").value;
        const originLat = Number(document.getElementById("originLat").value);
        const originLon = Number(document.getElementById("originLon").value);
        const capacity = Number(document.getElementById("vehicleCapacity").value);

        resultBox.innerHTML = `<div class="text-center py-5 text-muted"><span class="spinner-border spinner-border-sm me-2 text-success"></span>Running 2-Opt trajectory optimization...</div>`;

        const res = await fetch("/api/logistics/optimize", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            origin_name: originName,
            origin_lat: originLat,
            origin_lon: originLon,
            stops,
            vehicle_capacity_kg: capacity
          })
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Route optimization error");
        lastOptimizedData = data;

        const isSellerRole = currentUser && (currentUser.role === "FARMER" || currentUser.role === "FPO");

        resultBox.innerHTML = `
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <span class="badge bg-success rounded-pill px-3 py-1 mb-1 d-inline-flex align-items-center gap-1">
                <i data-lucide="zap" class="icon-xs"></i>2-Opt Optimized Sequence
              </span>
              <h5 class="fw-bold text-dark mb-0">Delivery Route Summary</h5>
            </div>
            ${isSellerRole ? `<button class="btn btn-brand btn-sm rounded-pill px-3 fw-semibold d-inline-flex align-items-center gap-1" onclick="handleDispatchTripSubmit()"><i data-lucide="send" class="icon-xs"></i> Create &amp; Dispatch Trip</button>` : ''}
          </div>

          <div class="row g-2 mb-3">
            <div class="col-4">
              <div class="p-2 bg-white rounded-3 border text-center">
                <small class="text-muted d-block">Total Route</small>
                <strong>${data.total_distance_km} km</strong>
                <small class="text-success d-block" style="font-size:0.7rem;">-${data.distance_saved_km} km saved</small>
              </div>
            </div>
            <div class="col-4">
              <div class="p-2 bg-white rounded-3 border text-center">
                <small class="text-muted d-block">Est. Travel Time</small>
                <strong>${data.estimated_travel_minutes} mins</strong>
                <small class="text-muted d-block" style="font-size:0.7rem;">(${data.estimated_travel_hours} hrs)</small>
              </div>
            </div>
            <div class="col-4">
              <div class="p-2 bg-white rounded-3 border text-center">
                <small class="text-muted d-block">Load Utilization</small>
                <strong>${data.load_utilization_percent}%</strong>
                <small class="text-muted d-block" style="font-size:0.7rem;">${data.total_load_kg}/${data.vehicle_capacity_kg} kg</small>
              </div>
            </div>
          </div>

          <div class="alert alert-success py-2.5 px-3 small mb-3 rounded-3">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center gap-1"><i data-lucide="truck" class="icon-sm"></i><strong>Recommended Vehicle:</strong> ${esc(data.recommended_vehicle)}</div>
              <div><span class="badge bg-success-subtle text-success">Est. Fuel: ₹${data.estimated_fuel_cost_inr}</span></div>
            </div>
            <div class="text-muted mt-1.5 d-flex align-items-start gap-1" style="font-size:0.76rem;">
              <i data-lucide="leaf" class="icon-xs text-success flex-shrink-0 mt-0.5"></i>
              <span><strong>Green Impact:</strong> Consolidated routing saves <strong>${data.co2_saved_kg} KG of CO2</strong> and ₹${data.cost_savings_inr} in direct transport expenses.</span>
            </div>
          </div>

          <h6 class="fw-bold text-dark small mb-2 d-flex align-items-center gap-1.5">
            <i data-lucide="milestone" class="icon-xs text-success"></i>Optimized Drop Sequence:
          </h6>
          <div class="d-flex flex-column gap-2" style="max-height: 250px; overflow-y:auto;">
            <div class="p-2.5 bg-white rounded-3 border-start border-success border-4 shadow-sm">
              <strong class="text-success d-flex align-items-center gap-1.5">
                <i data-lucide="map-pin" class="icon-sm"></i> Origin Hub: ${esc(data.origin.name)}
              </strong>
              <small class="text-muted d-block">Coordinates: [${data.origin.lat}, ${data.origin.lon}]</small>
            </div>
            ${data.route.map(stop => `
              <div class="p-2.5 bg-white rounded-3 border shadow-sm">
                <div class="d-flex justify-content-between align-items-center mb-1">
                  <strong>${stop.sequence}. ${esc(stop.name)}</strong>
                  <span class="badge bg-success-subtle text-success rounded-pill">${stop.quantity_kg} KG</span>
                </div>
                <div class="text-muted small d-flex align-items-center gap-2" style="font-size:0.78rem;">
                  <span><i data-lucide="map-pin" class="icon-xs me-0.5"></i>${esc(stop.address)}</span>
                  <span>&bull;</span>
                  <span><i data-lucide="arrow-right" class="icon-xs text-primary me-0.5"></i>${stop.distance_from_previous_km} km from previous stop</span>
                </div>
              </div>
            `).join("")}
          </div>`;
        refreshIcons();
      } catch (err) {
        resultBox.innerHTML = `<div class="alert alert-danger mb-0">${esc(err.message)}</div>`;
      }
    }

    async function handleDispatchTripSubmit() {
      if (!currentUser || !lastOptimizedData) return;
      if (!confirm("Dispatch this logistics trip? Connected customer orders will be marked DISPATCHED.")) return;

      const acceptedOrderIds = (window._lastOrders || []).filter(o => o.status === "ACCEPTED").map(o => o.id);

      try {
        const res = await fetch("/api/logistics/dispatch", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            farmer_phone: currentUser.phone,
            origin_name: lastOptimizedData.origin.name,
            origin_lat: lastOptimizedData.origin.lat,
            origin_lon: lastOptimizedData.origin.lon,
            vehicle_type: lastOptimizedData.recommended_vehicle,
            vehicle_number: "TS-09-UB-8821",
            driver_name: "Raju Logistics Driver",
            driver_phone: "+919876540000",
            stops: lastOptimizedData.route,
            order_ids: acceptedOrderIds,
            total_distance_km: lastOptimizedData.total_distance_km,
            total_load_kg: lastOptimizedData.total_load_kg,
            estimated_travel_minutes: lastOptimizedData.estimated_travel_minutes,
            fuel_cost_est: lastOptimizedData.estimated_fuel_cost_inr,
            co2_saved_kg: lastOptimizedData.co2_saved_kg
          })
        });

        const data = await res.json();
        if (res.ok) {
          showToast("Trip Dispatched", data.message || "Logistics trip dispatched successfully.", "success");
          fetchTripsData();
          fetchOrdersData();
        } else {
          showToast("Error", data.detail || "Dispatch failed", "error");
        }
      } catch (err) {
        console.error("Dispatch error:", err);
      }
    }

    async function fetchTripsData() {
      const container = document.getElementById("tripsListContainer");
      if (!currentUser) {
        container.innerHTML = `<p class="text-muted small">Log in to view active delivery trips.</p>`;
        return;
      }

      try {
        const res = await fetch(`/api/logistics/trips?phone=${encodeURIComponent(currentUser.phone)}`);
        if (!res.ok) return;
        const trips = await res.json();

        if (!trips || trips.length === 0) {
          container.innerHTML = `<p class="text-muted small py-2 mb-0">No active trips dispatched yet.</p>`;
          return;
        }

        const isSellerRole = (currentUser.role === "FARMER" || currentUser.role === "FPO");

        container.innerHTML = `
          <div class="row g-3">
            ${trips.map(tr => `
              <div class="col-md-6">
                <div class="p-3 bg-white rounded-4 border shadow-sm h-100">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="fw-bold text-success">Trip #${tr.id}</span>
                    <span class="badge ${tr.status === 'DELIVERED' ? 'bg-success' : 'bg-primary'} rounded-pill px-3">${tr.status}</span>
                  </div>
                  <div class="small text-secondary mb-2">
                    <div class="d-flex align-items-center gap-1.5"><i data-lucide="truck" class="icon-xs"></i> ${esc(tr.vehicle_type)} (${esc(tr.vehicle_number)})</div>
                    <div class="d-flex align-items-center gap-1.5"><i data-lucide="user-check" class="icon-xs"></i> Driver: ${esc(tr.driver_name)} (${esc(tr.driver_phone)})</div>
                    <div class="d-flex align-items-center gap-1.5"><i data-lucide="gauge" class="icon-xs"></i> ${tr.total_distance_km} km &nbsp;|&nbsp; ${tr.total_load_kg} KG load</div>
                  </div>
                  ${isSellerRole && tr.status !== 'DELIVERED' ? `
                    <button class="btn btn-outline-success btn-sm w-100 fw-semibold rounded-pill d-inline-flex align-items-center justify-content-center gap-1" onclick="handleMarkTripDelivered(${tr.id})">
                      <i data-lucide="check-circle-2" class="icon-xs"></i> Mark Trip &amp; Orders Delivered
                    </button>
                  ` : ''}
                </div>
              </div>
            `).join("")}
          </div>`;
        refreshIcons();
      } catch (err) {
        console.error("fetchTrips error:", err);
      }
    }

    async function handleMarkTripDelivered(tripId) {
      if (!confirm("Confirm all stops have been delivered? Connected customer orders will be marked DELIVERED.")) return;
      try {
        const res = await fetch(`/api/logistics/trips/${tripId}/deliver?phone=${encodeURIComponent(currentUser.phone)}`, { method: "POST" });
        const data = await res.json();
        if (res.ok) {
          showToast("Trip Completed", data.message || "All orders marked delivered.", "success");
          fetchTripsData();
          fetchOrdersData();
        } else {
          showToast("Error", data.detail || "Error updating trip", "error");
        }
      } catch (err) {
        console.error("Mark trip error:", err);
      }
    }

    // =========================================================================
    // TAB 5: Fair Price & Value Chain Transparency (ALL IN ₹)
    // =========================================================================
    async function fetchValueDistribution(crop) {
      const container = document.getElementById("valueDistributionContent");
      container.innerHTML = `<div class="text-center py-5 text-muted"><span class="spinner-border spinner-border-sm me-2 text-success"></span>Loading value distribution breakdown...</div>`;

      try {
        const res = await fetch(`/api/analytics/value-distribution?crop=${encodeURIComponent(crop)}`);
        const data = await res.json();
        if (!res.ok) throw new Error("Could not load value distribution");

        container.innerHTML = `
          <div class="row g-4 mb-4">
            <div class="col-lg-6">
              <div class="p-4 bg-danger bg-opacity-10 rounded-4 border border-danger border-opacity-25 h-100">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-bold text-danger mb-0 d-flex align-items-center gap-2">
                    <i data-lucide="alert-triangle" class="icon-md"></i>Traditional Mandi Chain
                  </h5>
                  <span class="badge bg-danger rounded-pill px-3">High Inefficiency</span>
                </div>
                <p class="text-muted small">Passes through 3-4 intermediaries before reaching consumers, resulting in massive margins lost to middlemen and 25% post-harvest food waste.</p>

                <div class="d-flex flex-column gap-2 mb-3">
                  <div class="p-2.5 bg-white rounded-3 border d-flex justify-content-between align-items-center">
                    <span class="d-flex align-items-center gap-1.5"><i data-lucide="sprout" class="icon-sm text-danger"></i> Farmer Realization</span>
                    <strong class="text-danger">₹${data.traditional_chain.farmer_earns_inr}/KG (42%)</strong>
                  </div>
                  <div class="p-2 bg-white rounded-3 border d-flex justify-content-between text-muted small">
                    <span class="d-flex align-items-center gap-1.5"><i data-lucide="user-x" class="icon-xs"></i> 1. Village Aggregator Margin</span>
                    <span>₹${data.traditional_chain.village_middleman_inr}/KG</span>
                  </div>
                  <div class="p-2 bg-white rounded-3 border d-flex justify-content-between text-muted small">
                    <span class="d-flex align-items-center gap-1.5"><i data-lucide="landmark" class="icon-xs"></i> 2. Mandi Arhatiya Commission</span>
                    <span>₹${data.traditional_chain.mandi_commission_inr}/KG</span>
                  </div>
                  <div class="p-2 bg-white rounded-3 border d-flex justify-content-between text-muted small">
                    <span class="d-flex align-items-center gap-1.5"><i data-lucide="store" class="icon-xs"></i> 3. Wholesaler + Retailer Markup</span>
                    <span>₹${(data.traditional_chain.wholesaler_margin_inr + data.traditional_chain.retailer_margin_inr).toFixed(1)}/KG</span>
                  </div>
                  <div class="p-2.5 bg-white rounded-3 border d-flex justify-content-between align-items-center">
                    <span class="d-flex align-items-center gap-1.5"><i data-lucide="shopping-cart" class="icon-sm text-dark"></i> Consumer Pays</span>
                    <strong class="text-dark">₹${data.traditional_chain.consumer_pays_inr}/KG</strong>
                  </div>
                </div>

                <div class="badge bg-danger bg-opacity-25 text-danger border border-danger p-2.5 w-100 text-start rounded-3 d-flex align-items-start gap-1.5">
                  <i data-lucide="alert-circle" class="icon-xs flex-shrink-0 mt-0.5"></i>
                  <span><strong>Supply Chain Loss:</strong> ~25% perishable spoilage due to delayed multi-hop handling.</span>
                </div>
              </div>
            </div>

            <div class="col-lg-6">
              <div class="p-4 bg-success bg-opacity-10 rounded-4 border border-success border-opacity-25 h-100">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-bold text-success mb-0 d-flex align-items-center gap-2">
                    <i data-lucide="shield-check" class="icon-md"></i>CropConnect Direct Model
                  </h5>
                  <span class="badge bg-success rounded-pill px-3">Direct Linkage</span>
                </div>
                <p class="text-muted small">Connects farmers/FPOs directly with buyers via automated matchmaking and consolidated 2-Opt logistics.</p>

                <div class="d-flex flex-column gap-2 mb-3">
                  <div class="p-2.5 bg-white rounded-3 border d-flex justify-content-between align-items-center">
                    <span class="d-flex align-items-center gap-1.5"><i data-lucide="sprout" class="icon-sm text-success"></i> Farmer Realization</span>
                    <strong class="text-success">₹${data.cropconnect_direct_chain.farmer_earns_inr}/KG (+${data.benefits.farmer_income_increase_percent}%)</strong>
                  </div>
                  <div class="p-2 bg-white rounded-3 border d-flex justify-content-between text-muted small">
                    <span class="d-flex align-items-center gap-1.5"><i data-lucide="truck" class="icon-xs text-primary"></i> Direct Smart Logistics</span>
                    <span>₹${data.cropconnect_direct_chain.direct_logistics_inr}/KG</span>
                  </div>
                  <div class="p-2 bg-white rounded-3 border d-flex justify-content-between text-muted small">
                    <span class="d-flex align-items-center gap-1.5"><i data-lucide="ban" class="icon-xs text-success"></i> Intermediary Middleman Cut</span>
                    <span class="text-success fw-bold">₹0.0 (100% Eliminated)</span>
                  </div>
                  <div class="p-2.5 bg-white rounded-3 border d-flex justify-content-between align-items-center">
                    <span class="d-flex align-items-center gap-1.5"><i data-lucide="shopping-cart" class="icon-sm text-success"></i> Consumer Pays</span>
                    <strong class="text-success">₹${data.cropconnect_direct_chain.consumer_pays_inr}/KG (-${data.benefits.consumer_price_savings_percent}%)</strong>
                  </div>
                </div>

                <div class="badge bg-success bg-opacity-25 text-success border border-success p-2.5 w-100 text-start rounded-3 d-flex align-items-start gap-1.5">
                  <i data-lucide="check-check" class="icon-xs flex-shrink-0 mt-0.5"></i>
                  <span><strong>Direct Freshness:</strong> &lt; 4.5% food loss through farm-to-table optimized routes.</span>
                </div>
              </div>
            </div>
          </div>

          <div class="row g-3">
            <div class="col-md-4">
              <div class="metric-card">
                <div class="p-2 bg-success bg-opacity-10 rounded-circle d-inline-flex mb-2">
                  <i data-lucide="trending-up" class="icon-lg text-success"></i>
                </div>
                <h4 class="fw-bold text-success mb-0">+${data.benefits.farmer_income_increase_percent}%</h4>
                <small class="text-muted">Direct Income Boost for Farmers</small>
              </div>
            </div>
            <div class="col-md-4">
              <div class="metric-card">
                <div class="p-2 bg-primary bg-opacity-10 rounded-circle d-inline-flex mb-2">
                  <i data-lucide="wallet" class="icon-lg text-primary"></i>
                </div>
                <h4 class="fw-bold text-primary mb-0">-${data.benefits.consumer_price_savings_percent}%</h4>
                <small class="text-muted">Price Discount for Consumers</small>
              </div>
            </div>
            <div class="col-md-4">
              <div class="metric-card">
                <div class="p-2 bg-warning bg-opacity-10 rounded-circle d-inline-flex mb-2">
                  <i data-lucide="shield-check" class="icon-lg text-warning"></i>
                </div>
                <h4 class="fw-bold text-warning-emphasis mb-0">${data.benefits.supply_chain_waste_reduction_percent}%</h4>
                <small class="text-muted">Post-Harvest Waste Reduced</small>
              </div>
            </div>
          </div>`;
        refreshIcons();
      } catch (err) {
        container.innerHTML = `<div class="alert alert-danger">${esc(err.message)}</div>`;
      }
    }

    // =========================================================================
    // Listing CRUD Modal Handlers (ALL IN ₹)
    // =========================================================================
    function openCreateListingModal() {
      if (!currentUser || (currentUser.role !== "FARMER" && currentUser.role !== "FPO")) {
        showToast("Authentication Required", "Please register or log in as a Farmer or FPO to add listings.", "info");
        setAuthTab("login");
        new bootstrap.Modal(document.getElementById("authModal")).show();
        return;
      }
      document.getElementById("listingId").value = "";
      document.getElementById("listingCrop").value = "";
      document.getElementById("listingQty").value = "";
      document.getElementById("listingPrice").value = "";
      document.getElementById("listingMinQty").value = "5";
      document.getElementById("listingBulkPrice").value = "";
      document.getElementById("listingZip").value = currentUser.zip_code || "500001";
      document.getElementById("listingShelfLife").value = "7";
      document.getElementById("listingGrade").value = "Grade A - Freshly Harvested";
      document.getElementById("listingModalTitle").textContent = t("new_listing_title");
      new bootstrap.Modal(document.getElementById("listingModal")).show();
      refreshIcons();
    }

    async function handleSaveListing(e) {
      e.preventDefault();
      if (!currentUser) return;

      const id = document.getElementById("listingId").value;
      const crop_name = document.getElementById("listingCrop").value;
      const quantity_kg = parseFloat(document.getElementById("listingQty").value);
      const price_per_kg = parseFloat(document.getElementById("listingPrice").value);
      const min_order_kg = parseFloat(document.getElementById("listingMinQty").value) || 5;
      const bulk_price_per_kg = parseFloat(document.getElementById("listingBulkPrice").value) || null;
      const zip_code = document.getElementById("listingZip").value;
      const shelf_life_days = parseInt(document.getElementById("listingShelfLife").value, 10) || 7;
      const quality_grade = document.getElementById("listingGrade").value;

      try {
        let res;
        if (id) {
          res = await fetch(`/api/listings/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              farmer_phone: currentUser.phone,
              crop_name, quantity_kg, price_per_kg, min_order_kg,
              bulk_price_per_kg, zip_code, shelf_life_days, quality_grade
            })
          });
        } else {
          res = await fetch(`/api/listings`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              farmer_phone: currentUser.phone,
              crop_name, quantity_kg, price_per_kg, min_order_kg,
              bulk_price_per_kg, zip_code, shelf_life_days, quality_grade
            })
          });
        }

        const data = await res.json();
        if (res.ok) {
          bootstrap.Modal.getInstance(document.getElementById("listingModal")).hide();
          showToast("Listing Saved", data.message || "Harvest listing published successfully!", "success");
          fetchListings();
        } else {
          showToast("Error", data.detail || "Error saving listing", "error");
        }
      } catch (err) {
        console.error("Save listing error:", err);
      }
    }

    // =========================================================================
    // Direct Chat Handlers
    // =========================================================================
    function openChatForListing(listingId, cropName, partnerPhone, partnerName) {
      if (!currentUser) {
        showToast("Login Required", "Please log in first to chat with the seller.", "info");
        setAuthTab("login");
        new bootstrap.Modal(document.getElementById("authModal")).show();
        return;
      }

      activeChatListing = { id: listingId, crop_name: cropName };
      activeChatPartnerPhone = partnerPhone;
      activeChatPartnerName = partnerName;

      document.getElementById("chatCropTitle").innerHTML = `<i data-lucide="message-square" class="icon-sm me-1"></i> ${esc(cropName)} - Direct Chat`;
      document.getElementById("chatPartnerTitle").textContent = `${partnerName} (${partnerPhone})`;
      document.getElementById("farmerBuyerBar").classList.add("d-none");
      document.getElementById("chatInputText").value = "";
      document.getElementById("chatInputText").disabled = false;
      document.getElementById("chatSendBtn").disabled = false;

      const modal = new bootstrap.Modal(document.getElementById("chatModal"));
      modal.show();

      fetchChatMessages();
      startChatPolling();
      refreshIcons();
    }

    async function fetchChatMessages() {
      if (!activeChatListing || !currentUser || !activeChatPartnerPhone) return;
      try {
        const url = `/api/listings/${activeChatListing.id}/messages?phone=${encodeURIComponent(currentUser.phone)}&partner_phone=${encodeURIComponent(activeChatPartnerPhone)}`;
        const res = await fetch(url);
        if (!res.ok) return;
        const messages = await res.json();
        renderChatMessages(messages);
      } catch (err) {
        console.error("fetchChatMessages error:", err);
      }
    }

    function renderChatMessages(messages) {
      const container = document.getElementById("chatMessagesList");
      if (!messages || messages.length === 0) {
        container.innerHTML = `<p class="text-muted small text-center my-auto">No messages yet. Start the direct conversation!</p>`;
        return;
      }

      container.innerHTML = messages.map(m => {
        const isSelf = (m.from_phone === currentUser.phone || m.from_phone.replace(/\D/g,'') === currentUser.phone.replace(/\D/g,''));
        const alignClass = isSelf ? "align-self-end" : "align-self-start";
        const bubbleClass = isSelf ? "chat-bubble-self" : "chat-bubble-other";
        const senderName = isSelf ? t("you") : (m.from_name || m.from_phone);
        const timeStr = m.ts ? new Date(m.ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : "";

        return `
          <div class="chat-bubble ${bubbleClass} ${alignClass}">
            <div class="d-flex justify-content-between align-items-center gap-2 mb-1">
              <small class="fw-bold ${isSelf ? 'text-white-50' : 'text-success'}" style="font-size:0.72rem;">${esc(senderName)}</small>
              <small class="${isSelf ? 'text-white-50' : 'text-muted'}" style="font-size:0.68rem;">${timeStr}</small>
            </div>
            <div class="small">${esc(m.body)}</div>
          </div>`;
      }).join("");

      container.scrollTop = container.scrollHeight;
    }

    async function handleSendMessage(e) {
      e.preventDefault();
      const input = document.getElementById("chatInputText");
      const body = input.value.trim();
      if (!body || !activeChatListing || !currentUser || !activeChatPartnerPhone) return;

      try {
        const res = await fetch(`/api/listings/${activeChatListing.id}/messages`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            from_phone: currentUser.phone,
            to_phone: activeChatPartnerPhone,
            body: body
          })
        });

        if (res.ok) {
          input.value = "";
          fetchChatMessages();
        } else {
          const err = await res.json();
          showToast("Chat Error", err.detail || "Error sending message", "error");
        }
      } catch (err) {
        console.error("Send message error:", err);
      }
    }

    function startChatPolling() {
      stopChatPolling();
      chatPollTimer = setInterval(() => {
        if (activeChatListing && activeChatPartnerPhone) {
          fetchChatMessages();
        }
      }, 2500);
    }

    function stopChatPolling() {
      if (chatPollTimer) {
        clearInterval(chatPollTimer);
        chatPollTimer = null;
      }
    }

    document.getElementById("chatModal").addEventListener("hidden.bs.modal", () => {
      stopChatPolling();
      activeChatListing = null;
      activeChatPartnerPhone = null;
    });

    // =========================================================================
    // Auth Handlers
    // =========================================================================
    async function handleLogin(e) {
      e.preventDefault();
      try {
        const res = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            role: document.getElementById("loginRole").value,
            phone: document.getElementById("loginPhone").value,
            password: document.getElementById("loginPassword").value
          })
        });
        const data = await res.json();
        if (res.ok) {
          currentUser = data.user;
          localStorage.setItem("cc_user", JSON.stringify(currentUser));
          bootstrap.Modal.getInstance(document.getElementById("authModal")).hide();
          updateNavUserState();
          fetchListings();
          startSyncPolling();
          showToast("Welcome Back", `Signed in as ${currentUser.name}`, "success");
        } else {
          showToast("Login Failed", data.detail || "Invalid credentials", "error");
        }
      } catch (err) {
        console.error("Login error:", err);
        showToast("Error", "Network connection failed", "error");
      }
    }

    async function handleRegister(e) {
      e.preventDefault();
      try {
        const res = await fetch("/api/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            role: document.getElementById("regRole").value,
            name: document.getElementById("regName").value,
            phone: document.getElementById("regPhone").value,
            zip_code: document.getElementById("regZip").value,
            password: document.getElementById("regPassword").value
          })
        });
        const data = await res.json();
        if (res.ok) {
          showToast("Account Created", "Registration successful! You can now log in.", "success");
          setAuthTab("login");
        } else {
          showToast("Registration Failed", data.detail || "Failed to create account", "error");
        }
      } catch (err) {
        console.error("Register error:", err);
        showToast("Error", "Network connection failed", "error");
      }
    }

    // ============ App Init ============
    document.addEventListener("DOMContentLoaded", () => {
      setLang(currentLang);
      updateNavUserState();
      fetchListings();
      startSyncPolling();
      refreshIcons();
    });

    // Immediate init in case DOM is already loaded
    setLang(currentLang);
    updateNavUserState();
    fetchListings();
    startSyncPolling();
    setTimeout(refreshIcons, 100);
    setTimeout(refreshIcons, 500);
  </script>
</body>
</html>
"""
