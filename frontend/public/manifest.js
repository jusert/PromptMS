import { MANIFEST_MATCHES } from "../src/config/domains";
export default {
    "manifest_version": 3,
    "name": "PromptMS",
    "version": "1.0.0",
    "permissions": [
    "sidePanel",
    "storage",
    "clipboardWrite",
    "tabs", 
    "activeTab"
    ],
    "host_permissions": [
        "http://127.0.0.1:8787/*"
    ],
    "action": {
        "default_title": "点击打开侧边栏"
    },
    "side_panel": {
        "default_path": "index.html"
    },
    "background": {
        "service_worker": "background.js"
    },
    "content_scripts": [
        {
            "matches": MANIFEST_MATCHES,
            "js": ["assets/content.js"],
            "run_at": "document_end"
        }
    ]
}