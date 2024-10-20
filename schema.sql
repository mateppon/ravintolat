	CREATE TABLE users(
		id SERIAL PRIMARY KEY, 
		name TEXT UNIQUE,
		password TEXT,
		role INTEGER

	);

	CREATE TABLE restaurants (
		id SERIAL PRIMARY KEY,
		creator_id INTEGER REFERENCES users,
		name TEXT UNIQUE,
		info TEXT,
		visible BOOLEAN
	);

	CREATE TABLE addresses(
		id SERIAL PRIMARY KEY,
		restaurant_id INTEGER REFERENCES restaurants ON DELETE CASCADE,
		coordinates TEXT		
	);

	CREATE TABLE reviews(
		id SERIAL PRIMARY KEY,
		restaurant_id INTEGER REFERENCES restaurants ON DELETE CASCADE,
		reviewer_id INTEGER REFERENCES users, 
		review TEXT,
		stars INTEGER
	);

	CREATE TABLE groups(
		id SERIAL PRIMARY KEY,
		group_name TEXT UNIQUE,
		creator_id INTEGER REFERENCES users
	); 

	CREATE TABLE restaurantsGroups(
		id SERIAL PRIMARY KEY,
		restauranst_id INTEGER REFERENCES restaurants ON DELETE CASCADE,
		group_id INTEGER REFERENCES groups ON DELETE CASCADE
	);
