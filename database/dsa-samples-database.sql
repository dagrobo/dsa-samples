create database dsa_samples
go

use dsa_samples
go

/*===========================================================================*/
/* tbl counters */

create table sample_counter (	
	sample_year int not null,
	sample_number int not null
)
go

insert into sample_counter values(2025, 0)
go

create proc csp_get_next_sample_number
as 
	declare @stored_year int, @current_year int, @stored_number int
	set @stored_year = (select sample_year from sample_counter)
	set @current_year = YEAR(GETDATE())
	set @stored_number = (select sample_number from sample_counter)

	update sample_counter
	set 
		sample_year = case when @current_year > @stored_year then @current_year else @stored_year end,
		sample_number = case when @current_year > @stored_year then 0 else @stored_number end;	

	set @stored_number = (select sample_number from sample_counter)
	update sample_counter set sample_number = @stored_number + 1;	

	select sample_year, sample_number from sample_counter
go

/*===========================================================================*/
/* tbl sample */

create table sample (
	id uniqueidentifier primary key not null,
	number int not null,		
	external_id nvarchar(200) default null,
	import_file_hash nvarchar(200) default null,
	sample_type nvarchar(1000) not null,		
	sample_component nvarchar(200) default null,	
	station nvarchar(200) default null,	
	sampling_method nvarchar(200) default null,			
	latitude float default 0,
	longitude float default 0,
	altitude float default 0,
	sampling_date_from datetime default null,	
	sampling_date_to datetime default null,
	reference_date datetime default null,	
	wet_weight_g float default null,	
	dry_weight_g float default null,
	volume_l float default null,
	lod_weight_start float default null,	
	lod_weight_end float default null,	
	lod_temperature float default null,		
	comment nvarchar(max) default null,	
	instance_status int not null default 1,	
	create_date datetime not null,	
	update_date datetime not null	
)
go

/*===========================================================================*/
/* tbl preparation */

create table preparation (
	id uniqueidentifier primary key not null,
	sample_id uniqueidentifier not null,
	number int not null,		
	preparation_geometry nvarchar(200) default null,
	preparation_method nvarchar(200) default null,	
	amount float default 0,
	prep_unit nvarchar(200) default null,
	quantity float default 0,
	quantity_unit nvarchar(200) default null,
	fill_height_mm float default 0,			
	comment nvarchar(max) default null,	
	instance_status int not null default 1,
	create_date datetime not null,
	update_date datetime not null	
)
go

alter table preparation add foreign key (sample_id) references sample(id); 

/*===========================================================================*/
/* tbl analysis */

create table analysis (
	id uniqueidentifier primary key not null,
	number int not null,		
	preparation_id uniqueidentifier not null,
	analysis_method nvarchar(200) not null,		
	specter_reference nvarchar(200) default null,
	activity_unit nvarchar(200) default null,
	activity_unit_type nvarchar(200) default null,
	sigma_act float not null default 2.0,
	sigma_mda float not null default 1.645,
	nuclide_library nvarchar(1000) default null,
	mda_library nvarchar(1000) default null,		
	comment nvarchar(max) default null,	
	instance_status int not null default 1,
	create_date datetime not null,	
	update_date datetime not null	
)
go

alter table analysis add foreign key (preparation_id) references preparation(id); 

/*===========================================================================*/
/* tbl analysis_result */

create table analysis_result (
	id uniqueidentifier primary key not null,
	analysis_id uniqueidentifier not null,
	nuclide_name nvarchar(200) not null,	
	activity float default null,	
	activity_uncertainty_abs float not null,		
	detection_limit float default null,	
	reportable bit default 1,
	instance_status int not null default 1,
	create_date datetime not null,	
	update_date datetime not null	
)
go

alter table analysis_result add foreign key (analysis_id) references analysis(id); 

/*===========================================================================*/
/* tbl attachment */

create table attachment (
	id uniqueidentifier primary key not null,
	source_table nvarchar(200) not null,
	source_id uniqueidentifier not null,
	filename nvarchar(1000) not null,
	filename_extension nvarchar(16) not null,
	content varbinary(max) not null,
	create_date datetime not null,	
	update_date datetime not null	
)
go
