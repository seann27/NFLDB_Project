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
	`city` varchar(255),
	`name` varchar(255),
	`abbrev` varchar(3)
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

-- ALTER TABLE `nfl_players` ADD FOREIGN KEY (`team_id`) REFERENCES `nfl_teams` (`id`);
--
-- ALTER TABLE `nfl_offense` ADD FOREIGN KEY (`game_id`) REFERENCES `nfl_games` (`id`);
--
-- ALTER TABLE `nfl_offense` ADD FOREIGN KEY (`player_id`) REFERENCES `nfl_players` (`id`);
--
-- ALTER TABLE `nfl_defense` ADD FOREIGN KEY (`game_id`) REFERENCES `nfl_games` (`id`);
--
-- ALTER TABLE `nfl_defense` ADD FOREIGN KEY (`team_id`) REFERENCES `nfl_teams` (`id`);
--
-- ALTER TABLE `nfl_games` ADD FOREIGN KEY (`team_home`) REFERENCES `nfl_teams` (`id`);
--
-- ALTER TABLE `nfl_games` ADD FOREIGN KEY (`team_away`) REFERENCES `nfl_teams` (`id`);
