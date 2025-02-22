CREATE TABLE IF NOT EXISTS quest_monsters (
	id bigint PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
	players integer,
	health integer,
	attack varchar,
	defense varchar,
	part_breakability varchar,
	ailments varchar[],
	stun varchar,
	exhaust varchar,
	mount varchar,
	monster_id bigint,
    quest_id bigint,
	constraint fk_quest_monsters_monsters foreign key (monster_id) REFERENCES monsters (id),
	constraint fk_quest_monsters_quests foreign key (quest_id) REFERENCES quests (id)
);

-- PostgresPipeline requires a unique index for the Model's insert query
CREATE UNIQUE INDEX IF NOT EXISTS id_quest_monsters ON quest_monsters (id);
