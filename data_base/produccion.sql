create schema produccion;
use produccion;
create table if not exists maquina (
	id_maquina char(15) not null primary key,
    nombre char(30),
    area char(30)
)  engine=INNODB;
create table if not exists catalogo (
	clave_producto char(30) not null primary key,
    clase char(15),
    descripcion char(50),
    unidad char(3),
    peso double,
    estribos smallint,
    tramos smallint
)  engine=INNODB;
create table if not exists produccion_actual (
	id_maquina char(15) not null primary key, 
    golpes int not null default 0,
    unidades int not null default 0,
    kilogramos double not null default 0.0,
    producto char(30),
	foreign key (id_maquina) references maquina(id_maquina) on update cascade,
	foreign key (producto) references catalogo(clave_producto) on update cascade
)	engine=INNODB;
create table if not exists produccion_anual (
	fecha datetime not null primary key,
    turno tinyint not null,
	id_maquina char(15) not null, 
    operador char(50),
    producto char(30),
    golpes int not null default 0,
    unidades int not null default 0,
    kilogramos double not null default 0.0,
    foreign key (id_maquina) references maquina(id_maquina) on update cascade,
	foreign key (producto) references catalogo(clave_producto) on update cascade
) 	engine=INNODB;
alter table produccion_actual add column tiempo_paro time after id_maquina;
alter table produccion_anual add column tiempo_paro time after id_maquina;
alter table produccion_actual add column velocidad smallint default 0 after tiempo_paro;
alter table produccion_actual add column paros smallint default 0 after tiempo_paro;
alter table produccion_actual add column inicio time after id_maquina;
update produccion_actual set tiempo_paro = '09:00:00' where id_maquina = 'EVG';

select * from produccion_actual;
delete from catalogo where peso > 0;

select id_maquina, tiempo_paro, velocidad, golpes from produccion_actual;	 