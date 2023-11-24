use project1;
alter table participant add constraint fk_part2event foreign key(event_id) references event(event_id);
alter table event add constraint fk_event2club foreign key(club_id) references club(club_id);
alter table faculty add constraint fk_faculty2club foreign key(club_id) references club(club_id);
alter table club_head add constraint fk_clubhead2club foreign
key(club_id) references club(club_id);
alter table club add constraint fk_club2fac foreign key(fac_id) references faculty(faculty_id);
alter table club add constraint fk_club2clubhead foreign key(headed_by) references club_head(head_id);

ALTER TABLE club ADD COLUMN image_url VARCHAR(255);
ALTER TABLE faculty ADD COLUMN image_url VARCHAR(255);
ALTER TABLE club_head ADD COLUMN image_url VARCHAR(255);

ALTER TABLE event drop column price;