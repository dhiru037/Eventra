create database project1;
use project1;
create table event(event_id varchar(10) primary key, name varchar(10), date date, venue varchar(10), about varchar(100), proposal varchar(100), price decimal(10,2) default 0, fac_approval varchar(10), dean_approval varchar(10), remarks varchar(100));
alter table event modify name varchar(10) not null;
create table faculty(faculty_id varchar(10) primary key, fac_name varchar(10) not null, phone_no varchar(10), email varchar(15), club_id varchar(10));
alter table event add club_id varchar(10);
create table club(club_id varchar(10) primary key, club_name varchar(15) not null, vertical varchar(15),about varchar(100), fac_id varchar(10), headed_by varchar(10));
create table club_head(head_id varchar(10) primary key, name varchar(15) not null, phone_no varchar(10), email varchar(15), club_id varchar(10));
 create table participant(srn varchar(10) primary key, name varchar(15) not null, phone_no varchar(10), email varchar(15), event_id varchar(10));
 alter table club_head modify email varchar(50);
alter table event modify name varchar(100);
alter table participant modify email varchar(100);





