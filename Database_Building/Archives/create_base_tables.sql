CREATE TABLE `nfl_games`
(
	`id` varchar(255),
	`season` int,
	`week` int,
	`team_home` varchar(50),
	`team_away` varchar(50),
	`spread_vistor` float,
	`over_under` float,
	`points_home` int,
	`points_away` int
);

CREATE TABLE `nfl_players`
(
	`id` varchar(255),
	`name` varchar(255),
	`team_id` varchar(255),
	`rookie_year` int,
	`position` varchar(10)
);

CREATE TABLE `nfl_teams`
(
	`id` varchar(255),
	`year` int,
	`name` varchar(255),
	`conference` varchar(255),
	`division` varchar(255),
	`record` varchar(255),
	`div_rank` varchar(255),
	`coach_head` varchar(255),
	`coach_off` varchar(255),
	`coach_def` varchar(255),
	`manager` varchar(255),
	`offensive_scheme` varchar(255),
	`defensive_scheme` varchar(255)
);

CREATE TABLE `nfl_offense`
(
	`id` varchar(255),
	`game_id` varchar(255),
	`player_id` varchar(255),
	`player_teamid` varchar(255),
	`pass_att` float,
	`pass_comp` float,
	`pass_yds` float,
	`pass_int` float,
	`rush_att` float,
	`rush_yds` float,
	`rush_tds` float,
	`rec_tgt` float,
	`rec` float,
	`rec_yds` float,
	`rec_tds` float,
	`pass_tds` float,
	`fmb_lost` float,
	`rtn_tds` float,
	`two_pts` float,
	`snapcount` int,
	`pct_snaps` float,
	`dk_points` float
);

CREATE TABLE `nfl_defense`
(
	`id` varchar(255),
	`game_id` varchar(255),
	`team_id` varchar(255),
	`pass_yds_allow` float,
	`rush_yds_allow` float,
	`rec_yds_allow` float,
	`pass_tds_allow` int,
	`flex_tds_allow` int,
	`points_allow` int,
	`sacks` float,
	`interceptions` float,
	`def_points` float,
	`dk_points` float
);
