create table `Employee`(
    `_id` varchar(10) primary key,
    `first_name` varchar(50) not null,
    `last_name` varchar(50) not null,
    `email` varchar(100) not null unique,
    `password` varchar(256) not null, 
    `phone` varchar(15) not null unique,
    `designation` varchar(50) not null,
    `is_active` boolean not null default true,
    `is_admin` boolean not null default false,
    `created_by` int references Employee(_id),
    `created_at` timestamp default current_timestamp,
    `updated_by` int references Employee(_id),
    `updated_at` timestamp default current_timestamp
);


create table `Room` (
	`_id` serial primary key,
	`title` varchar(20) not null unique,
	-- `type` varchar(16) not null check in("meeting", "conference"),
	`type` enum('meeting', 'conference') default 'meeting' not null,
	`capacity` int not null,
	`description` text,
	`has_microphone` boolean not null default false,
	`has_projector` boolean not null default false,
	`has_speakers` boolean not null default false,
	`has_whiteboard` boolean not null default false,
	-- `status` varchar(20) not null default `available` check in('available', 'maintenance'),
	`status` enum('available', 'maintenance') not null default 'available',
    `created_by` int references Employee(_id),
    `created_at` timestamp default current_timestamp,
    `updated_by` int references Employee(_id),
    `updated_at` timestamp default current_timestamp
);


CREATE TABLE `Team` (
	`_id` serial primary key,
	`name` varchar(20) not null,
    `created_by` int references Employee(_id),
    `created_at` timestamp default current_timestamp,
    `updated_by` int references Employee(_id),
    `updated_at` timestamp default current_timestamp
);

CREATE TABLE `TeamMember` (
	`_id` serial primary key,
	`team_id` int references Team(_id),
	`employee_id` int references Employee(_id)
);

CREATE TABLE `Meeting` (
	`_id` serial primary key,
	`title` varchar(100) NOT NULL,
	`date` DATE NOT NULL,
	`start_time` TIME NOT NULL,
	`end_time` TIME NOT NULL,
	`summary` TEXT,
	`room_id` int NOT NULL
);

CREATE TABLE `MeetingMember` (
	`_id` serial primary key,
	`meeting_id` int references Meeting(_id),
	`team_id` int references Team(_id),
	`attendee_id` int references Employee(_id)
);