# Package for calculating special metrics based on NFL stats

Summary

# Files
calculate_skillpoints.py - Class that calculates fantasy points (PPR) based on stats

# SkillPoints.build_skillpoints_dataframe(game_summary)
    - game_summary is a pandas dataframe that must have the following columns:
        - game_id
        - home_team
        - home_rush_yds
        - home_rush_att
        - home_rush_tds
        - home_shortpass_yds
        - home_shortpass_att
        - home_shortpass_completions
        - home_shortpass_tds
        - home_deeppass_yds
        - home_deeppass_att
        - home_deeppass_completions
        - home_deeppass_tds
        - home_interceptions
        - home_sacked
        - away_team
        - away_rush_yds
        - away_rush_att
        - away_rush_tds
        - away_shortpass_yds
        - away_shortpass_att
        - away_shortpass_completions
        - away_shortpass_tds
        - away_deeppass_yds
        - away_deeppass_att
        - away_deeppass_completions
        - away_deeppass_tds
        - away_interceptions
        - away_sacked

# Usage
    >>> sp = SkillPoints()
    >>> skillpoints_df = sp.build_skillpoints_dataframe(game_summary)

# installation

pip install --upgrade NFL_Metrics
