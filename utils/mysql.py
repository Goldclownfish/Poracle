#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from args import args as get_args
import logging
import pymysql
from . import config
from peewee import (InsertQuery, Check, CompositeKey, ForeignKeyField,
                    SmallIntegerField, IntegerField, CharField, DoubleField,
                    BooleanField, DateTimeField, fn, DeleteQuery, FloatField,
                    TextField, JOIN, OperationalError)
from flask import Flask
from playhouse.flask_utils import FlaskDB
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import RetryOperationalError, case
from playhouse.migrate import migrate, MySQLMigrator
from playhouse.flask_utils import FlaskDB


# Globals
app = Flask(__name__)
flaskDb = FlaskDB()
sb_schema_version = 1
# Logging

log = logging.getLogger('mysql')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(threadName)18s][%(module)14s]' +
                              '[%(levelname)8s] %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)
args = get_args(os.path.abspath(os.path.dirname(__file__)))
# Test Db Connection

def connect_db():

    try:
        return pymysql.connect(host="{}".format(
            args.dbhost), port=int("{}".format(
            args.dbport)), user="{}".format(
            args.user), passwd="{}".format(
            args.password), database='{}'.format(args.database),
            connect_timeout=10)
    except pymysql.Error as e:
        log.critical("MySQL unhappy [ERROR]:% d: % s\n" % (e.args[0], e.args[1]))
        exit(1)
        return False

def check_db_version():

    log.info('Connecting to MySQL database on {}:{}'.format(args.dbhost,
                                                            args.dbport))


    db = connect_db()
    try:
        cur = db.cursor()
        cur.execute('''SELECT val FROM version where `key`='schema_version';''')
        db_ver = cur.fetchone()
        cur_ver = int(1)
    except pymysql.err.ProgrammingError:
        log.info("MySQL not happy, tables not found. Learning carpentry ...")
        db.cursor().execute('''CREATE TABLE humans(
        `id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
        `name` varchar(50),
        `enabled` tinyint(1) NOT NULL,
        `latitude` double NOT NULL,
        `longitude` double NOT NULL
        ); 
        CREATE TABLE `monsters`(
        `discord_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
        `pokemon_id` smallint(6) NOT NULL,
        `distance` smallint(6) DEFAULT NULL,
        `min_iv` smallint(6) DEFAULT NULL
        );
        CREATE TABLE `raids`(
        `discord_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
        `pokemon_id` smallint(6),
        `distance` smallint(6) DEFAULT NULL,
        `egg_level` smallint(6) 
        );
        CREATE TABLE geocode(
        `id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
        `adress` varchar(191) COLLATE utf8mb4_unicode_ci,
        `latitude` double NOT NULL,
        `longitude` double NOT NULL,
        `name` varchar(191) COLLATE utf8mb4_unicode_ci,
        `description` longtext COLLATE utf8mb4_unicode_ci,
        `url` varchar(191) COLLATE utf8mb4_unicode_ci
        ); 
        CREATE TABLE version(
        `key` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
        `val` smallint(6) NOT NULL
        );
        LOCK TABLES `version` WRITE;
        INSERT INTO `version` (`key`, `val`) VALUES ('schema_version',1);  
        UNLOCK TABLES;'''
        )
    if (db_ver[0] != cur_ver):

        log.critical('MySQL unhappy, tables looks weird, probably wrong house')
        exit(2)
    else:
        log.info('MySQL happy, tables look pretty')






