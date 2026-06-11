import streamlit.components.v1 as components
import os

# Create a custom component directory for localStorage bridge
_component_dir = os.path.join(os.path.dirname(__file__), "credits_component")
os.makedirs(_component_dir, exist_ok=True)

_js_code = r"""
import { Streamlit } from "streamlit-component-lib";

function readCredits() {
    var savedCredits = localStorage.getItem('promptHub_credits');
    if (savedCredits === null || savedCredits === 'null' || savedCredits === 'undefined') {
        savedCredits = 10;
        localStorage.setItem('promptHub_credits', savedCredits);
    }
    var credits = parseInt(savedCredits);
    if (isNaN(credits)) credits = 10;
    return credits;
}

function onRender(event) {
    var credits = readCredits();
    Streamlit.setComponentValue(credits);
    Streamlit.setFrameHeight(0);
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
Streamlit.setComponentReady();
"""

# Write the JS as index.js
with open(os.path.join(_component_dir, "index.js"), "w") as f:
    f.write(_js_code)

# Create package.json
_package_json = r'''{"name": "credits-bridge", "version": "1.0.0", "main": "index.js", "dependencies": {"streamlit-component-lib": "^2.0.0"}}'''
with open(os.path.join(_component_dir, "package.json"), "w") as f:
    f.write(_package_json)

# Create index.html
_html_code = r"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body><script>
// Read credits from localStorage
var savedCredits = localStorage.getItem('promptHub_credits');
if (savedCredits === null || savedCredits === 'null' || savedCredits === 'undefined') {
    savedCredits = 10;
    localStorage.setItem('promptHub_credits', savedCredits);
}
var credits = parseInt(savedCredits);
if (isNaN(credits)) credits = 10;
// Send back to Python
if (window.parent && window.parent.postMessage) {
    window.parent.postMessage({type: 'streamlit:componentMessage', value: credits}, '*');
}
// Set iframe height to 0
document.body.style.margin = '0';
document.body.style.height = '0';
document.documentElement.style.height = '0';
</script></body>
</html>
"""
with open(os.path.join(_component_dir, "index.html"), "w") as f:
    f.write(_html_code)

_credits_bridge = components.declare_component("credits_bridge", path=_component_dir)
