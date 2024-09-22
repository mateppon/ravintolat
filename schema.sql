	CREATE TABLE users(
		id SERIAL PRIMARY KEY, 
		name TEXT,
		password TEXT,
		role INTEGER

	);

	CREATE TABLE restaurants (
		id SERIAL PRIMARY KEY,
		creator_id INTEGER REFERENCES users,
		name TEXT,
		info TEXT,
		visible BOOLEAN
	);

	CREATE TABLE addresses(
		id SERIAL PRIMARY KEY,
		restaurant_id INTEGER REFERENCES restaurants,
		street TEXT,
		street_number INTEGER,
		city TEXT
	);

	CREATE TABLE reviews(
		id SERIAL PRIMARY KEY,
		restaurant_id INTEGER REFERENCES restaurants,
		reviewer_id INTEGER REFERENCES users, 
		review TEXT,
		stars INTEGER,
		visible BOOLEAN
	);

	CREATE TABLE groups(
		id SERIAL PRIMARY KEY,
		group_name TEXT,
		creator_id INTEGER REFERENCES users,
		resutaurant_id INTEGER REFERENCES restaurants
	); 
