import requests
import os

def check_service_health(url, timeout=5):
    """
    Checks if a service is up (returns 200).
    """
    try:
        response = requests.head(url, timeout=timeout)
        return response.status_code == 200
    except Exception:
        return False

def get_stats_html():
    """
    Returns the HTML for the stats section.
    """
    return """
<div align="center">
  <img src="https://github-readme-stats.anuraghazra1.vercel.app/api?username=aabhiyann&show_icons=true&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&icon_color=58a6ff&text_color=c9d1d9&count_private=true" alt="GitHub Stats" height="170" />
  <img src="https://github-readme-stats.anuraghazra1.vercel.app/api/top-langs/?username=aabhiyann&layout=compact&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=c9d1d9&langs_count=8" alt="Top Languages" height="170" />
</div>

<div align="center">
  <img src="https://streak-stats.demolab.com?user=aabhiyann&theme=github-dark-blue&hide_border=true&background=0d1117&stroke=58a6ff&ring=58a6ff&fire=58a6ff&currStreakLabel=58a6ff" alt="GitHub Streak" />
</div>

<div align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=aabhiyann&theme=github-compact&hide_border=true&bg_color=0d1117&color=58a6ff&line=58a6ff&point=c9d1d9&area=true&custom_title=Contribution%20Activity" alt="Contribution Graph" width="95%" />
</div>

<div align="center">
  <img src="https://github-profile-trophy.vercel.app/?username=aabhiyann&theme=algolia&no-frame=true&margin-w=5&column=4" alt="GitHub Trophies" width="90%" />
</div>
"""

def get_fallback_html():
    """
    Returns a fallback message or empty string if services are down.
    """
    return """
<div align="center">
  <i>(GitHub stats temporarily unavailable due to external service maintenance)</i>
</div>
"""

def main():
    # Service URLs (checking the erratic ones)
    streak_url = "https://streak-stats.demolab.com?user=aabhiyann"
    trophy_url = "https://github-profile-trophy.vercel.app/"
    
    print("Checking service health...")
    # We check if AT LEAST ONE of the trouble services is up. 
    # Or strict: ALL must be up.
    # Given the user's request, if they are down, hide them.
    streak_up = check_service_health(streak_url)
    trophy_up = check_service_health(trophy_url)
    
    print(f"Streak Stats Health: {'UP' if streak_up else 'DOWN'}")
    print(f"Trophy Service Health: {'UP' if trophy_up else 'DOWN'}")
    
    # Logic: If both are DOWN, use fallback. If at least ONE is up, we might want to show partial?
    # For simplicity, if EITHER of the "fragile" services (streak/trophy) is down, 
    # we might want to hide that SPECIFIC one, or hide the whole block.
    # The user asked: "only when servers are running they display".
    
    # Let's be smart: The "Stats Cards" and "Activity Graph" usually work fine (different providers).
    # But for this implementation, we will toggle the WHOLE block based on general health 
    # to avoid a Frankenstein layout, OR we could be granular.
    # Let's try granular construction if we want to be fancy? 
    # No, keep it simple for now: "Safety Mode".
    
    if streak_up and trophy_up:
        stats_content = get_stats_html()
        print("All services operational. Generating full stats.")
    else:
        # If the erratic ones are down, do we hide EVERYTHING including the reliable ones?
        # Maybe we keep the reliable ones (Anuraghazra stats) and only hide the broken ones?
        # Let's customize get_filtered_html based on what's up.
        
        print("Some services are down. Generating filtered view.")
        
        # Always include standard stats (usually reliable vercel app)
        html_parts = [
            """
<div align="center">
  <img src="https://github-readme-stats.anuraghazra1.vercel.app/api?username=aabhiyann&show_icons=true&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&icon_color=58a6ff&text_color=c9d1d9&count_private=true" alt="GitHub Stats" height="170" />
  <img src="https://github-readme-stats.anuraghazra1.vercel.app/api/top-langs/?username=aabhiyann&layout=compact&theme=github_dark&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=c9d1d9&langs_count=8" alt="Top Languages" height="170" />
</div>
"""
        ]
        
        if streak_up:
            html_parts.append("""
<div align="center">
  <img src="https://streak-stats.demolab.com?user=aabhiyann&theme=github-dark-blue&hide_border=true&background=0d1117&stroke=58a6ff&ring=58a6ff&fire=58a6ff&currStreakLabel=58a6ff" alt="GitHub Streak" />
</div>
""")
        
        # Activity graph is usually reliable
        html_parts.append("""
<div align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=aabhiyann&theme=github-compact&hide_border=true&bg_color=0d1117&color=58a6ff&line=58a6ff&point=c9d1d9&area=true&custom_title=Contribution%20Activity" alt="Contribution Graph" width="95%" />
</div>
""")
        
        if trophy_up:
            html_parts.append("""
<div align="center">
  <img src="https://github-profile-trophy.vercel.app/?username=aabhiyann&theme=algolia&no-frame=true&margin-w=5&column=4" alt="GitHub Trophies" width="90%" />
</div>
""")
        
        stats_content = "\n".join(html_parts)

    # Read Template
    with open("README.template.md", "r") as f:
        template = f.read()
    
    # Replace Placeholder
    final_readme = template.replace("{{ STATS_SECTION }}", stats_content)
    
    # Write README
    with open("README.md", "w") as f:
        f.write(final_readme)
    
    print("README.md updated successfully.")

if __name__ == "__main__":
    main()
