custom_css = """
    /* ============================================
       MAIN CONTAINER
       ============================================ */
    .progress-text { 
        display: none !important;
    }
    
    .gradio-container { 
        max-width: 1000px !important;
        width: 100% !important;
        margin: 0 auto !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        background: #0f0f0f !important;
    }
    
    /* ============================================
       TABS
       ============================================ */
    /* Tab buttons - normal state */
    button[role="tab"] {
        color: #a3a3a3 !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        transition: all 0.2s ease !important;
        background: transparent !important;
    }
    
    button[role="tab"]:hover {
        color: #e5e5e5 !important;
    }
    
    /* Selected tab - white text and white underline */
    button[role="tab"][aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #ffffff !important;
        border-radius: 0 !important;
        background: transparent !important;
    }
    
    /* Remove orange underline from tab container */
    .tabs {
        border-bottom: none !important;
        border-radius: 0 !important;
    }
    
    .tab-nav {
        border-bottom: 1px solid #3f3f3f !important;
        border-radius: 0 !important;
    }
    
    /* Remove any pseudo-elements that might create lines */
    button[role="tab"]::before,
    button[role="tab"]::after,
    .tabs::before,
    .tabs::after,
    .tab-nav::before,
    .tab-nav::after {
        display: none !important;
        content: none !important;
        border-radius: 0 !important;
    }
    
    /* Center document management tab */
    #doc-management-tab {
        max-width: 500px !important;
        margin: 0 auto !important;
    }
    
    /* ============================================
       BUTTONS
       ============================================ */
    button {
        border-radius: 8px !important;
        border: none !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }
    
    /* Primary button */
    .primary {
        background: #3b82f6 !important;
        color: white !important;
    }
    
    .primary:hover {
        background: #2563eb !important;
        transform: translateY(-1px) !important;
    }
    
    /* Stop/danger button */
    .stop {
        background: #ef4444 !important;
        color: white !important;
    }
    
    .stop:hover {
        background: #dc2626 !important;
        transform: translateY(-1px) !important;
    }

    /* =========================================================
   CHAT INPUT AREA
   ========================================================= */

    /* ---------- Chat input container ---------- */
    form:has(textarea[placeholder="Type a message..."]) {
        display: flex !important;
        align-items: center;
        gap: 12px !important;

        padding: 10px 14px !important;
        border-radius: 14px !important;

        background: #ffffff !important;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);

        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 
            0 1px 2px rgba(0, 0, 0, 0.04),
            0 6px 16px rgba(0, 0, 0, 0.06);

        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    /* Focus state for entire input container */
    form:has(textarea[placeholder="Type a message..."]:focus-within) {
        border-color: rgba(59, 130, 246, 0.6) !important;
        box-shadow: 
            0 0 0 2px rgba(59, 130, 246, 0.15),
            0 8px 20px rgba(0, 0, 0, 0.08);
    }

    /* ---------- Textarea styling ---------- */
    textarea[placeholder="Type a message..."],
    textarea[data-testid*="textbox"]:not(#file-list-box textarea) {
        flex: 1;
        resize: none !important;

        background: #ffffff !important; /* force white surface */
        border: none !important;
        outline: none !important;
        box-shadow: none !important;

        padding: 8px 4px !important;
        font-size: 14px;
        line-height: 1.5;
        color: #0f172a !important; /* black / slate-900 */

        min-height: 40px;
    }

    /* Placeholder */
    textarea::placeholder {
        color: #64748b !important; /* slate-500 */
        opacity: 1 !important; /* Firefox fix */
    }

    /* ---------- Send / submit button ---------- */
    form:has(textarea[placeholder="Type a message..."]) button[type="submit"] {
        display: flex;
        align-items: center;
        justify-content: center;

        width: 40px;
        height: 40px;

        border-radius: 10px;
        border: none !important;

        background: #3b82f6; /* blue-500 */
        color: white;

        cursor: pointer;
        transition: 
            background-color 0.2s ease,
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    /* Hover */
    form:has(textarea[placeholder="Type a message..."]) button[type="submit"]:hover {
        background: #2563eb; /* blue-600 */
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.35);
        transform: translateY(-1px);
    }

    /* Active / click */
    form:has(textarea[placeholder="Type a message..."]) button[type="submit"]:active {
        transform: translateY(0);
        box-shadow: 0 2px 6px rgba(59, 130, 246, 0.25);
    }

    /* Disabled state */
    form:has(textarea[placeholder="Type a message..."]) button[type="submit"]:disabled {
        background: #cbd5f5; /* muted blue */
        cursor: not-allowed;
        box-shadow: none;
    }

    /* ---------- Mobile friendliness ---------- */
    @media (max-width: 640px) {
        form:has(textarea[placeholder="Type a message..."]) {
            padding: 8px 10px !important;
            border-radius: 12px !important;
        }

        textarea {
            font-size: 15px;
        }
    }
    
    /* ============================================
       FILE UPLOAD - FIXED HEIGHT AND TEXT COLOR
       ============================================ */
    .file-preview, 
    [data-testid="file-upload"] {
        background: #1a1a1a !important;
        border: 1px solid #3f3f3f !important;
        border-radius: 5px !important;
        color: #ffffff !important;
        min-height: 200px !important;
    }
    
    .file-preview:hover, 
    [data-testid="file-upload"]:hover {
        border-color: #3b82f6 !important;
        background: #1f1f1f !important;
    }
    
    /* Text inside file upload - white color */
    .file-preview *,
    [data-testid="file-upload"] * {
        color: #ffffff !important;
    }
    
    /* Hide file upload label */
    .file-preview .label,
    [data-testid="file-upload"] .label {
        display: none !important;
    }
    
    /* ============================================
       INPUTS & TEXTAREAS
       ============================================ */
    input, 
    textarea {
        background: #1a1a1a !important;
        border: 1px solid #3f3f3f !important;
        border-radius: 10px !important;
        color: #e5e5e5 !important;
        transition: border-color 0.2s ease !important;
    }
    
    input:focus, 
    textarea:focus {
        border-color: #3b82f6 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    textarea[readonly] {
        background: #1a1a1a !important;
        color: #a3a3a3 !important;
    }
    
    /* ============================================
       FILE LIST BOX
       ============================================ */
    #file-list-box {
        background: #1a1a1a !important;
        border: 1px solid #3f3f3f !important;
        border-radius: 5px !important;
        padding: 10px !important;
    }
    
    #file-list-box textarea {
        background: transparent !important;
        border: none !important;
        color: #e5e5e5 !important;
        padding: 0 !important;
    }
    
    /* ============================================
       CHATBOT
       ============================================ */
    .chatbot {
        border-radius: 5px !important;
        background: #ffffff !important;
        border: none !important;
        color: #000000 !important;
    }
    .chatbot p,
    .chatbot span {
        color: #000000 !important;
        font-weight: 600 !important;  /* bold */
    }
    
    .message {
        border-radius: 10px !important;
        width: fit-content !important;
    }
    
    .message.user {
        background: #3b82f6 !important;
        color: white !important;
    }
    
    .message.bot {
        background: #1f1f1f !important;
        color: #e5e5e5 !important;
        border: 1px solid #3f3f3f !important;
    }
    
    /* ============================================
       PROGRESS BAR
       ============================================ */
    .progress-bar-wrap {
        border-radius: 10px !important;
        overflow: hidden !important;
        background: #1a1a1a !important;
    }

    .progress-bar {
        border-radius: 10px !important;
        background: #3b82f6 !important;
    }
    
    /* ============================================
       TYPOGRAPHY
       ============================================ */
    h1, h2, h3, h4, h5, h6 {
        color: #e5e5e5 !important;
    }
    
    /* ============================================
       GLOBAL OVERRIDES
       ============================================ */
    * {
        box-shadow: none !important;
    }
    
    footer {
        visibility: hidden;
    }
"""