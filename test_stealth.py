from playwright_stealth import stealth
print("Available in stealth module:", dir(stealth))
print("Is stealth_sync inside stealth module?", hasattr(stealth, "stealth_sync"))
print("Is sync_api inside stealth module?", hasattr(stealth, "sync_api"))

import playwright_stealth
print("Is stealth_sync inside root?", hasattr(playwright_stealth, "stealth_sync"))
print("Available in root:", [k for k in dir(playwright_stealth) if not k.startswith('_')])
