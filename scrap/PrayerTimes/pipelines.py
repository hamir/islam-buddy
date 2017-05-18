# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi    
from scrapy.utils.project import get_project_settings    
 
settings = get_project_settings() 

class PrayertimesPipeline(object):
    insert_SQL = """insert into MCA (%s) values (%s)"""
    truncate_SQL = """truncate MCA"""

    def __init__(self):    
        dbargs = settings.get('DB_CONNECT')    
        db_server = settings.get('DB_SERVER')    
        dbpool = adbapi.ConnectionPool(db_server, **dbargs)    
        self.dbpool = dbpool    
 
    def __del__(self):    
        self.dbpool.close()	

    def process_item(self, item, spider):    
        keys = item.fields.keys()
	data = [item[keyIndx] for keyIndx in keys]
	#self.dbpool.runOperation(self.truncate_SQL)
	for indx, prayer in enumerate(data[0]):
	    self.insert_data(item, prayer, data[1][indx], indx, self.insert_SQL)    
        return item    
 
    def insert_data(self, item, prayer, prayerTimes, indx, insert):    
        keys = item.fields.keys()    
        fields = u','.join(keys)    
	fields = fields + ',Idx'
        qm = u','.join([u'%s'] * (len(keys)+1))    
        sql = insert % (fields, qm)    
        data = [prayer, prayerTimes, indx]
	return self.dbpool.runOperation(sql, data)       	
