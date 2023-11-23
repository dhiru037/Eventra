use project1;

INSERT INTO club_head(head_id, name, phone_no, email, club_id) VALUES
('MEM01', 'Bhuvan', '12345', 'bhuvan@gmail.com', 'C01'),
('MEM02', 'Manoj', '54321', 'manoj@gmail.com', 'C02');

INSERT INTO faculty(faculty_id, fac_name, phone_no, email, club_id) VALUES
('FAC01', 'Ram', '67890', 'ram@gmail.com', 'C01'),
('FAC02', 'Sita', '09876', 'sita@gmail.com', 'C02');

INSERT INTO club(club_id, club_name, vertical, about, fac_id, headed_by) VALUES
('C01', 'Aikya', 'Social', 'Youth leadership and Social Service Club', 'FAC01', 'MEM01'),
('C02', 'Embrione', 'CS', 'Exploring new trends in tech', 'FAC02', 'MEM02');

INSERT INTO event(event_id, name, date, venue, about, fac_approval, dean_approval, remarks, club_id, proposal) VALUES
('EV01', 'Haul It Away', '2023-12-01', 'PESU52', 'Hackathon', 'Approved', 'Approved', 'Event preparations commenced', 'C01', 'https://docs.google.com/document/d/1T...'),
('EV02', 'Sampradha', '2023-12-05', 'Government Schools', NULL, 'Pending', NULL, 'Make them', 'C01', NULL),
('EV03', 'Kodikon', '2023-01-02', 'PESU52', 'Hackathon', 'Approved', 'Approved', NULL, 'C02', NULL),
('EV04', 'Xmas-thon', '2023-12-22', 'GJB', 'Kick off your holidays with a win in Xmas-thon!', 'Pending', 'Pending', 'Event Created', 'C02', '-');

INSERT INTO participant(srn, name, phone_no, email, event_id, date) VALUES
('PES01', 'Deepak', '12121', 'deepak@gmail.com', 'EV01', '2023-11-10'),
('PES02', 'Pranav', '21212', 'ps@gmail.com', 'EV01', '2023-11-12'),
('PES04', 'Athul', '78890', 'athul@gmail.com', 'EV03', '2023-11-14'),
('PES05', 'Abhay', '23394', 'abhay@gmail.com', NULL, NULL);

ALTER TABLE club ADD COLUMN image_url VARCHAR(255);
ALTER TABLE faculty ADD COLUMN image_url VARCHAR(255);
ALTER TABLE club_head ADD COLUMN image_url VARCHAR(255);

 
UPDATE club SET image_url = 'https://drive.google.com/uc?export=view&id=11khptY6TSJuEof570f0zuGHmObmnS6XZ' WHERE club_id = 'C01';
UPDATE club SET image_url = 'https://drive.google.com/uc?export=view&id=1fhcluMqrt5YemFIQ6tyM_w63YdmCV1E0' WHERE club_id = 'C02';

UPDATE faculty SET image_url = 'https://drive.google.com/uc?export=view&id=1pBX7uE3n9aoYeTETvAgnEtatN3xjezQo' WHERE faculty_id = 'FAC01';
UPDATE faculty SET image_url = 'https://drive.google.com/uc?export=view&id=1czHz5uy4-lLXWLL_7pE-aKbnpGl2-7QU' WHERE faculty_id = 'FAC02';

UPDATE club_head SET image_url = 'https://drive.google.com/uc?export=view&id=1FUg5QU-iXuePnMmlPUslcEnT_ZjBYxUW' WHERE head_id = 'MEM01';
UPDATE club_head SET image_url = 'https://drive.google.com/uc?export=view&id=1uM_rOVLzofVtuBN2Q2FbetUKWGbIVGfZ' WHERE head_id = 'MEM02';


