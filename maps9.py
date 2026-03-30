def generate_maps():
    maps = {}
    themes =[
        {"bg": "#050B14", "floor": "#0F2027", "neon": "#00f3ff", "name": "CYBER FOREST"},
        {"bg": "#140A05", "floor": "#2C150A", "neon": "#ff5e00", "name": "WASTELAND"},
        {"bg": "#020A14", "floor": "#0A2540", "neon": "#009dff", "name": "FROST MATRIX"},
        {"bg": "#1A0000", "floor": "#330000", "neon": "#ff003c", "name": "CORE INFERNO"}
    ]
    
    for stage in range(1, 21):
        theme_index = (stage - 1) // 5
        is_boss = (stage % 5 == 0)
        platforms = []
        walls = [] # חדש! קירות ממשיים שחוסמים תנועה

        # פריסת פלטפורמות ומכשולים לאורך 10,000 פיקסלים
        if not is_boss:
            # במות רגילות
            for offset in range(800, 9000, 700):
                platforms.append({"x": offset, "y_offset": 120 + (offset % 100), "w": 250, "h": 20})
            
            # הוספת "קירות" שחייבים לקפוץ מעליהם (מפוזרים לאורך המפה)
            for offset in range(1200, 8500, 1500):
                walls.append({"x": offset, "h": 150, "w": 40}) # קיר בגובה 150 פיקסלים
        else:
            # זירת בוס - פלטפורמות באזור 2000-8000
            for offset in range(1000, 8000, 1000):
                platforms.append({"x": offset, "y_offset": 160, "w": 300, "h": 20})
                platforms.append({"x": offset+400, "y_offset": 280, "w": 200, "h": 20})

        # הוספת כל סוגי האויבים בהדרגה
        allowed_enemies = ["melee"]
        if stage >= 2: allowed_enemies.append("jumper")
        if stage >= 3: allowed_enemies.append("flyer")     
        if stage >= 5: allowed_enemies.append("shooter")   
        if stage >= 7: allowed_enemies.append("bomber")    
        if stage >= 9: allowed_enemies.append("tank")      
        if stage >= 12: allowed_enemies.append("ninja")    
        if stage >= 14: allowed_enemies.append("shield")   

        maps[stage] = {
            "name": f"SYSTEM OVERLORD" if is_boss else f"{themes[theme_index]['name']} - SECTOR {stage % 5 if stage % 5 != 0 else 5}",
            "bg": themes[theme_index]["bg"],
            "floor": themes[theme_index]["floor"],
            "neon": themes[theme_index]["neon"],
            "platforms": platforms,
            "walls": walls,
            "is_boss": is_boss,
            "enemies": allowed_enemies
        }
    return maps
